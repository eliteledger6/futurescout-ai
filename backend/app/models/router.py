"""Model router: the only code that talks to NEAR AI (OpenAI-compatible API).

What it does for every agent call:
  * picks the agent's primary model from model_config.yaml, then its fallbacks
  * retries transient failures (rate limit, timeout, 5xx, network) with backoff
  * asks for structured output and validates it with Pydantic; one "repair"
    retry feeds the validation error back to the model
  * degrades to prompt-only JSON if the API rejects response_format
  * records tokens, estimated cost and latency per call
Nothing here logs prompts, responses or keys.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional, Type

import openai
from pydantic import BaseModel, Field, ValidationError

from app.config import Settings
from app.models.config import AgentModelConfig, ModelConfig, ModelSpec

log = logging.getLogger("futurescout.router")

_RETRYABLE = (
    openai.RateLimitError,
    openai.APITimeoutError,
    openai.APIConnectionError,
    openai.InternalServerError,
)


class ModelRouterError(RuntimeError):
    """All models failed (or a non-recoverable error such as bad credentials)."""

    def __init__(self, message: str, attempts: Optional[list[str]] = None):
        super().__init__(message)
        self.attempts = attempts or []


class _ModelFailed(Exception):
    """Internal: this model failed; try the next one."""


class UsageRecord(BaseModel):
    agent: str
    llm_alias: str
    llm_id: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cached_tokens: int = 0
    cost_usd: float = 0.0
    latency_s: float = 0.0
    ok: bool = True
    note: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RouterResult:
    text: str
    parsed: Optional[BaseModel]
    usage: UsageRecord
    llm_alias: str
    used_fallback: bool


def estimate_cost(spec: ModelSpec, prompt_tokens: int, completion_tokens: int, cached_tokens: int = 0) -> float:
    cached_tokens = min(cached_tokens, prompt_tokens)
    cache_price = spec.cache_read_per_m if spec.cache_read_per_m is not None else spec.input_per_m
    return (
        (prompt_tokens - cached_tokens) * spec.input_per_m
        + cached_tokens * cache_price
        + completion_tokens * spec.output_per_m
    ) / 1_000_000


SCHEMA_MARKER = "# Output format"


def _server_message(exc: Exception) -> str:
    """The provider's short reason for a 400 (e.g. 'System message must be at the beginning').
    Error bodies describe the request problem; they do not echo the key. Truncated."""
    body = getattr(exc, "body", None)
    msg = body.get("message") if isinstance(body, dict) else None
    if isinstance(body, dict) and isinstance(body.get("error"), dict):
        msg = body["error"].get("message") or msg
    return " ".join(str(msg or getattr(exc, "message", "") or "").split())[:200]


def extract_json(text: str) -> Any:
    """Pull a JSON object out of a model reply (handles <think> blocks and code fences)."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            raise
        return json.loads(text[start : end + 1])


class ModelRouter:
    def __init__(
        self,
        config: ModelConfig,
        settings: Settings,
        *,
        client_factory: Optional[Callable[[Settings], Any]] = None,
        sleep: Callable[[float], None] = time.sleep,
        max_retries: int = 3,
        backoff_base: float = 1.0,
    ) -> None:
        self.config = config
        self.settings = settings
        self._client_factory = client_factory or self._default_client
        self._client: Any = None
        self._sleep = sleep
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.usage: list[UsageRecord] = []
        self._degraded: set[str] = set()  # aliases that rejected response_format
        self._no_effort: set[str] = set()  # aliases that rejected reasoning_effort

    # ---- client ---------------------------------------------------------
    @staticmethod
    def _default_client(settings: Settings) -> Any:
        return openai.OpenAI(
            base_url=settings.near_ai_base_url,
            api_key=settings.require_near_key(),
            max_retries=0,  # this router does its own retrying
        )

    def _get_client(self) -> Any:
        if self._client is None:
            self._client = self._client_factory(self.settings)
        return self._client

    # ---- public ---------------------------------------------------------
    def complete(
        self,
        agent: str,
        messages: list[dict],
        *,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> RouterResult:
        if agent not in self.config.agents:
            raise ModelRouterError(f"no model configured for agent '{agent}'")
        cfg = self.config.agents[agent]
        attempts: list[str] = []
        for index, alias in enumerate([cfg.primary, *cfg.fallbacks]):
            try:
                return self._try_model(agent, alias, cfg, messages, response_model, index > 0)
            except _ModelFailed as exc:
                attempts.append(f"{alias}: {exc}")
                log.warning("agent=%s model=%s failed: %s", agent, alias, exc)
        raise ModelRouterError(
            f"all models failed for agent '{agent}'", attempts=attempts
        )

    def usage_summary(self) -> list[dict]:
        """Totals per (agent, model) for reporting."""
        totals: dict[tuple[str, str], dict] = {}
        for rec in self.usage:
            row = totals.setdefault(
                (rec.agent, rec.llm_id),
                {"agent": rec.agent, "model": rec.llm_id, "calls": 0, "failed_calls": 0,
                 "prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0.0},
            )
            row["calls"] += 1
            row["failed_calls"] += 0 if rec.ok else 1
            row["prompt_tokens"] += rec.prompt_tokens
            row["completion_tokens"] += rec.completion_tokens
            row["cost_usd"] += rec.cost_usd
        return list(totals.values())

    # ---- internals ------------------------------------------------------
    def _mode(self, alias: str, spec: ModelSpec, response_model: Optional[Type[BaseModel]]) -> str:
        if response_model is None:
            return "text"
        if alias in self._degraded:
            return "prompt_only"
        if spec.structured_outputs:
            return "json_schema"
        if spec.json_mode:
            return "json_object"
        return "prompt_only"

    @staticmethod
    def _build_messages(messages: list[dict], response_model: Optional[Type[BaseModel]]) -> list[dict]:
        """Exactly ONE system message, first (some models, e.g. Qwen on NEAR AI, reject a second
        system message: "System message must be at the beginning", seen live 2026-11-08)."""
        system_parts = [m["content"] for m in messages if m.get("role") == "system"]
        rest = [m for m in messages if m.get("role") != "system"]
        if response_model is not None:
            schema = json.dumps(response_model.model_json_schema())
            system_parts.append(
                f"{SCHEMA_MARKER}\nRespond with ONLY one JSON object that validates against this JSON Schema. "
                "No prose before or after it, no markdown fences.\n" + schema
            )
        if not system_parts:
            return rest
        return [{"role": "system", "content": "\n\n".join(system_parts)}, *rest]

    def _backoff(self, attempt: int, exc: Exception) -> float:
        retry_after = None
        response = getattr(exc, "response", None)
        if response is not None:
            raw = getattr(response, "headers", {}).get("retry-after")
            try:
                retry_after = float(raw) if raw is not None else None
            except ValueError:
                retry_after = None
        delay = retry_after if retry_after is not None else self.backoff_base * (2 ** (attempt - 1))
        return min(delay, 30.0)

    def _try_model(
        self,
        agent: str,
        alias: str,
        cfg: AgentModelConfig,
        messages: list[dict],
        response_model: Optional[Type[BaseModel]],
        used_fallback: bool,
    ) -> RouterResult:
        spec = self.config.models[alias]
        mode = self._mode(alias, spec, response_model)
        convo = self._build_messages(messages, response_model)
        transport_attempts = 0
        repaired = False
        note = ""

        while True:
            kwargs: dict[str, Any] = {
                "model": spec.id,
                "messages": convo,
                "temperature": cfg.temperature,
                "max_tokens": cfg.max_tokens,
                "timeout": cfg.timeout_s,
            }
            if cfg.reasoning_effort and spec.reasoning and alias not in self._no_effort:
                kwargs["reasoning_effort"] = cfg.reasoning_effort
            if mode == "json_schema" and response_model is not None:
                kwargs["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": response_model.__name__, "schema": response_model.model_json_schema()},
                }
            elif mode == "json_object":
                kwargs["response_format"] = {"type": "json_object"}

            started = time.perf_counter()
            try:
                response = self._get_client().chat.completions.create(**kwargs)
            except (openai.AuthenticationError, openai.PermissionDeniedError) as exc:
                # The same key is used for every model, so falling back cannot help.
                raise ModelRouterError(
                    "NEAR AI rejected the credentials (check NEAR_AI_API_KEY and credit balance)"
                ) from exc
            except openai.BadRequestError as exc:
                text = str(exc).lower()
                if "reasoning_effort" in kwargs and ("reasoning" in text or "effort" in text):
                    self._no_effort.add(alias)
                    note = (note + "; " if note else "") + "reasoning_effort rejected; sent without it"
                    continue
                if mode in ("json_schema", "json_object") and any(
                    k in text for k in ("response_format", "json_schema", "json_object")
                ):
                    self._degraded.add(alias)
                    mode = "prompt_only"
                    note = "response_format rejected; used prompt-only JSON"
                    continue
                raise _ModelFailed(f"bad request ({exc.status_code}): {_server_message(exc)}") from exc
            except _RETRYABLE as exc:
                transport_attempts += 1
                if transport_attempts > self.max_retries:
                    raise _ModelFailed(f"{type(exc).__name__} after {transport_attempts} attempts") from exc
                self._sleep(self._backoff(transport_attempts, exc))
                continue
            except openai.APIStatusError as exc:
                raise _ModelFailed(f"API error {exc.status_code}") from exc

            latency = time.perf_counter() - started
            usage = getattr(response, "usage", None)
            prompt_t = int(getattr(usage, "prompt_tokens", 0) or 0)
            completion_t = int(getattr(usage, "completion_tokens", 0) or 0)
            details = getattr(usage, "prompt_tokens_details", None)
            cached_t = int(getattr(details, "cached_tokens", 0) or 0)
            record = UsageRecord(
                agent=agent, llm_alias=alias, llm_id=spec.id,
                prompt_tokens=prompt_t, completion_tokens=completion_t, cached_tokens=cached_t,
                cost_usd=estimate_cost(spec, prompt_t, completion_t, cached_t),
                latency_s=round(latency, 3), note=note,
            )
            self.usage.append(record)
            log.info(
                "agent=%s model=%s tokens=%d/%d cost=$%.5f latency=%.1fs%s",
                agent, spec.id, prompt_t, completion_t, record.cost_usd, latency,
                " (fallback)" if used_fallback else "",
            )

            choices = getattr(response, "choices", None) or []
            content = getattr(getattr(choices[0], "message", None), "content", None) if choices else None
            finish = getattr(choices[0], "finish_reason", None) if choices else None
            if not content or not content.strip():
                record.ok = False
                if finish == "length":
                    raise _ModelFailed(f"ran out of output tokens (max_tokens={cfg.max_tokens}) before answering, "
                                       "probably while reasoning")
                raise _ModelFailed("empty response")
            if finish == "length" and response_model is not None:
                note = (note + "; " if note else "") + "output hit max_tokens (may be cut off)"
                record.note = note

            if response_model is None:
                return RouterResult(content, None, record, alias, used_fallback)

            try:
                parsed = response_model.model_validate(extract_json(content))
                return RouterResult(content, parsed, record, alias, used_fallback)
            except (ValueError, ValidationError) as exc:
                record.ok = False
                if repaired:
                    raise _ModelFailed("invalid structured output after one repair attempt") from exc
                repaired = True
                problem = str(exc)[:1500]
                convo = [
                    *convo,
                    {"role": "assistant", "content": content},
                    {"role": "user", "content": (
                        "Your reply did not validate against the schema. Problem:\n"
                        f"{problem}\nReturn ONLY the corrected JSON object."
                    )},
                ]
                continue

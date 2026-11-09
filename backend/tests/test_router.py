import json

import openai
import pytest
from pydantic import BaseModel

from app.config import ConfigError, Settings
from app.models.config import load_model_config
from app.models.router import ModelRouter, ModelRouterError, estimate_cost, extract_json
from tests.helpers import FakeClient, make_response, status_error, timeout_error


class Answer(BaseModel):
    value: int


def make_router(handler, **kw):
    settings = Settings(near_ai_api_key="test-key", _env_file=None)
    client = FakeClient(handler)
    router = ModelRouter(load_model_config(), settings, client_factory=lambda s: client,
                         sleep=lambda s: None, **kw)
    return router, client


def msgs():
    return [{"role": "user", "content": "hi"}]


def test_config_loads_and_every_agent_alias_exists():
    cfg = load_model_config()
    assert {"chief", "science", "patent", "market", "x", "risk", "investment"} <= set(cfg.agents)


def test_plain_text_call_records_usage_and_cost():
    router, client = make_router(lambda n, kw: make_response("hello", 2000, 1000))
    result = router.complete("chief", msgs())
    assert result.text == "hello" and not result.used_fallback
    spec = router.config.models[router.config.agents["chief"].primary]
    expected = (2000 * spec.input_per_m + 1000 * spec.output_per_m) / 1e6
    assert result.usage.cost_usd == pytest.approx(expected)
    assert client.calls[0]["model"] == spec.id
    assert router.usage_summary()[0]["calls"] == 1


def test_structured_output_is_parsed_and_schema_sent():
    router, client = make_router(lambda n, kw: make_response('{"value": 7}'))
    result = router.complete("chief", msgs(), response_model=Answer)  # qwen3.8: structured_outputs=true
    assert result.parsed == Answer(value=7)
    assert client.calls[0]["response_format"]["type"] == "json_schema"
    assert "JSON Schema" in client.calls[0]["messages"][0]["content"]


def test_json_mode_model_uses_json_object():
    router, client = make_router(lambda n, kw: make_response('{"value": 1}'))
    router.complete("science", msgs(), response_model=Answer)  # deepseek flash: json_mode only
    assert client.calls[0]["response_format"] == {"type": "json_object"}


def test_model_without_flags_uses_prompt_only():
    router, client = make_router(lambda n, kw: make_response('{"value": 1}'))
    router.complete("market", msgs(), response_model=Answer)  # glm_5_3: no flags
    assert "response_format" not in client.calls[0]


def test_fenced_and_think_wrapped_json_is_accepted():
    text = "<think>reasoning...</think>\n```json\n{\"value\": 3}\n```"
    assert extract_json(text) == {"value": 3}
    router, _ = make_router(lambda n, kw: make_response(text))
    assert router.complete("chief", msgs(), response_model=Answer).parsed.value == 3


def test_rate_limit_is_retried_with_backoff():
    sleeps = []

    def handler(n, kw):
        return status_error(openai.RateLimitError, 429, headers={"retry-after": "2"}) if n < 3 else make_response("ok")

    settings = Settings(near_ai_api_key="k", _env_file=None)
    client = FakeClient(handler)
    router = ModelRouter(load_model_config(), settings, client_factory=lambda s: client, sleep=sleeps.append)
    assert router.complete("chief", msgs()).text == "ok"
    assert sleeps == [2.0, 2.0] and len(client.calls) == 3


def test_timeouts_exhaust_retries_then_fall_back_to_next_model():
    def handler(n, kw):
        return timeout_error() if kw["model"] == "Qwen/Qwen3.8-27B" else make_response("from fallback")

    router, client = make_router(handler, max_retries=2)
    result = router.complete("chief", msgs())
    assert result.text == "from fallback" and result.used_fallback
    assert result.usage.llm_id == "z-ai/glm-5.3-flash"


def test_invalid_json_gets_one_repair_attempt():
    def handler(n, kw):
        return make_response("not json") if n == 1 else make_response('{"value": 9}')

    router, client = make_router(handler)
    result = router.complete("chief", msgs(), response_model=Answer)
    assert result.parsed.value == 9 and len(client.calls) == 2
    assert "did not validate" in client.calls[1]["messages"][-1]["content"]
    assert [u.ok for u in router.usage] == [False, True]


def test_persistent_invalid_output_falls_back_then_raises_with_attempt_log():
    router, client = make_router(lambda n, kw: make_response("never json"))
    with pytest.raises(ModelRouterError) as err:
        router.complete("chief", msgs(), response_model=Answer)
    assert len(err.value.attempts) == 2  # primary + one fallback
    assert len(client.calls) == 4        # each model: first try + one repair


def test_response_format_rejection_degrades_to_prompt_only():
    def handler(n, kw):
        if "response_format" in kw:
            return status_error(openai.BadRequestError, 400, "response_format json_schema is not supported")
        return make_response('{"value": 5}')

    router, client = make_router(handler)
    assert router.complete("chief", msgs(), response_model=Answer).parsed.value == 5
    assert "response_format" not in client.calls[-1]
    # remembered: the next call does not retry the rejected format
    router.complete("chief", msgs(), response_model=Answer)
    assert "response_format" not in client.calls[-1]


def test_bad_credentials_fail_fast_without_fallback():
    router, client = make_router(lambda n, kw: status_error(openai.AuthenticationError, 401))
    with pytest.raises(ModelRouterError, match="credentials"):
        router.complete("chief", msgs())
    assert len(client.calls) == 1


def test_missing_api_key_raises_clear_config_error():
    router = ModelRouter(load_model_config(), Settings(_env_file=None, near_ai_api_key=None))
    with pytest.raises(ConfigError, match="NEAR_AI_API_KEY"):
        router.complete("chief", msgs())


def test_unknown_agent_is_an_error():
    router, _ = make_router(lambda n, kw: make_response("x"))
    with pytest.raises(ModelRouterError):
        router.complete("nonexistent", msgs())


def test_cached_tokens_are_priced_at_cache_rate():
    spec = load_model_config().models["deepseek_v4_1_flash"]
    full = estimate_cost(spec, 1_000_000, 0, 0)
    cached = estimate_cost(spec, 1_000_000, 0, 1_000_000)
    assert full == pytest.approx(0.30) and cached == pytest.approx(0.006)


# ---- behaviours found in the first LIVE NEAR AI run (2026-11-08) ------------------------
def test_exactly_one_system_message_first_even_with_agent_system_prompt():
    router, client = make_router(lambda n, kw: make_response('{"value": 3}'))
    router.complete("science", [{"role": "system", "content": "AGENT PROMPT"}, {"role": "user", "content": "hi"}],
                    response_model=Answer)
    sent = client.calls[0]["messages"]
    assert [m["role"] for m in sent] == ["system", "user"]
    assert sent[0]["content"].startswith("AGENT PROMPT") and '"title": "Answer"' in sent[0]["content"]


def test_reasoning_effort_sent_to_reasoning_models_and_dropped_if_rejected():
    def handler(n, kw):
        if "reasoning_effort" in kw:
            return status_error(openai.BadRequestError, 400, "unknown parameter: reasoning_effort")
        return make_response('{"value": 1}')

    router, client = make_router(handler)
    assert router.complete("science", msgs(), response_model=Answer).parsed.value == 1
    assert client.calls[0]["reasoning_effort"] == "low" and "reasoning_effort" not in client.calls[1]
    router.complete("science", msgs(), response_model=Answer)  # remembered: not sent again
    assert "reasoning_effort" not in client.calls[2]


def test_out_of_tokens_while_reasoning_is_reported_clearly():
    from types import SimpleNamespace

    def handler(n, kw):
        r = make_response("")
        r.choices[0].finish_reason = "length"
        return r

    router, _ = make_router(handler)
    with pytest.raises(ModelRouterError) as info:
        router.complete("science", msgs(), response_model=Answer)
    assert "ran out of output tokens" in " ".join(info.value.attempts)
    assert SimpleNamespace  # noqa: keep import used


def test_bad_request_reason_from_provider_is_kept():
    router, _ = make_router(lambda n, kw: status_error(openai.BadRequestError, 400, "System message must be at the beginning."))
    with pytest.raises(ModelRouterError) as info:
        router.complete("chief", msgs())
    assert "System message must be at the beginning" in " ".join(info.value.attempts)


def test_network_libraries_never_log_urls_even_in_verbose_mode(caplog):
    """OpenAlex puts the API key in the URL; httpx logs URLs at INFO (seen live 2026-11-08)."""
    import logging

    import httpx

    from app.config import quiet_network_logs

    logging.getLogger().setLevel(logging.INFO)
    quiet_network_logs()
    transport = httpx.MockTransport(lambda r: httpx.Response(200))
    with caplog.at_level(logging.INFO):
        httpx.Client(transport=transport).get("https://api.fixture.invalid/works?api_key=FIXTURE-SECRET")
    assert "FIXTURE-SECRET" not in caplog.text

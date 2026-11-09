"""Test helpers. Everything here fakes the network: it is MOCK/FIXTURE data, never real."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import httpx
import openai

FIXTURES = Path(__file__).parent / "fixtures"


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def load_text(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


# ---- fake OpenAI-compatible client --------------------------------------
class FakeCompletions:
    def __init__(self, handler):
        self.handler = handler
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        result = self.handler(len(self.calls), kwargs)
        if isinstance(result, Exception):
            raise result
        return result


class FakeClient:
    def __init__(self, handler):
        self.chat = SimpleNamespace(completions=FakeCompletions(handler))

    @property
    def calls(self) -> list[dict]:
        return self.chat.completions.calls


def make_response(text: str, prompt_tokens: int = 1000, completion_tokens: int = 500, cached: int = 0):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text))],
        usage=SimpleNamespace(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            prompt_tokens_details=SimpleNamespace(cached_tokens=cached),
        ),
    )


def status_error(cls, status: int, message: str = "boom", headers: dict | None = None):
    request = httpx.Request("POST", "https://fake.test/v1/chat/completions")
    response = httpx.Response(status, request=request, headers=headers or {})
    return cls(message, response=response, body=None)


def schema_title(messages: list[dict]) -> str:
    """Title of the JSON schema the router put at the end of the (single) system message."""
    from app.models.router import SCHEMA_MARKER

    system = messages[0]["content"]
    after = system.split(SCHEMA_MARKER, 1)[1]
    schema_text = after[after.index("{"):]
    schema, _ = json.JSONDecoder().raw_decode(schema_text)
    return schema["title"]


class Scripted:
    """Fake model: picks a canned (MOCK) reply by the output schema the router asked for.

    replies maps schema name -> dict | Exception | list of those (used in order, last repeats).
    """

    def __init__(self, replies: dict):
        from collections import Counter

        self.replies = replies
        self.calls = Counter()

    def __call__(self, n, kwargs):
        title = schema_title(kwargs["messages"])
        self.calls[title] += 1
        reply = self.replies[title]
        if isinstance(reply, list):
            reply = reply[min(self.calls[title] - 1, len(reply) - 1)]
        if isinstance(reply, Exception):
            return reply
        return make_response(json.dumps(reply))


def timeout_error():
    return openai.APITimeoutError(request=httpx.Request("POST", "https://fake.test/v1/chat/completions"))

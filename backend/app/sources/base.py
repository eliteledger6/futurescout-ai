"""Shared helpers for API clients: errors, polite rate limiting, retrying GET."""

from __future__ import annotations

import threading
import time
from typing import Callable, Iterable, Mapping, Optional

import httpx


class SourceError(Exception):
    """A data source failed. Agents turn this into an AgentError; it never becomes fake data."""

    def __init__(self, source: str, message: str, *, retryable: bool = False, status: Optional[int] = None):
        super().__init__(f"{source}: {message}")
        self.source = source
        self.message = message
        self.retryable = retryable
        self.status = status


class RateLimiter:
    """Guarantees at least `min_interval` seconds between calls (shared across threads)."""

    def __init__(
        self,
        min_interval: float,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.min_interval = min_interval
        self._clock = clock
        self._sleep = sleep
        self._last: Optional[float] = None
        self._lock = threading.Lock()

    def wait(self) -> None:
        with self._lock:
            if self._last is not None:
                remaining = self.min_interval - (self._clock() - self._last)
                if remaining > 0:
                    self._sleep(remaining)
            self._last = self._clock()


def redact(text: str, secrets: Iterable[Optional[str]]) -> str:
    for secret in secrets:
        if secret:
            text = text.replace(secret, "***")
    return text


_RETRY_STATUS = (429, 500, 502, 503, 504)


def get_with_retry(
    http: httpx.Client,
    url: str,
    *,
    source: str,
    params: Optional[Mapping[str, object]] = None,
    secrets: Iterable[Optional[str]] = (),
    status_hints: Optional[Mapping[int, str]] = None,
    max_attempts: int = 3,
    sleep: Callable[[float], None] = time.sleep,
    before_request: Optional[Callable[[], None]] = None,
) -> httpx.Response:
    """GET with retries on 429/5xx/network errors. Error text never contains secrets."""
    secrets = list(secrets)
    hints = dict(status_hints or {})
    for attempt in range(1, max_attempts + 1):
        if before_request:
            before_request()
        try:
            response = http.get(url, params=params)
        except httpx.TransportError as exc:
            if attempt < max_attempts:
                sleep(min(2 ** (attempt - 1), 30))
                continue
            raise SourceError(
                source, redact(f"network error ({type(exc).__name__}: {exc})", secrets), retryable=True
            ) from None
        if response.status_code == 200:
            return response
        if response.status_code in _RETRY_STATUS and attempt < max_attempts:
            try:
                delay = float(response.headers.get("retry-after", ""))
            except ValueError:
                delay = float(2 ** (attempt - 1))
            sleep(min(delay, 30))
            continue
        message = hints.get(response.status_code) or f"HTTP {response.status_code}"
        raise SourceError(
            source, redact(message, secrets),
            retryable=response.status_code in _RETRY_STATUS, status=response.status_code,
        )
    raise SourceError(source, "request failed", retryable=True)  # pragma: no cover

"""Daily US stock prices from Alpha Vantage (TIME_SERIES_DAILY, free key).

Free plan (alphavantage.co, read 2026-11-08): 25 requests per day; `outputsize=compact` (the latest
100 data points) is free, `full` history is premium. So every metric here is limited to the last
~100 trading days (about 5 months) and reports say so. No 52-week or 200-day view on the free plan.

Response (known format): {"Meta Data": {...}, "Time Series (Daily)": {"YYYY-MM-DD": {"1. open": "..",
"2. high": "..", "3. low": "..", "4. close": "..", "5. volume": ".."}}}. Limit / error replies come back
with HTTP 200 and an "Information", "Note" or "Error Message" field instead. Parsed defensively and
mock-tested only until the first live call.
Prices are cached on disk for 12 hours to protect the daily quota. The key is redacted from errors.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import httpx

from app.config import BACKEND_DIR
from app.sources.base import RateLimiter, SourceError, get_with_retry

API = "https://www.alphavantage.co/query"
SOURCE = "Alpha Vantage"
CACHE_DIR = BACKEND_DIR / "cache" / "prices"
CACHE_TTL_S = 12 * 3600


@dataclass
class Bar:
    day: date
    close: float
    high: float
    low: float
    volume: float


def parse_daily(payload: object, symbol: str) -> list[Bar]:
    """Oldest first."""
    if not isinstance(payload, dict):
        raise SourceError(SOURCE, "response had an unexpected shape")
    for k in ("Error Message", "Information", "Note"):
        if payload.get(k):
            text = str(payload[k])
            if k == "Error Message":
                raise SourceError(SOURCE, f"{symbol}: symbol not found or invalid request")
            raise SourceError(SOURCE, f"{symbol}: Alpha Vantage limit or notice: {text[:160]}", retryable=True)
    series = payload.get("Time Series (Daily)")
    if not isinstance(series, dict):
        raise SourceError(SOURCE, f"{symbol}: no daily series in response")
    bars = []
    for d, row in series.items():
        try:
            bars.append(Bar(date.fromisoformat(d), float(row["4. close"]), float(row["2. high"]),
                            float(row["3. low"]), float(row.get("5. volume", 0) or 0)))
        except (KeyError, TypeError, ValueError):
            continue
    return sorted(bars, key=lambda b: b.day)


class AlphaVantageClient:
    SOURCE = SOURCE

    def __init__(
        self,
        api_key: str,
        *,
        http: Optional[httpx.Client] = None,
        limiter: Optional[RateLimiter] = None,
        cache_dir: Optional[Path] = CACHE_DIR,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if not api_key:
            raise SourceError(SOURCE, "ALPHA_VANTAGE_API_KEY is not set")
        self._key = api_key
        self._http = http or httpx.Client(timeout=30.0)
        self._limiter = limiter or RateLimiter(1.2)
        self._cache_dir = cache_dir
        self._sleep, self._clock = sleep, clock
        self.requests = 0
        self.cache_hits = 0

    @staticmethod
    def source_url(symbol: str) -> str:
        """The API request for this series, WITHOUT the key (the key is never stored or shown)."""
        return f"{API}?function=TIME_SERIES_DAILY&symbol={symbol.upper()}&outputsize=compact"

    def daily(self, symbol: str) -> list[Bar]:
        symbol = symbol.upper()
        if not symbol.replace(".", "").replace("-", "").isalnum() or len(symbol) > 10:
            raise SourceError(SOURCE, f"invalid ticker {symbol!r}")
        path = self._cache_dir / f"{symbol}.json" if self._cache_dir else None
        if path and path.is_file() and self._clock() - path.stat().st_mtime < CACHE_TTL_S:
            self.cache_hits += 1
            return parse_daily(json.loads(path.read_text(encoding="utf-8")), symbol)
        r = get_with_retry(
            self._http, API, source=SOURCE, secrets=[self._key], sleep=self._sleep, before_request=self._limiter.wait,
            params={"function": "TIME_SERIES_DAILY", "symbol": symbol, "outputsize": "compact", "apikey": self._key},
            max_attempts=2,
        )
        self.requests += 1
        try:
            payload = r.json()
        except ValueError:
            raise SourceError(SOURCE, f"{symbol}: response was not JSON") from None
        bars = parse_daily(payload, symbol)   # raises on limit/error replies (those are not cached)
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload), encoding="utf-8")
        return bars


def now_utc() -> datetime:
    return datetime.now(timezone.utc)

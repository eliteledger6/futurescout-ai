"""NEAR Intents 1Click API: token list + DRY-RUN quotes only (stage 2 of the topic funds).

A dry quote (`"dry": true`) returns what a swap would give right now without reserving anything, creating a deposit
address or sending funds. No key or JWT is needed for it. This module never builds, signs or submits a transaction.

A holding counts as tradable via NEAR Intents only if the public token list has a token whose symbol is a known
tokenized-stock form of the ticker (e.g. NVDA, NVDAon, NVDAx, bNVDA) AND whose USD price is within a tolerance of the
stock's last close (guards against unrelated tokens that share a symbol). Checked live on 2026-11-09: the public list
(216 tokens) had no tokenized stocks, so holdings show "no NEAR Intents route yet" until one appears.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Callable, Optional

import httpx
from pydantic import BaseModel

from app.sources.base import SourceError

SOURCE = "NEAR Intents 1Click"


class TokenRoute(BaseModel):
    available: bool
    symbol: Optional[str] = None
    asset_id: Optional[str] = None
    blockchain: Optional[str] = None
    token_price_usd: Optional[float] = None
    checked_at: datetime
    note: str = ""


class QuoteCheck(BaseModel):
    """A real 1Click dry-run quote: what paying `amount_in_usd` of USDC would return now. Nothing was sent."""

    amount_in_usd: float
    amount_out_usd: Optional[float] = None
    amount_out: Optional[str] = None
    cost_pct: Optional[float] = None          # (in - out) / in: fee + spread + slippage, as quoted
    time_estimate_s: Optional[float] = None
    quoted_at: datetime
    correlation_id: Optional[str] = None
    error: Optional[str] = None


def symbol_forms(ticker: str) -> set[str]:
    t = ticker.upper()
    return {t, f"{t}ON", f"{t}X", f"B{t}", f"{t}.D", f"W{t}"}


class OneClickClient:
    def __init__(self, api: str, *, http: Optional[httpx.Client] = None,
                 now: Callable[[], datetime] = lambda: datetime.now(timezone.utc)) -> None:
        self.api = api.rstrip("/")
        self._http = http or httpx.Client(timeout=30.0)
        self._now = now
        self._tokens: Optional[list[dict]] = None
        self._tokens_at = 0.0
        self.requests = 0

    def tokens(self) -> list[dict]:
        if self._tokens is not None and time.time() - self._tokens_at < 3600:
            return self._tokens
        try:
            r = self._http.get(f"{self.api}/v0/tokens")
            self.requests += 1
            r.raise_for_status()
            data = r.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SourceError(SOURCE, f"token list unavailable ({type(exc).__name__})") from None
        if not isinstance(data, list):
            raise SourceError(SOURCE, "token list had an unexpected shape")
        self._tokens, self._tokens_at = data, time.time()
        return data

    def route_for(self, ticker: str, last_close: Optional[float], tolerance_pct: float) -> TokenRoute:
        now = self._now()
        forms = symbol_forms(ticker)
        matches = [t for t in self.tokens() if str(t.get("symbol", "")).upper() in forms]
        if not matches:
            return TokenRoute(available=False, checked_at=now, note="no tokenized version in the public NEAR Intents token list")
        for t in matches:
            price = t.get("price")
            if last_close and price and abs(float(price) / last_close - 1) * 100 <= tolerance_pct:
                return TokenRoute(available=True, symbol=t.get("symbol"), asset_id=t.get("assetId"), blockchain=t.get("blockchain"),
                                  token_price_usd=float(price), checked_at=now, note="symbol and price match the stock")
        t = matches[0]
        return TokenRoute(available=False, symbol=t.get("symbol"), asset_id=t.get("assetId"), blockchain=t.get("blockchain"),
                          token_price_usd=float(t["price"]) if t.get("price") else None, checked_at=now,
                          note="a token with this symbol exists but its price does not match the stock: treated as unrelated")

    def dry_quote(self, pay_asset: str, pay_decimals: int, dest_asset: str, amount_usd: float, account: str) -> QuoteCheck:
        now = self._now()
        amount = int(Decimal(str(round(amount_usd, 2))) * (10 ** pay_decimals))
        body = {"dry": True, "swapType": "EXACT_INPUT", "slippageTolerance": 100, "originAsset": pay_asset,
                "depositType": "INTENTS", "destinationAsset": dest_asset, "amount": str(amount),
                "refundTo": account, "refundType": "INTENTS", "recipient": account, "recipientType": "INTENTS",
                "deadline": (now + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S.000Z")}
        try:
            r = self._http.post(f"{self.api}/v0/quote", json=body)
            self.requests += 1
            data = r.json()
        except (httpx.HTTPError, ValueError) as exc:
            return QuoteCheck(amount_in_usd=amount_usd, quoted_at=now, error=f"quote failed ({type(exc).__name__})")
        q = data.get("quote") if isinstance(data, dict) else None
        if r.status_code >= 400 or not q:
            msg = (data.get("message") if isinstance(data, dict) else None) or f"HTTP {r.status_code}"
            return QuoteCheck(amount_in_usd=amount_usd, quoted_at=now, error=str(msg)[:200])
        try:
            in_usd, out_usd = float(q.get("amountInUsd")), float(q.get("amountOutUsd"))
        except (TypeError, ValueError):
            in_usd, out_usd = amount_usd, None
        return QuoteCheck(amount_in_usd=round(in_usd, 2), amount_out_usd=round(out_usd, 2) if out_usd is not None else None,
                          amount_out=q.get("amountOutFormatted"),
                          cost_pct=round((in_usd - out_usd) / in_usd * 100, 3) if out_usd is not None and in_usd else None,
                          time_estimate_s=q.get("timeEstimate"), quoted_at=now, correlation_id=data.get("correlationId"))

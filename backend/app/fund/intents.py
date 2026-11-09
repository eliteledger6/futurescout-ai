"""NEAR Intents 1Click API: token list + DRY-RUN quotes only (stage 2 of the topic funds).

A dry quote (`"dry": true`) returns what a swap would give right now without reserving anything, creating a deposit
address or sending funds. No key or JWT is needed for it. This module never builds, signs or submits a transaction.

A holding counts as tradable via NEAR Intents only if a token list has a token whose symbol is a known
tokenized-stock form of the ticker (e.g. NVDA, NVDAon, NVDAx, bNVDA) AND whose USD price is within a tolerance of the
stock's last close (guards against unrelated tokens that share a symbol).

Two public lists are read (live check 2026-11-09):
  * 1Click  GET /v0/tokens (216 tokens, with prices): no tokenized stocks;
  * the NEAR Intents bridge RPC `supported_tokens` (250 tokens, no prices): 28 Ondo tokens on BNB Chain, e.g. NVDAon,
    MRVLon, INTCon, MSFTon, GOOGLon, METAon, TSLAon, SPYon. They are quotable through 1Click by their
    `intents_token_id`; for these the price check uses the price implied by a small dry-run quote.
Ondo restricts who may hold these tokens (non-US, eligibility checks); a quote says nothing about eligibility.
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
                 now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
                 bridge_rpc: Optional[str] = "https://bridge.chaindefuser.com/rpc") -> None:
        self.api = api.rstrip("/")
        self.bridge_rpc = bridge_rpc
        self._bridge: Optional[list[dict]] = None
        self.pay: Optional[tuple[str, int, str]] = None   # (pay asset, decimals, quote account): enables price checks by dry quote
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

    def bridge_tokens(self) -> list[dict]:
        """Tokens of the NEAR Intents bridge (no prices). Empty on any error: the bridge list is a bonus, not required."""
        if self._bridge is None:
            self._bridge = []
            if self.bridge_rpc:
                try:
                    r = self._http.post(self.bridge_rpc, json={"id": 1, "jsonrpc": "2.0", "method": "supported_tokens", "params": [{}]})
                    self.requests += 1
                    toks = ((r.json() or {}).get("result") or {}).get("tokens") or []
                    self._bridge = [t for t in toks if isinstance(t, dict) and t.get("asset_name") and t.get("intents_token_id")]
                except (httpx.HTTPError, ValueError, AttributeError):
                    self._bridge = []
        return self._bridge

    def _bridge_route(self, ticker: str, last_close: Optional[float], tolerance_pct: float) -> Optional[TokenRoute]:
        now = self._now()
        forms = symbol_forms(ticker)
        cands = [t for t in self.bridge_tokens() if str(t["asset_name"]).upper() in forms]
        if not cands or not self.pay or not last_close:
            return None
        t = cands[0]
        chain = {"eth:56": "BNB Chain", "eth:1": "Ethereum", "eth:8453": "Base"}.get(str(t.get("defuse_asset_identifier", "")).rsplit(":", 1)[0], "bridged")
        q = self.dry_quote(self.pay[0], self.pay[1], t["intents_token_id"], 100.0, self.pay[2])
        try:
            implied = q.amount_in_usd / float(q.amount_out) if q.amount_out and not q.error else None
        except (TypeError, ValueError, ZeroDivisionError):
            implied = None
        if implied and abs(implied / last_close - 1) * 100 <= tolerance_pct:
            return TokenRoute(available=True, symbol=t["asset_name"], asset_id=t["intents_token_id"], blockchain=chain,
                              token_price_usd=round(implied, 4), checked_at=now,
                              note="listed by the NEAR Intents bridge; the price implied by a dry-run quote matches the stock")
        return TokenRoute(available=False, symbol=t["asset_name"], asset_id=t["intents_token_id"], blockchain=chain,
                          token_price_usd=round(implied, 4) if implied else None, checked_at=now,
                          note=("listed by the NEAR Intents bridge, but no quote could be obtained right now" if not implied else
                                "a token with this symbol is listed but its quoted price does not match the stock: treated as unrelated"))

    def route_for(self, ticker: str, last_close: Optional[float], tolerance_pct: float) -> TokenRoute:
        now = self._now()
        forms = symbol_forms(ticker)
        matches = [t for t in self.tokens() if str(t.get("symbol", "")).upper() in forms]
        if not matches:
            bridged = self._bridge_route(ticker, last_close, tolerance_pct)
            if bridged is not None:
                return bridged
            return TokenRoute(available=False, checked_at=now, note="no tokenized version in the public NEAR Intents token lists")
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

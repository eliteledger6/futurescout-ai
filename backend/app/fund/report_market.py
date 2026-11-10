"""Report market (owner 2026-11-10): any trading bot can buy early access to a fresh report from the report agent.

Rule: a report is sold for its first `economy.embargo_hours` (24 h) after it was written; after that it is free on the
website for everyone. Our own trading agent buys the same way inside the system (app/fund/economy.py).

How an outside bot buys (no account with us, no API key):
  1. GET /api/market: fresh reports with their price in NEAR and the account to pay (the report agent, NEAR mainnet);
  2. send that much NEAR to the report agent with an ordinary NEAR transfer;
  3. POST /api/market/buy {run_id, tx_hash, buyer}: we read the transaction from the chain (final, signed by `buyer`,
     paid to the report agent, at least the price) and return the full report plus an access token. A transaction can be
     redeemed once. Nothing here signs or holds a key: checking a payment only reads the chain.
"""

from __future__ import annotations

import json
import secrets
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from pydantic import BaseModel, Field

from app.fund.economy import EconomyConfig, near_to_yocto, parse_transfer

_lock = threading.Lock()


class Sale(BaseModel):
    run_id: str
    buyer: str
    tx_hash: str
    amount_near: float
    token: str
    at: datetime


class MarketState(BaseModel):
    sales: list[Sale] = Field(default_factory=list)

    def by_token(self, token: str) -> Optional[Sale]:
        return next((s for s in self.sales if token and secrets.compare_digest(s.token, token)), None)

    def redeemed(self, tx_hash: str) -> Optional[Sale]:
        return next((s for s in self.sales if s.tx_hash == tx_hash), None)


def load_market(path: Path) -> MarketState:
    return MarketState.model_validate(json.loads(path.read_text(encoding="utf-8"))) if path.is_file() else MarketState()


def save_market(state: MarketState, path: Path) -> None:
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(state.model_dump_json(indent=2), encoding="utf-8")
        tmp.replace(path)


def unlock_at(generated_at: datetime, cfg: EconomyConfig) -> datetime:
    g = generated_at if generated_at.tzinfo else generated_at.replace(tzinfo=timezone.utc)
    return g + timedelta(hours=cfg.embargo_hours)


def is_locked(generated_at: datetime, cfg: EconomyConfig, now: datetime) -> bool:
    """True while a report is in its early-access window (and the market is open)."""
    return bool(cfg.market_open) and now < unlock_at(generated_at, cfg)


def buy(*, state: MarketState, path: Path, run_id: str, buyer: str, tx_hash: str, price_near: float, cfg: EconomyConfig,
        read: Callable[[str, str], Any], now: datetime) -> Sale:
    """Check the buyer's payment on chain and grant access. Raises ValueError with a plain reason when it does not qualify."""
    if not cfg.market_open:
        raise ValueError("the report market is closed")
    if not cfg.seller_account:
        raise ValueError("no report agent account is configured")
    tx_hash, buyer = (tx_hash or "").strip(), (buyer or "").strip().lower()
    if not tx_hash or not buyer:
        raise ValueError("tx_hash and buyer are required")
    used = state.redeemed(tx_hash)
    if used:
        if used.run_id == run_id and used.buyer == buyer:
            return used                                        # same purchase asked again: same access, no new sale
        raise ValueError("this transaction was already used for another purchase")
    try:
        got = parse_transfer(read(tx_hash, buyer), tx_hash=tx_hash, buyer=buyer, seller=cfg.seller_account,
                             min_yocto=near_to_yocto(price_near))
    except RuntimeError as exc:
        raise ValueError(str(exc)) from None
    sale = Sale(run_id=run_id, buyer=buyer, tx_hash=tx_hash, amount_near=round(got / 1e24, 6), token=secrets.token_urlsafe(24), at=now)
    state.sales.append(sale)
    save_market(state, path)
    return sale

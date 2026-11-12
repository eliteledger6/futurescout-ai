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
import re
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


def unlock_at(generated_at: datetime, cfg: EconomyConfig) -> Optional[datetime]:
    """When a report becomes free on the site; None when it never does (embargo_hours: null = paid access only)."""
    if cfg.embargo_hours is None:
        return None
    g = generated_at if generated_at.tzinfo else generated_at.replace(tzinfo=timezone.utc)
    return g + timedelta(hours=cfg.embargo_hours)


def demo_free(generated_at: datetime, cfg: EconomyConfig, run_id: str = "") -> bool:
    """True when a report that would be sold is open only because the owner unlocked it for the demo: it is on the
    always_free list, or it was written at or after demo_free_from."""
    if not cfg.market_open:
        return False
    if run_id and run_id in cfg.always_free:
        return True
    if cfg.demo_free_from is None:
        return False
    g = generated_at if generated_at.tzinfo else generated_at.replace(tzinfo=timezone.utc)
    f = cfg.demo_free_from if cfg.demo_free_from.tzinfo else cfg.demo_free_from.replace(tzinfo=timezone.utc)
    return g >= f


def is_locked(generated_at: datetime, cfg: EconomyConfig, now: datetime, run_id: str = "") -> bool:
    """True while the market is open and the report is not yet free (never free when embargo_hours is null), unless the
    owner made it always free."""
    if demo_free(generated_at, cfg, run_id):
        return False
    until = unlock_at(generated_at, cfg)
    return bool(cfg.market_open) and (until is None or now < until)


_TX_HASH = re.compile(r"[1-9A-HJ-NP-Za-km-z]{43,44}")                  # a NEAR transaction hash: 32 bytes in base58
_ACCOUNT = re.compile(r"(?=.{2,64}$)[a-z0-9]+([-_.][a-z0-9]+)*")       # a NEAR account name
CLAIM_HOURS = 24.0                                                     # a payment can be redeemed this long after it was made
_buy_lock = threading.Lock()


def buy(*, state: MarketState, path: Path, run_id: str, buyer: str, tx_hash: str, price_near: float, cfg: EconomyConfig,
        read: Callable[[str, str], Any], now: datetime, paid_at: Optional[Callable[[Any], Optional[datetime]]] = None,
        not_before: Optional[datetime] = None, own_accounts: tuple[str, ...] = ()) -> Sale:
    """Check the buyer's payment on chain and grant access. Raises ValueError with a plain reason when it does not qualify.

    Security pass 2026-11-12: every transfer to the report agent is public, so an old one (the owner topping the account
    up, our own trading agent paying) could be handed in by anybody to open any paid report. Now, when `paid_at` is
    given (the API always gives it): the payment must have been made after the report was written (`not_before`) and at
    most CLAIM_HOURS ago, and it may not come from one of our own accounts. One purchase is checked at a time, so the
    same payment cannot open two reports by asking twice at once."""
    if not cfg.market_open:
        raise ValueError("the report market is closed")
    if not cfg.seller_account:
        raise ValueError("no report agent account is configured")
    tx_hash, buyer = (tx_hash or "").strip(), (buyer or "").strip().lower()
    if not tx_hash or not buyer:
        raise ValueError("tx_hash and buyer are required")
    if paid_at is not None:
        if not _TX_HASH.fullmatch(tx_hash) or not _ACCOUNT.fullmatch(buyer):
            raise ValueError("tx_hash must be a NEAR transaction hash and buyer a NEAR account name")
        if buyer in {a.strip().lower() for a in (*own_accounts, cfg.seller_account) if a}:
            raise ValueError("this account's transfers are FUTURESCOUT's own and cannot be redeemed here")
    with _buy_lock:
        known = {s.tx_hash for s in state.sales}
        state.sales.extend(s for s in load_market(path).sales if s.tx_hash not in known)   # sales another request saved meanwhile
        used = state.redeemed(tx_hash)
        if used:
            if used.run_id == run_id and used.buyer == buyer:
                return used                                        # same purchase asked again: same access, no new sale
            raise ValueError("this transaction was already used for another purchase")
        try:
            payload = read(tx_hash, buyer)
            got = parse_transfer(payload, tx_hash=tx_hash, buyer=buyer, seller=cfg.seller_account,
                                 min_yocto=near_to_yocto(price_near))
        except RuntimeError as exc:
            raise ValueError(str(exc)) from None
        if paid_at is not None:
            when = paid_at(payload)
            if when is None:
                raise ValueError("the payment's time could not be read from the chain; try again in a minute")
            when = when if when.tzinfo else when.replace(tzinfo=timezone.utc)
            after = (not_before if not_before.tzinfo else not_before.replace(tzinfo=timezone.utc)) if not_before else None
            if after and when < after:
                raise ValueError("this payment was made before the report was written, so it cannot be for this report")
            if now - when > timedelta(hours=CLAIM_HOURS):
                raise ValueError(f"this payment is older than {CLAIM_HOURS:g} hours; a payment must be redeemed within that time")
        sale = Sale(run_id=run_id, buyer=buyer, tx_hash=tx_hash, amount_near=round(got / 1e24, 6), token=secrets.token_urlsafe(24), at=now)
        state.sales.append(sale)
        save_market(state, path)
        return sale

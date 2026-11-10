"""Agent economy (owner 2026-11-10): the report agent sells each research report to the trading agent for NEAR, and
stakes what it earns so the staking rewards pay for its NEAR AI usage (Staking for Inference).

Owner's limits (config/funds.yaml -> economy): a report costs at most 2 NEAR; the trading agent spends at most 10% of
its fund's value on reports; the report agent stakes 80% of its NEAR and keeps 20% for transaction fees.

Everything that moves money is checked here in code:
  * `economy.enabled` is an owner-only switch (false by default); the live trading switch and kill switch also apply;
  * a report is bought at most once; the purchase is saved as "sending" BEFORE the transfer, and an unclear send is never
    retried (it stays "sending" until checked on chain);
  * the payment is a plain NEAR transfer, then read back from the chain: signer = trading agent, receiver = report agent,
    amount >= the price, final success;
  * the stake goes only to the staking contract named in the config, and never more than stake_share of the balance.
The keys are read from .env at execution time and never stored or printed.
"""

from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Optional

import httpx
from pydantic import BaseModel, Field

YOCTO = 10 ** 24
_lock = threading.Lock()


def near_to_yocto(amount_near: float) -> int:
    return int((Decimal(str(amount_near)) * YOCTO).to_integral_value())


class EconomyConfig(BaseModel):
    enabled: bool = False                # OWNER-ONLY switch: the trading agent pays the report agent in real NEAR
    seller_account: str = ""             # the report agent's mainnet account (must match REPORT_AGENT_ACCOUNT_ID)
    max_price_near: float = 5.0          # owner 2026-11-10: a report costs 3 to 5 NEAR, set by its quality
    min_price_near: float = 3.0
    markup: float = 3.0                  # floor: never below what the report cost to make x markup
    budget_share_of_fund: float = 0.10   # owner: at most this share of the live fund's value goes to reports
    stake_share: float = 0.80            # owner: the report agent stakes this share of its NEAR ...
    min_stake_near: float = 1.0          # ... when that is at least this much (smaller stakes earn almost nothing)
    staking_contract: str = ""           # the contract behind NEAR AI's "Stake NEAR" button; empty = staking is off
    stake_method: str = "deposit_and_stake"
    stake_args: dict = Field(default_factory=dict)   # e.g. NEAR AI's product_id and price_id (copied from the dashboard's own call)
    stake_gas_tgas: int = 125
    rpc: str = "https://free.rpc.fastnear.com"
    wallet_reserve_near: float = 0.05    # the trading agent always keeps this much NEAR for fees
    pay_from: str = "wallet"             # "wallet" (plain transfer) or "private" (signed order from the near.com balance)
    market_open: bool = False            # owner 2026-11-10: outside bots may buy early access to fresh reports (GET/POST /api/market)
    embargo_hours: float = 24.0          # a report is sold for this long after it was written, then it is free on the site


class Price(BaseModel):
    run_id: str
    topic: str
    price_near: float
    price_usd: float
    cost_usd: float
    basis: str
    at: datetime


class Purchase(BaseModel):
    id: str
    run_id: str
    topic: str
    price_near: float
    buyer: str
    seller: str
    status: str = "sending"              # sending | paid | failed
    tx_hash: Optional[str] = None
    note: str = ""
    at: datetime


class StakeEvent(BaseModel):
    id: str
    account: str
    contract: str
    amount_near: float
    balance_before_near: float
    status: str = "sending"              # sending | staked | failed
    tx_hash: Optional[str] = None
    note: str = ""
    at: datetime


class EconomyState(BaseModel):
    prices: dict[str, Price] = Field(default_factory=dict)
    purchases: list[Purchase] = Field(default_factory=list)
    stakes: list[StakeEvent] = Field(default_factory=list)

    def bought(self, run_id: str) -> Optional[Purchase]:
        return next((p for p in self.purchases if p.run_id == run_id and p.status in ("paid", "sending")), None)

    def spent_near(self) -> float:
        return round(sum(p.price_near for p in self.purchases if p.status in ("paid", "sending")), 6)


def load_economy(path: Path) -> EconomyState:
    return EconomyState.model_validate(json.loads(path.read_text(encoding="utf-8"))) if path.is_file() else EconomyState()


def save_economy(state: EconomyState, path: Path) -> None:
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(state.model_dump_json(indent=2), encoding="utf-8")
        tmp.replace(path)


# ------------------------------------------------------------------ pricing (the report agent sets its price)
def price_report(*, run_id: str, topic: str, cost_usd: float, score: Optional[float], confidence_pct: Optional[float],
                 near_usd: float, cfg: EconomyConfig, now: datetime) -> Price:
    """Price inside the owner's band by quality (score and confidence): the weakest report costs min_price_near, the best
    max_price_near; never below what the report cost to make (x markup)."""
    s = (score if score is not None else 40.0) / 100
    c = (confidence_pct if confidence_pct is not None else 30.0) / 100
    quality = max(0.0, min(1.0, s * (0.5 + c)))  # e.g. score 80, confidence 50% -> 0.8
    near = cfg.min_price_near + (cfg.max_price_near - cfg.min_price_near) * quality
    floor = cost_usd * cfg.markup / near_usd if near_usd > 0 else 0.0
    near = round(min(cfg.max_price_near, max(near, floor)), 3)
    usd = near * near_usd
    basis = (f"quality {quality:.2f} (score {score if score is not None else 'n/a'}, confidence "
             f"{confidence_pct if confidence_pct is not None else 'n/a'}%) inside the {cfg.min_price_near:g}-{cfg.max_price_near:g} NEAR band "
             f"= {near:g} NEAR (${usd:.2f}); the report cost ${cost_usd:.2f} of AI to make")
    return Price(run_id=run_id, topic=topic, price_near=near, price_usd=round(near * near_usd, 4), cost_usd=round(cost_usd, 4), basis=basis, at=now)


# ------------------------------------------------------------------ the trading agent's report budget
def report_budget_near(*, fund_value_usd: float, near_usd: float, state: EconomyState, cfg: EconomyConfig) -> float:
    """NEAR still available for reports: budget_share_of_fund of the fund's value, minus what reports already cost."""
    if near_usd <= 0:
        return 0.0
    return round(max(0.0, cfg.budget_share_of_fund * fund_value_usd / near_usd - state.spent_near()), 6)


def purchase_blocks(*, state: EconomyState, price: Price, budget_near: float, wallet_near: Optional[float], cfg: EconomyConfig,
                    trading_enabled: bool, kill_switch: bool) -> list[str]:
    bad: list[str] = []
    if not cfg.enabled:
        bad.append("the agent economy is switched off (economy.enabled is false in config/funds.yaml)")
    if not trading_enabled:
        bad.append("trading_enabled is false")
    if kill_switch:
        bad.append("kill switch is on")
    if not cfg.seller_account:
        bad.append("no report agent account in economy.seller_account")
    if state.bought(price.run_id):
        bad.append("this report was already bought")
    if price.price_near > cfg.max_price_near + 1e-9:
        bad.append(f"price {price.price_near} NEAR is above the {cfg.max_price_near} NEAR limit")
    if price.price_near > budget_near + 1e-9:
        bad.append(f"price {price.price_near} NEAR is above the report budget left ({budget_near:.3f} NEAR = "
                   f"{cfg.budget_share_of_fund:.0%} of the fund minus reports already bought)")
    if wallet_near is not None and wallet_near - cfg.wallet_reserve_near < price.price_near:
        bad.append(f"the trading wallet holds {wallet_near:.3f} NEAR; {price.price_near} NEAR plus the {cfg.wallet_reserve_near} NEAR fee reserve is needed")
    return bad


def parse_transfer(payload: Any, *, tx_hash: str, buyer: str, seller: str, min_yocto: int) -> int:
    """Check a `tx` RPC result: final success, signed by the buyer, paid to the seller, at least the price. Returns the amount."""
    if not isinstance(payload, dict) or "error" in payload:
        raise RuntimeError(f"transaction not readable: {str((payload or {}).get('error'))[:160] if isinstance(payload, dict) else 'bad shape'}")
    result = payload.get("result") or {}
    status = result.get("status") or {}
    if "SuccessValue" not in status and "SuccessReceiptId" not in status:
        raise RuntimeError("transaction did not succeed (or is not final yet)")
    tx = result.get("transaction") or {}
    if tx.get("hash") and tx["hash"] != tx_hash:
        raise RuntimeError("transaction hash mismatch")
    if tx.get("signer_id") != buyer:
        raise RuntimeError(f"signed by {tx.get('signer_id')}, not by the buyer {buyer}")
    if tx.get("receiver_id") != seller:
        raise RuntimeError(f"paid {tx.get('receiver_id')}, not the report agent {seller}")
    total = sum(int(a["Transfer"].get("deposit") or 0) for a in tx.get("actions") or [] if isinstance(a, dict) and "Transfer" in a)
    if total < min_yocto:
        raise RuntimeError(f"payment too small: {total / YOCTO:.4f} NEAR, the price is {min_yocto / YOCTO:.4f} NEAR")
    return total


def read_tx(http: httpx.Client, rpc: str, tx_hash: str, sender: str) -> Any:
    body = {"jsonrpc": "2.0", "id": "fs-econ", "method": "tx", "params": {"tx_hash": tx_hash, "sender_account_id": sender, "wait_until": "FINAL"}}
    return http.post(rpc, json=body, timeout=60).json()


def buy_report(*, state: EconomyState, path: Path, price: Price, buyer: str, cfg: EconomyConfig,
               send: Callable[[str, int], str], read: Callable[[str, str], Any], now: datetime) -> Purchase:
    """Pay the report agent exactly once, then confirm the payment on chain. `send(receiver, yocto) -> tx hash` signs."""
    p = Purchase(id=uuid.uuid4().hex[:10], run_id=price.run_id, topic=price.topic, price_near=price.price_near, buyer=buyer,
                 seller=cfg.seller_account, at=now, note="saved before sending; never sent twice")
    state.purchases.append(p)
    save_economy(state, path)                                         # point of no return: recorded first
    try:
        p.tx_hash = send(cfg.seller_account, near_to_yocto(price.price_near)) or None
    except Exception as exc:  # noqa: BLE001
        p.note = f"send step raised ({str(exc)[:160]}); kept as 'sending': check the account on nearblocks before anything else"
        save_economy(state, path)
        return p
    try:
        got = parse_transfer(read(p.tx_hash or "", buyer), tx_hash=p.tx_hash or "", buyer=buyer, seller=cfg.seller_account,
                             min_yocto=near_to_yocto(price.price_near))
        p.status, p.note = "paid", f"paid {got / YOCTO:g} NEAR; confirmed on NEAR mainnet"
    except Exception as exc:  # noqa: BLE001
        p.note = f"sent, but the on-chain check did not confirm it yet: {str(exc)[:160]}"
    save_economy(state, path)
    return p


# ------------------------------------------------------------------ the report agent stakes what it earned
def stake_amount_yocto(balance_yocto: int, cfg: EconomyConfig) -> Optional[int]:
    """stake_share of the balance (the rest stays for fees), or None when that is under min_stake_near or staking is off."""
    if not cfg.staking_contract:
        return None
    amount = int(Decimal(balance_yocto) * Decimal(str(cfg.stake_share)))
    return amount if amount >= near_to_yocto(cfg.min_stake_near) else None


def stake(*, state: EconomyState, path: Path, account: str, balance_yocto: int, cfg: EconomyConfig,
          call: Callable[[str, str, dict, int, int], str], now: datetime) -> Optional[StakeEvent]:
    """Stake stake_share of the report agent's NEAR into the configured pool. `call(contract, method, args, gas, deposit)` signs."""
    amount = stake_amount_yocto(balance_yocto, cfg)
    if amount is None:
        return None
    ev = StakeEvent(id=uuid.uuid4().hex[:10], account=account, contract=cfg.staking_contract, amount_near=round(amount / YOCTO, 6),
                    balance_before_near=round(balance_yocto / YOCTO, 6), at=now, note="saved before sending")
    state.stakes.append(ev)
    save_economy(state, path)
    try:
        ev.tx_hash = call(cfg.staking_contract, cfg.stake_method, dict(cfg.stake_args), cfg.stake_gas_tgas * 10 ** 12, amount) or None
        ev.status, ev.note = "staked", f"staked {ev.amount_near:g} NEAR ({cfg.stake_share:.0%} of {ev.balance_before_near:g}); the rest stays for fees"
    except Exception as exc:  # noqa: BLE001
        ev.status, ev.note = "failed", f"stake refused: {str(exc)[:200]}"
    save_economy(state, path)
    return ev


def account_near(http: httpx.Client, rpc: str, account: str) -> tuple[int, int]:
    """(liquid yocto, locked yocto) of an account. Read-only."""
    body = {"jsonrpc": "2.0", "id": "fs-econ", "method": "query", "params": {"request_type": "view_account", "finality": "final", "account_id": account}}
    r = (http.post(rpc, json=body, timeout=30).json().get("result") or {})
    return int(r.get("amount") or 0), int(r.get("locked") or 0)


def staked_amount(http: httpx.Client, cfg: EconomyConfig, account: str) -> Optional[int]:
    """NEAR `account` has staked through the configured contract. NEAR AI's stake.dao: get_farm_position(account_id,
    product_id) -> staked_near_amount (seen 2026-11-10); a plain staking pool: get_account_staked_balance. Read-only."""
    if not cfg.staking_contract:
        return None
    import base64
    product = cfg.stake_args.get("product_id")
    method, args = (("get_farm_position", {"account_id": account, "product_id": product}) if product
                    else ("get_account_staked_balance", {"account_id": account}))
    body = {"jsonrpc": "2.0", "id": "fs-econ", "method": "query",
            "params": {"request_type": "call_function", "finality": "final", "account_id": cfg.staking_contract, "method_name": method,
                       "args_base64": base64.b64encode(json.dumps(args).encode()).decode()}}
    try:
        out = json.loads(bytes(http.post(cfg.rpc, json=body, timeout=30).json()["result"]["result"]).decode())
        return int(out["staked_near_amount"]) if isinstance(out, dict) else int(out or 0)
    except Exception:  # noqa: BLE001
        return None

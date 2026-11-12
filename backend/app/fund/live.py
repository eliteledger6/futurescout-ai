"""Stage 3: small REAL trades through NEAR Intents 1Click, with hard limits (owner go-ahead 2026-11-09).

Owner's written scope: a dedicated mainnet account funded with about 5 USD of USDC + 0.5 NEAR; a trading agent on a
strong model proposes; the owner approves each trade on this machine; the first trade proves the path works; shadow
mode (real quotes, nothing sent) continues with a larger pretend budget. See STAGE3_PLAN.md.

Safety, all enforced HERE in code and never left to a model:
  * `trading_enabled` is false by default (config/funds.yaml -> live), and a kill-switch file stops everything;
  * BUYS of tokens on the allowlist built from the price-checked Ondo routes; SELLS (owner's written yes 2026-11-10) only of
    a token the fund holds, only on the private signed route, only when the owner set `live.sells_enabled: true`;
  * caps per trade, per UTC day and in total; quoted price within a band of the stock's last close; cost cap;
  * a proposal can be executed once: its status is saved as "executing" BEFORE any transfer, and a proposal that is
    past "approved" is never sent again (resume only polls the status of the deposit already made);
  * the only on-chain writes are `storage_deposit` (if the deposit address needs it) and one `ft_transfer` of USDC
    to the deposit address returned by a real 1Click quote; refunds go back to the same account;
  * the key is read from FUND_MAINNET_PRIVATE_KEY at execution time, never stored, logged or returned by the API.

Nothing in this module runs by itself: `scripts/fund_trade.py approve <id>` is the only caller of `execute`.
There is no testnet for NEAR Intents (their docs say so), so the mock tests cover the logic and the first small
live trade is the real integration test.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Literal, Optional

import httpx
from pydantic import BaseModel, Field

from app.fund.strategy import StrategyConfig

DISCLAIMER = ("Real money with a small budget capped by the owner; orders run after the code checks on the agent's own approval "
              "(the owner's setting live.auto_approve; without it each order waits for the owner). Tokenized stocks are issued by Ondo and are "
              "not the shares themselves. Not investment advice.")
FINAL = {"success", "refunded", "failed", "rejected", "shadow_filled", "hold"}
SPENT = {"executing", "deposited", "success"}          # statuses that count against the caps
SIDES = ("buy", "sell")


# ------------------------------------------------------------------ config
class LiveConfig(BaseModel):
    auto_approve: bool = False           # FUTURE, owner-only: when true a live proposal from a strategy check is executed without the
                                         # typed approval. Built 2026-11-10 at the owner's request ("for now still owner approves");
                                         # Claude never sets it to true. Every other check (caps, allowlist, price band, kill switch) still runs.
    strategy: StrategyConfig = Field(default_factory=StrategyConfig)   # when the agent wakes up and its fixed rules (app/fund/strategy.py)
    trading_enabled: bool = False
    rpc: str = "https://free.rpc.fastnear.com"     # rpc.mainnet.near.org is deprecated and rate-limits (HTTP 429, seen 2026-11-09)
    usdc_contract: str = "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1"
    usdc_decimals: int = 6
    pay_with: str = "near"               # "near" (native NEAR, owner's choice 2026-11-09) or "usdc"
    near_asset_id: str = "nep141:wrap.near"   # how 1Click names NEAR; a plain NEAR transfer to the deposit address pays it
    near_reserve: float = 0.05           # NEAR always left in the account for fees
    private_reserve_near: float = 0.2    # NEAR always left in the near.com balance when a buy is sized from it
    route: str = "wallet"                # "wallet" = pay from the wallet to a deposit address (got stuck 2026-11-09);
                                         # "confidential" = signed order from the private balance, as near.com does
    signed_route_enabled: bool = False   # second switch for the confidential route; false = built but cannot submit
    order_recipients: list[str] = ["intents.near"]   # verifiers a generated order may be addressed to
    intents_contract: str = "intents.near"
    sells_enabled: bool = False          # OWNER-ONLY switch (written yes 2026-11-10): the agent may sell a held token for NEAR
    budget_mode: Literal["spent", "net"] = "spent"   # "spent": the total cap counts every dollar ever spent on buys;
                                         # "net" (OWNER-ONLY): it counts buys minus the proceeds of sales, so sale money can be re-invested
    max_sells_per_day: int = 2
    max_trade_usd: float = 5.0
    max_day_usd: float = 5.0
    max_total_usd: float = 5.0
    min_trade_usd: float = 1.0
    price_band_pct: float = 3.0          # quoted token price vs the stock's last close (close up to 1 day old); 0 = no band in
                                         # code: the agent sees the gap and decides (owner 2026-11-11)
    band_per_stale_day_pct: float = 1.5  # extra band per further day of age of that close
    max_band_pct: float = 8.0
    max_cost_pct: float = 2.0            # (in - out) / in of the real quote
    slippage_bps: int = 100
    deadline_minutes: int = 30
    poll_seconds: float = 5.0
    poll_timeout_seconds: float = 600.0
    shadow_budget_usd: float = 10000.0
    explorer_tx: str = "https://nearblocks.io/txns/{tx}"


# ------------------------------------------------------------------ state
class Event(BaseModel):
    at: datetime
    status: str
    note: str = ""


class Proposal(BaseModel):
    id: str
    created_at: datetime
    mode: str                                  # live | shadow
    side: str = "buy"                          # buy | sell | hold (the agent proposed to do nothing)
    topic: str
    ticker: str
    symbol: str                                # token symbol, e.g. INTCon
    asset_id: str
    usd: float                                 # buy: amount paid; sell: estimated value of what is sold
    fraction: Optional[float] = None           # sell: share of the holding to sell (0..1)
    quantity: Optional[float] = None           # sell: tokens to sell (estimate at proposal time; the real amount is in quote)
    rationale: str = ""
    risks: list[str] = Field(default_factory=list)
    confidence: str = "low"
    model: Optional[str] = None
    model_cost_usd: float = 0.0
    ref_close: Optional[float] = None          # the stock's last daily close used for the price check
    ref_close_date: Optional[str] = None
    dry_quote: Optional[dict] = None           # at proposal time
    status: str = "proposed"                   # proposed | approved | rejected | executing | deposited | success | refunded | failed | shadow_filled
    quote: Optional[dict] = None               # the real quote (or the dry one in shadow mode) used at execution
    deposit_address: Optional[str] = None
    deposit_tx: Optional[str] = None
    result: Optional[dict] = None              # final 1Click status payload (trimmed)
    error: Optional[str] = None
    history: list[Event] = Field(default_factory=list)
    sha256: Optional[str] = None               # fingerprint of the finished record
    correction: Optional[str] = None           # a later, clearly marked correction of the record's wording (not part of the fingerprint)
    chain: Optional[dict] = None               # NEAR testnet record of that fingerprint

    def mark(self, status: str, note: str = "", now: Optional[datetime] = None) -> None:
        self.status = status
        self.history.append(Event(at=now or datetime.now(timezone.utc), status=status, note=note[:300]))


class TradingState(BaseModel):
    proposals: list[Proposal] = Field(default_factory=list)
    updated_at: Optional[datetime] = None
    checks: list = Field(default_factory=list)            # strategy wake-ups (app.fund.strategy.Check), newest last
    seen_runs: dict[str, str] = Field(default_factory=dict)     # topic -> report run id already considered
    seen_closes: dict[str, str] = Field(default_factory=dict)   # ticker -> close date already reacted to
    # owner 2026-11-12: "the trading agent should always be aware of the price of the share it is holding". Every check
    # reads each holding's live token price. key = ticker (live holdings: "live:" + ticker) -> {price, at, cost_per_share,
    # gain_pct, seen_price, seen_at, since_seen_pct}; seen_* = the price when the agent last looked at the holding.
    holding_prices: dict[str, dict] = Field(default_factory=dict)
    last_check_at: Optional[datetime] = None
    last_live_check_at: Optional[datetime] = None          # live and shadow react to the same events separately
    private_near: Optional[float] = None                   # NEAR in the near.com (private) balance, read by the owner's loop after a
    private_checked_at: Optional[datetime] = None          # signed login; the read-only site shows this snapshot
    last_values: dict[str, dict] = Field(default_factory=dict)   # symbol -> {"usd", "at"}: last good dry-quote value of a holding,
                                                           # used when NEAR Intents cannot quote it (owner 2026-11-10)
    hidden: list[str] = Field(default_factory=list)        # owner 2026-11-10: records kept in this file but not shown on the site
                                                           # and not counted as holdings (e.g. MRVLon, sold by hand in near.com)

    def get(self, pid: str) -> Optional[Proposal]:
        return next((p for p in self.proposals if p.id == pid or p.id.startswith(pid)), None)

    def spent(self, mode: str = "live", day: Optional[str] = None) -> float:
        """Dollars paid for BUYS (sells never count here)."""
        tot = 0.0
        for p in self.proposals:
            if p.mode != mode or p.status not in SPENT or p.side != "buy":
                continue
            if day and not any(e.status == "executing" and e.at.astimezone(timezone.utc).date().isoformat() == day for e in p.history):
                continue
            tot += p.usd
        return round(tot, 2)

    def proceeds(self, mode: str = "live") -> float:
        """Dollars received from finished SALES (the amount actually reported, else the quote's)."""
        return round(sum(_usd_out(p) for p in self.proposals
                         if p.mode == mode and p.side == "sell" and p.status in ("success", "shadow_filled")), 2)

    def invested(self, mode: str, budget_mode: str) -> float:
        """What the total cap is measured against: every buy ("spent") or buys minus sale proceeds ("net")."""
        return round(self.spent(mode) - (self.proceeds(mode) if budget_mode == "net" else 0.0), 2)

    def sells_today(self, mode: str, day: str) -> int:
        return sum(1 for p in self.proposals if p.mode == mode and p.side == "sell"
                   and any(e.status in ("executing", "shadow_filled") and e.at.astimezone(timezone.utc).date().isoformat() == day for e in p.history))

    def live_holdings(self) -> list[dict]:
        """Tokens the live fund holds according to its own records: finished buys minus sales (finished or under way)."""
        rows: dict[str, dict] = {}
        for p in sorted(self.proposals, key=lambda x: x.created_at):
            if p.mode != "live" or p.side not in SIDES or p.id in self.hidden:
                continue
            if p.side == "buy" and p.status == "success":
                r = rows.setdefault(p.symbol, {"ticker": p.ticker, "symbol": p.symbol, "asset_id": p.asset_id, "topic": p.topic, "quantity": 0.0,
                                               "cost_usd": 0.0, "first_bought": p.created_at.isoformat(), "buys": 0})
                r["quantity"] += _qty_out(p)
                r["cost_usd"] += p.usd
                r["buys"] += 1
            elif p.side == "sell" and p.status in SPENT and p.symbol in rows:
                r = rows[p.symbol]
                sold = _qty_in(p)
                if r["quantity"] > 0:
                    r["cost_usd"] *= max(0.0, 1 - sold / r["quantity"])
                r["quantity"] = max(0.0, r["quantity"] - sold)
        return [{**r, "quantity": round(r["quantity"], 8), "cost_usd": round(r["cost_usd"], 2)} for r in rows.values() if r["quantity"] > 1e-9]


def _num(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _qty_out(p: "Proposal") -> float:
    return _num((p.result or {}).get("amountOutFormatted")) or _num((p.quote or {}).get("amountOutFormatted"))


def _qty_in(p: "Proposal") -> float:
    return _num((p.result or {}).get("amountInFormatted")) or _num((p.quote or {}).get("amountInFormatted")) or _num(p.quantity)


def _usd_out(p: "Proposal") -> float:
    return _num((p.result or {}).get("amountOutUsd")) or _num((p.quote or {}).get("amountOutUsd"))


_lock = threading.Lock()


def load_state(path: Path) -> TradingState:
    if path.is_file():
        return TradingState.model_validate(json.loads(path.read_text(encoding="utf-8")))
    return TradingState()


def save_state(state: TradingState, path: Path) -> None:
    with _lock:
        state.updated_at = datetime.now(timezone.utc)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(state.model_dump_json(indent=2), encoding="utf-8")
        tmp.replace(path)


def new_id() -> str:
    return uuid.uuid4().hex[:10]


def fingerprint(p: Proposal) -> str:
    data = p.model_dump(mode="json", exclude={"sha256", "chain", "correction"})
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# ------------------------------------------------------------------ limits (pure code)
def check_limits(state: TradingState, p: Proposal, cfg: LiveConfig, *, kill_switch: bool, now: datetime) -> list[str]:
    """Every reason this proposal may NOT be executed live right now. Empty list = allowed."""
    bad: list[str] = []
    if kill_switch:
        bad.append("kill switch is on (STOP file present)")
    if not cfg.trading_enabled:
        bad.append("trading_enabled is false in config/funds.yaml")
    if p.side not in SIDES:
        bad.append(f"'{p.side}' is not a trade")
        return bad
    day = now.astimezone(timezone.utc).date().isoformat()
    if p.side == "sell":
        if not cfg.sells_enabled:
            bad.append("selling is built but switched off (live.sells_enabled is false in config/funds.yaml)")
        if state.sells_today("live", day) >= cfg.max_sells_per_day:
            bad.append(f"already {cfg.max_sells_per_day} sale(s) today (live.max_sells_per_day)")
        if not p.fraction or not 0 < p.fraction <= 1:
            bad.append("a sale needs a share of the holding between 0 and 1")
        if not any(h["symbol"] == p.symbol for h in state.live_holdings()):
            bad.append(f"the fund holds no {p.symbol} according to its records")
        if p.usd < cfg.min_trade_usd:
            bad.append(f"the sale is worth about ${p.usd:.2f}, below the minimum ${cfg.min_trade_usd:.2f}")
        return bad
    if p.usd < cfg.min_trade_usd:
        bad.append(f"amount ${p.usd:.2f} is below the minimum ${cfg.min_trade_usd:.2f}")
    if p.usd > cfg.max_trade_usd + 1e-9:
        bad.append(f"amount ${p.usd:.2f} is above the per-trade cap ${cfg.max_trade_usd:.2f}")
    if state.spent("live", day) + p.usd > cfg.max_day_usd + 1e-9:
        bad.append(f"daily cap ${cfg.max_day_usd:.2f} would be exceeded (already ${state.spent('live', day):.2f} today)")
    used = state.invested("live", cfg.budget_mode)
    if used + p.usd > cfg.max_total_usd + 1e-9:
        what = "invested net of sales" if cfg.budget_mode == "net" else "in total"
        bad.append(f"total cap ${cfg.max_total_usd:.2f} would be exceeded (already ${used:.2f} {what})")
    return bad


def check_sell_quote(q: dict, p: Proposal, cfg: LiveConfig, now: Optional[datetime] = None) -> list[str]:
    """Sanity checks on a SALE quote (token in, NEAR out) before anything is signed: the swap cost, and the price received per
    token must not be far BELOW the stock's last close (selling above it is fine)."""
    try:
        q_in, in_usd, out_usd = float(q["amountInFormatted"]), float(q["amountInUsd"]), float(q["amountOutUsd"])
    except (KeyError, TypeError, ValueError):
        return ["quote is missing amounts"]
    if q_in <= 0 or in_usd <= 0 or out_usd <= 0:
        return ["quote has non-positive amounts"]
    bad: list[str] = []
    cost = (in_usd - out_usd) / in_usd * 100
    if cost > cfg.max_cost_pct:
        bad.append(f"quoted cost {cost:.2f}% is above the cap {cfg.max_cost_pct:.2f}%")
    if cfg.price_band_pct <= 0:
        return bad                                    # owner 2026-11-11: no code band; the agent judged the price itself
    if p.ref_close:
        got = out_usd / q_in
        band = price_band(cfg, p.ref_close_date, now or datetime.now(timezone.utc))
        if got < p.ref_close * (1 - band / 100):
            bad.append(f"the sale pays ${got:.2f} per token, {(1 - got / p.ref_close) * 100:.1f}% below the stock's last close "
                       f"${p.ref_close:.2f} of {p.ref_close_date or 'unknown date'} (band {band:.1f}%)")
    else:
        bad.append("no reference close for the stock")
    return bad


def price_band(cfg: LiveConfig, ref_date: Optional[str], now: datetime) -> float:
    """Allowed gap between the quoted token price and the stock's last close, in percent.

    The close is the independent reference, but it ages: Friday's close is three days old on Monday and stocks move.
    Base band for a close up to one day old, plus `band_per_stale_day_pct` for each extra day, capped at `max_band_pct`.
    """
    try:
        age = (now.astimezone(timezone.utc).date() - datetime.fromisoformat(ref_date).date()).days if ref_date else 99
    except ValueError:
        age = 99
    return min(cfg.max_band_pct, cfg.price_band_pct + cfg.band_per_stale_day_pct * max(0, age - 1))


def check_quote(q: dict, p: Proposal, cfg: LiveConfig, now: Optional[datetime] = None) -> list[str]:
    """Sanity checks on a quote before any money moves."""
    bad: list[str] = []
    try:
        a_in, a_out_usd, a_out = float(q["amountInUsd"]), float(q["amountOutUsd"]), float(q["amountOutFormatted"])
    except (KeyError, TypeError, ValueError):
        return ["quote is missing amounts"]
    if a_out <= 0 or a_in <= 0:
        return ["quote has non-positive amounts"]
    if abs(a_in - p.usd) > max(0.05, p.usd * 0.02):
        bad.append(f"quote is for ${a_in:.2f}, not the approved ${p.usd:.2f}")
    cost = (a_in - a_out_usd) / a_in * 100
    if cost > cfg.max_cost_pct:
        bad.append(f"quoted cost {cost:.2f}% is above the cap {cfg.max_cost_pct:.2f}%")
    if cfg.price_band_pct <= 0:
        return bad                                    # owner 2026-11-11: no code band; the agent judged the price itself
    if p.ref_close:
        implied = a_in / a_out
        off = abs(implied / p.ref_close - 1) * 100
        band = price_band(cfg, p.ref_close_date, now or datetime.now(timezone.utc))
        if off > band:
            bad.append(f"quoted price ${implied:.2f} is {off:.1f}% away from the stock's last close ${p.ref_close:.2f} "
                       f"of {p.ref_close_date or 'unknown date'} (band {band:.1f}%)")
    else:
        bad.append("no reference close for the stock")
    return bad


# ------------------------------------------------------------------ NEAR mainnet access
def rpc_view(http: httpx.Client, rpc: str, contract: str, method: str, args: dict) -> Any:
    body = {"jsonrpc": "2.0", "id": "fs", "method": "query",
            "params": {"request_type": "call_function", "finality": "final", "account_id": contract, "method_name": method,
                       "args_base64": base64.b64encode(json.dumps(args).encode()).decode()}}
    payload = http.post(rpc, json=body, timeout=30).json()
    if "error" in payload or "result" not in payload or "result" not in payload["result"]:
        raise RuntimeError(f"NEAR RPC error calling {method}: {str(payload.get('error', payload))[:160]}")
    return json.loads(bytes(payload["result"]["result"]).decode() or "null")


def read_balances(http: httpx.Client, cfg: LiveConfig, account: str, tokens: list[dict]) -> dict:
    """Read-only balances of the fund account: NEAR, USDC, and tokens held inside NEAR Intents. No key needed."""
    out: dict = {"account": account, "near": None, "usdc": None, "holdings": [], "errors": []}
    try:
        body = {"jsonrpc": "2.0", "id": "fs", "method": "query",
                "params": {"request_type": "view_account", "finality": "final", "account_id": account}}
        res = http.post(cfg.rpc, json=body, timeout=30).json()
        if "result" in res:
            out["near"] = round(int(res["result"].get("amount", "0")) / 1e24, 4)
        else:
            err = str(res.get("error") or "")
            out["errors"].append("account not found on mainnet" if "does not exist" in err or "UNKNOWN_ACCOUNT" in err
                                 else f"the NEAR server did not answer the balance request ({err[:80] or 'no result'})")
            return out
    except (httpx.HTTPError, ValueError) as exc:
        out["errors"].append(f"NEAR balance: {type(exc).__name__}")
        return out
    try:
        raw = rpc_view(http, cfg.rpc, cfg.usdc_contract, "ft_balance_of", {"account_id": account})
        out["usdc"] = round(int(raw or 0) / 10 ** cfg.usdc_decimals, 4)
    except Exception as exc:  # noqa: BLE001
        out["errors"].append(f"USDC balance: {str(exc)[:80]}")
    if tokens:
        try:
            ids = [t["asset_id"] for t in tokens]
            raw = rpc_view(http, cfg.rpc, cfg.intents_contract, "mt_batch_balance_of", {"account_id": account, "token_ids": ids})
            for t, amount in zip(tokens, raw or []):
                qty = int(amount or 0) / 10 ** int(t.get("decimals", 18))
                if qty > 0:
                    out["holdings"].append({"symbol": t["symbol"], "ticker": t["ticker"], "quantity": round(qty, 8),
                                            "value_usd": round(qty * t["price"], 2) if t.get("price") else None})
        except Exception as exc:  # noqa: BLE001
            out["errors"].append(f"NEAR Intents holdings: {str(exc)[:80]}")
    return out


class MainnetSigner:
    """Signs the two calls a buy needs, on NEAR MAINNET, with the dedicated fund account's key (py-near)."""

    def __init__(self, account_id: str, private_key: str, rpc: str) -> None:
        if not account_id.endswith(".near") and len(account_id) != 64:
            raise ValueError("FUND_MAINNET_ACCOUNT_ID must be a mainnet account (name.near or a 64-character implicit account)")
        if not private_key.startswith("ed25519:"):
            raise ValueError("FUND_MAINNET_PRIVATE_KEY must look like 'ed25519:...'")
        self.account_id, self._key, self.rpc = account_id, private_key, rpc

    def call(self, contract: str, method: str, args: dict, gas: int, deposit: int) -> str:
        from py_near.account import Account   # imported lazily: only needed for real sends

        async def go() -> str:
            acc = Account(self.account_id, self._key, rpc_addr=self.rpc)
            await acc.startup()
            try:
                res = await acc.function_call(contract, method, args, gas=gas, amount=deposit)
            finally:
                await acc.shutdown()
            status = getattr(res, "status", None)
            if isinstance(status, dict) and "Failure" in status:
                raise RuntimeError(f"transaction failed on chain: {str(status['Failure'])[:200]}")
            tx = getattr(getattr(res, "transaction", None), "hash", None) or getattr(res, "transaction_hash", None)
            if isinstance(res, str):
                tx = res
            return str(tx or "")

        return self._run(go)

    def transfer(self, receiver: str, amount_yocto: int) -> str:
        """Plain NEAR transfer (how a NEAR-paid 1Click swap is funded)."""
        from py_near.account import Account

        async def go() -> str:
            acc = Account(self.account_id, self._key, rpc_addr=self.rpc)
            await acc.startup()
            try:
                res = await acc.send_money(receiver, amount_yocto)
            finally:
                await acc.shutdown()
            status = getattr(res, "status", None)
            if isinstance(status, dict) and "Failure" in status:
                raise RuntimeError(f"transfer failed on chain: {str(status['Failure'])[:200]}")
            tx = getattr(getattr(res, "transaction", None), "hash", None) or getattr(res, "transaction_hash", None)
            if isinstance(res, str):
                tx = res
            return str(tx or "")

        return self._run(go)

    def _run(self, go) -> str:  # noqa: ANN001
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        try:
            return asyncio.run(go())
        except Exception as exc:  # noqa: BLE001  (never let the key into a message)
            raise RuntimeError(str(exc)[:300].replace(self._key, "***")) from None


# ------------------------------------------------------------------ 1Click (real quotes and status)
class OneClickLive:
    def __init__(self, api: str, *, http: Optional[httpx.Client] = None, api_key: Optional[str] = None) -> None:
        self.api = api.rstrip("/")
        self._http = http or httpx.Client(timeout=40.0)
        self._headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def quote(self, *, dry: bool, pay_asset: str, dest_asset: str, amount_units: int, account: str, slippage_bps: int,
              deadline: datetime, deposit_type: str = "ORIGIN_CHAIN") -> dict:
        """deposit_type INTENTS = paid from a balance already inside NEAR Intents (needed to quote a SALE of a bridged stock
        token: an ORIGIN_CHAIN quote refuses it with "refundTo is not valid", seen 2026-11-10)."""
        body = {"dry": dry, "swapType": "EXACT_INPUT", "slippageTolerance": slippage_bps, "originAsset": pay_asset,
                "depositType": deposit_type, "destinationAsset": dest_asset, "amount": str(amount_units),
                "refundTo": account, "refundType": deposit_type, "recipient": account, "recipientType": "INTENTS",
                "deadline": deadline.strftime("%Y-%m-%dT%H:%M:%S.000Z")}
        r = self._http.post(f"{self.api}/v0/quote", json=body, headers=self._headers)
        try:
            data = r.json()
        except ValueError:
            raise RuntimeError(f"1Click quote: HTTP {r.status_code}, not JSON") from None
        q = data.get("quote") if isinstance(data, dict) else None
        if r.status_code >= 400 or not q:
            raise RuntimeError(f"1Click quote refused: {str((data or {}).get('message') or r.status_code)[:200]}")
        keep = ("amountIn", "amountInFormatted", "amountInUsd", "amountOut", "amountOutFormatted", "amountOutUsd", "minAmountOut",
                "timeEstimate", "depositAddress", "deadline", "timeWhenInactive")
        out = {k: q.get(k) for k in keep if q.get(k) is not None}
        out["correlationId"] = data.get("correlationId")
        out["quotedAt"] = datetime.now(timezone.utc).isoformat()
        out["dry"] = dry
        return out

    def price_usd(self, asset_id: str) -> float:
        """USD price of an asset from the public 1Click token list (used to size a NEAR payment for a USD amount)."""
        r = self._http.get(f"{self.api}/v0/tokens", headers=self._headers)
        for t in r.json() if r.status_code == 200 else []:
            if t.get("assetId") == asset_id and t.get("price"):
                return float(t["price"])
        raise RuntimeError(f"no price for {asset_id} in the 1Click token list")

    def submit_deposit(self, deposit_address: str, tx_hash: str) -> None:
        try:
            self._http.post(f"{self.api}/v0/deposit/submit", json={"txHash": tx_hash, "depositAddress": deposit_address}, headers=self._headers)
        except httpx.HTTPError:
            pass          # optional speed-up; the swap starts on receipt of the deposit anyway

    def status(self, deposit_address: str) -> dict:
        r = self._http.get(f"{self.api}/v0/status", params={"depositAddress": deposit_address}, headers=self._headers)
        data = r.json() if r.status_code < 500 else {}
        return data if isinstance(data, dict) else {}


# ------------------------------------------------------------------ executor
class Executor:
    def __init__(self, cfg: LiveConfig, state_path: Path, oneclick: OneClickLive, *, pay_asset: str,
                 signer: Optional[Any] = None, http: Optional[httpx.Client] = None, kill_file: Optional[Path] = None,
                 now: Callable[[], datetime] = lambda: datetime.now(timezone.utc), sleep: Callable[[float], None] = time.sleep) -> None:
        self.cfg, self.state_path, self.oneclick, self.pay_asset = cfg, state_path, oneclick, pay_asset
        self.signer, self._http = signer, http or httpx.Client(timeout=30.0)
        self.kill_file = kill_file or state_path.with_name("STOP")
        self._now, self._sleep = now, sleep

    def kill_switch(self) -> bool:
        return self.kill_file.exists()

    @property
    def pays_near(self) -> bool:
        return self.cfg.pay_with == "near"

    def pay_units(self, usd: float) -> int:
        """Smallest units of the pay asset worth `usd` (NEAR: sized from the 1Click price; USDC: 1:1)."""
        if self.pays_near:
            return int(usd / self.oneclick.price_usd(self.cfg.near_asset_id) * 10 ** 24)
        return int(round(usd * 10 ** self.cfg.usdc_decimals))

    def dry_quote(self, asset_id: str, usd: float, account: str) -> dict:
        return self.oneclick.quote(dry=True, pay_asset=self.pay_asset, dest_asset=asset_id, amount_units=self.pay_units(usd), account=account,
                                   slippage_bps=self.cfg.slippage_bps, deadline=self._now() + timedelta(minutes=10))

    # ---- shadow: a real dry quote, nothing sent
    def shadow_fill(self, state: TradingState, p: Proposal, account: str = "intents.near", decimals: int = 18) -> Proposal:
        if p.mode != "shadow" or p.status != "proposed":
            raise RuntimeError("only a fresh shadow proposal can be shadow-filled")
        if p.side == "sell":
            return self._shadow_sell(state, p, account, decimals)
        try:
            q = self.dry_quote(p.asset_id, p.usd, account)
        except (RuntimeError, httpx.HTTPError) as exc:
            p.error = str(exc)[:200]
            p.mark("failed", "shadow: no quote (" + p.error + ")", self._now())
            p.sha256 = fingerprint(p)
            save_state(state, self.state_path)
            return p
        problems = [m for m in check_quote(q, p, self.cfg, self._now()) if "cost" not in m]   # shadow: no cost cap (owner's choice)
        p.quote = q
        if problems:
            p.error = "; ".join(problems)
            p.mark("failed", "shadow: " + p.error, self._now())
        else:
            p.mark("shadow_filled", f"would receive {q.get('amountOutFormatted')} {p.symbol} for ${p.usd:.2f} (nothing was sent)", self._now())
        p.sha256 = fingerprint(p)
        save_state(state, self.state_path)
        return p

    def _shadow_sell(self, state: TradingState, p: Proposal, account: str, decimals: int) -> Proposal:
        units = int((p.quantity or 0) * 10 ** decimals)
        problems: list[str] = []
        try:
            if units <= 0:
                raise RuntimeError("nothing to sell")
            q = self.oneclick.quote(dry=True, pay_asset=p.asset_id, dest_asset=self.cfg.near_asset_id, amount_units=units, account=account,
                                    slippage_bps=self.cfg.slippage_bps, deadline=self._now() + timedelta(minutes=10), deposit_type="INTENTS")
            problems = [m for m in check_sell_quote(q, p, self.cfg, self._now()) if "cost" not in m]
        except (RuntimeError, httpx.HTTPError) as exc:
            q, problems = None, [str(exc)[:200]]
        p.quote = q
        if problems:
            p.error = "; ".join(problems)
            p.mark("failed", "shadow sale: " + p.error, self._now())
        else:
            p.mark("shadow_filled", f"would sell {q.get('amountInFormatted')} {p.symbol} for about ${float(q.get('amountOutUsd') or 0):.2f} of NEAR "
                                    "(nothing was sent)", self._now())
        p.sha256 = fingerprint(p)
        save_state(state, self.state_path)
        return p

    # ---- live
    def execute(self, state: TradingState, p: Proposal) -> Proposal:
        """Run ONE approved live buy. Raises RuntimeError (and leaves funds untouched) if any check fails before sending."""
        if p.mode != "live":
            raise RuntimeError("not a live proposal")
        if p.status != "approved":
            raise RuntimeError(f"proposal is '{p.status}', not 'approved' (a proposal is never sent twice; use resume to re-check a deposit)")
        if p.side == "sell":
            raise RuntimeError("sales run only on the private signed route (live.route: confidential); the stocks are in the private balance")
        if self.signer is None:
            raise RuntimeError("FUND_MAINNET_ACCOUNT_ID / FUND_MAINNET_PRIVATE_KEY are not set")
        blocked = check_limits(state, p, self.cfg, kill_switch=self.kill_switch(), now=self._now())
        if blocked:
            raise RuntimeError("blocked by limits: " + "; ".join(blocked))
        units = self.pay_units(p.usd)
        if self.pays_near:
            body = {"jsonrpc": "2.0", "id": "fs", "method": "query",
                    "params": {"request_type": "view_account", "finality": "final", "account_id": self.signer.account_id}}
            have = int(((self._http.post(self.cfg.rpc, json=body, timeout=30).json().get("result") or {}).get("amount")) or 0)
            need = units + int(self.cfg.near_reserve * 10 ** 24)
            if have < need:
                raise RuntimeError(f"the account holds {have / 1e24:.3f} NEAR, less than the {need / 1e24:.3f} NEAR needed "
                                   f"(${p.usd:.2f} of NEAR plus {self.cfg.near_reserve} NEAR kept for fees)")
        else:
            have = int(rpc_view(self._http, self.cfg.rpc, self.cfg.usdc_contract, "ft_balance_of", {"account_id": self.signer.account_id}) or 0)
            if have < units:
                raise RuntimeError(f"the account holds {have / 10 ** self.cfg.usdc_decimals:.2f} USDC, less than the ${p.usd:.2f} needed")
        q = self.oneclick.quote(dry=False, pay_asset=self.pay_asset, dest_asset=p.asset_id, amount_units=units, account=self.signer.account_id,
                                slippage_bps=self.cfg.slippage_bps, deadline=self._now() + timedelta(minutes=self.cfg.deadline_minutes))
        problems = check_quote(q, p, self.cfg, self._now())
        if not q.get("depositAddress"):
            problems.append("quote has no deposit address")
        if str(q.get("amountIn")) != str(units):
            problems.append("quote amountIn differs from the approved amount")
        if problems:
            p.quote = q
            p.error = "; ".join(problems)
            p.mark("failed", "refused before sending: " + p.error, self._now())
            save_state(state, self.state_path)
            raise RuntimeError("refused before sending (nothing was sent): " + p.error)

        # Point of no return: record first, then send exactly once.
        p.quote, p.deposit_address = q, q["depositAddress"]
        coin = "NEAR" if self.pays_near else "USDC"
        p.mark("executing", f"real quote accepted; sending ${p.usd:.2f} of {coin} to the 1Click deposit address", self._now())
        save_state(state, self.state_path)
        if not self.pays_near:
            try:        # preparation: no USDC moves here, so a failure is a clean "failed"
                registered = rpc_view(self._http, self.cfg.rpc, self.cfg.usdc_contract, "storage_balance_of", {"account_id": p.deposit_address})
                if not registered:
                    self.signer.call(self.cfg.usdc_contract, "storage_deposit", {"account_id": p.deposit_address, "registration_only": True},
                                     30 * 10 ** 12, 1_250_000_000_000_000_000_000)
            except Exception as exc:  # noqa: BLE001
                p.error = f"could not prepare the deposit address: {str(exc)[:240]}"
                p.mark("failed", "no USDC was sent: " + p.error, self._now())
                save_state(state, self.state_path)
                raise RuntimeError(p.error + " (no USDC was sent)") from None
        try:
            if self.pays_near:
                tx = self.signer.transfer(p.deposit_address, units)
            else:
                tx = self.signer.call(self.cfg.usdc_contract, "ft_transfer", {"receiver_id": p.deposit_address, "amount": str(units)}, 30 * 10 ** 12, 1)
        except Exception as exc:  # noqa: BLE001
            p.error = f"send step raised: {str(exc)[:240]}"
            p.mark("deposited", "the transfer may or may not have gone through; check with resume before anything else", self._now())
            save_state(state, self.state_path)
            raise RuntimeError(p.error + " (status kept as 'deposited': run resume, never approve again)") from None
        p.deposit_tx = tx or None
        p.mark("deposited", f"{coin} sent, tx {tx}", self._now())
        save_state(state, self.state_path)
        if tx:
            self.oneclick.submit_deposit(p.deposit_address, tx)
        return self.poll(state, p)

    def poll(self, state: TradingState, p: Proposal) -> Proposal:
        """Wait for the swap of an already-made deposit to finish (also used by resume). Sends nothing."""
        if p.status != "deposited" or not p.deposit_address:
            raise RuntimeError("nothing to poll: no deposit was made for this proposal")
        if (p.quote or {}).get("route") == "confidential":
            # Learned on the first real private-route order (2026-11-10): the public status endpoint answers 404 for a
            # private deposit address; the order's progress is only visible inside near.com (or with the owner's session).
            raise RuntimeError("this order went through the PRIVATE route, which the public status check cannot see. "
                               "Check near.com; when the stock is there, record it with:  python scripts\\fund_trade.py confirm "
                               + p.id + "   (or `refunded` if the money came back)")
        waited = 0.0
        last = ""
        while waited <= self.cfg.poll_timeout_seconds:
            try:
                st = self.oneclick.status(p.deposit_address)
            except (httpx.HTTPError, ValueError):
                st = {}
            status = str(st.get("status") or "")
            if status and status != last:
                last = status
                p.history.append(Event(at=self._now(), status=p.status, note=f"1Click status: {status}"))
            if status in ("SUCCESS", "REFUNDED", "FAILED"):
                details = st.get("swapDetails") or {}
                p.result = {"status": status, **{k: details.get(k) for k in ("amountInFormatted", "amountOutFormatted", "amountOutUsd",
                                                                           "refundedAmountFormatted", "refundReason") if details.get(k) is not None}}
                p.mark({"SUCCESS": "success", "REFUNDED": "refunded", "FAILED": "failed"}[status],
                       f"final 1Click status {status}", self._now())
                p.sha256 = fingerprint(p)
                save_state(state, self.state_path)
                return p
            self._sleep(self.cfg.poll_seconds)
            waited += self.cfg.poll_seconds
        save_state(state, self.state_path)
        raise RuntimeError("the swap did not finish within the polling window; funds are with 1Click or being refunded. Run resume later.")


def performance(state: TradingState, prices: dict[str, tuple[float, str, str]], shadow_budget: float) -> dict:
    """How the real-money fund and the shadow fund are doing, in PERCENT only (owner 2026-11-11: the amounts are small).

    `prices`: ticker -> (price, when, source). The live NEAR Intents price of the tokenized stock comes first (the same
    price near.com shows); the stock's latest daily close only when that is missing (owner 2026-11-11: the close was stale
    while the market was open). Real money: (value of holdings + money back from sales) vs money put in. Shadow: the same
    on the money it placed. Report purchases are not counted (they are the agent economy). None when a holding is unpriced."""
    def pct(value: float, cost: float) -> Optional[float]:
        return round((value / cost - 1) * 100, 2) if cost > 0 else None

    live_rows = state.live_holdings()
    priced = [h for h in live_rows if h["ticker"] in prices]
    put_in = sum(p.usd for p in state.proposals if p.mode == "live" and p.status == "success" and p.side != "sell")
    live_value = sum(h["quantity"] * prices[h["ticker"]][0] for h in priced) + state.proceeds("live")
    live_ok = len(priced) == len(live_rows) and put_in > 0
    pf = shadow_portfolio(state, {f"{t}on": v[0] for t, v in prices.items()}, shadow_budget)
    sh_cost = sum(r["cost_usd"] for r in pf["positions"])
    sh_ok = bool(pf["positions"]) and all(r["value_usd"] is not None for r in pf["positions"])
    sh_value = sum(r["value_usd"] for r in pf["positions"] if r["value_usd"] is not None) + pf["realized_usd"]
    used = [prices[h["ticker"]] for h in priced] + [prices[r["ticker"]] for r in pf["positions"] if r["ticker"] in prices]
    return {"live_pct": pct(live_value, put_in) if live_ok else None,
            "shadow_pct": pct(sh_value, sh_cost) if sh_ok else None,
            "shadow_positions": {r["symbol"]: r["change_pct"] for r in pf["positions"]},
            "live_positions": {h["symbol"]: pct(h["quantity"] * prices[h["ticker"]][0], h["cost_usd"]) for h in priced},
            "priced_at": max((u[1] for u in used), default=None),
            "basis": "; ".join(sorted({u[2] for u in used})) or "no price",
            "note": "report purchases not included"}


def shadow_portfolio(state: TradingState, prices: dict[str, float], budget: float) -> dict:
    """Pretend positions built from shadow fills: quantity and cost per token, valued at the given token prices.
    A shadow sale removes tokens at their average cost and adds what the quote paid to the cash."""
    rows: dict[str, dict] = {}
    proceeds = realized = 0.0
    for p in sorted(state.proposals, key=lambda x: x.created_at):
        if p.mode != "shadow" or p.status != "shadow_filled" or not p.quote:
            continue
        if p.side == "sell":
            r = rows.get(p.symbol)
            sold, got = _num(p.quote.get("amountInFormatted")), _usd_out(p)
            if r and r["quantity"] > 0:
                share = min(1.0, sold / r["quantity"])
                realized += got - r["cost_usd"] * share
                r["cost_usd"] *= 1 - share
                r["quantity"] = max(0.0, r["quantity"] - sold)
            proceeds += got
            continue
        r = rows.setdefault(p.symbol, {"symbol": p.symbol, "ticker": p.ticker, "topic": p.topic, "asset_id": p.asset_id, "quantity": 0.0,
                                       "cost_usd": 0.0, "orders": 0, "first_bought": p.created_at.isoformat()})
        r["quantity"] += _num(p.quote.get("amountOutFormatted"))
        r["cost_usd"] += p.usd
        r["orders"] += 1
    spent_total = sum(p.usd for p in state.proposals if p.mode == "shadow" and p.status == "shadow_filled" and p.side == "buy")
    out, invested, value = [], 0.0, 0.0
    for r in [r for r in rows.values() if r["quantity"] > 1e-9]:
        px = prices.get(r["symbol"])
        r["quantity"] = round(r["quantity"], 6)
        r["cost_usd"] = round(r["cost_usd"], 2)
        r["value_usd"] = round(r["quantity"] * px, 2) if px else None
        r["change_pct"] = round((r["value_usd"] / r["cost_usd"] - 1) * 100, 2) if px and r["cost_usd"] else None
        invested += r["cost_usd"]
        value += r["value_usd"] if r["value_usd"] is not None else r["cost_usd"]
        out.append(r)
    out.sort(key=lambda r: -r["cost_usd"])
    cash = round(budget - spent_total + proceeds, 2)
    return {"budget_usd": budget, "invested_usd": round(invested, 2), "cash_usd": cash, "value_usd": round(value + cash, 2),
            "realized_usd": round(realized, 2), "positions": out}


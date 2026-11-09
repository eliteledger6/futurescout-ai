"""Stage 3: small REAL trades through NEAR Intents 1Click, with hard limits (owner go-ahead 2026-11-09).

Owner's written scope: a dedicated mainnet account funded with about 5 USD of USDC + 0.5 NEAR; a trading agent on a
strong model proposes; the owner approves each trade on this machine; the first trade proves the path works; shadow
mode (real quotes, nothing sent) continues with a larger pretend budget. See STAGE3_PLAN.md.

Safety, all enforced HERE in code and never left to a model:
  * `trading_enabled` is false by default (config/funds.yaml -> live), and a kill-switch file stops everything;
  * only BUYS of tokens on the allowlist built from the price-checked Ondo routes; sells are not implemented;
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
from typing import Any, Callable, Optional

import httpx
from pydantic import BaseModel, Field

DISCLAIMER = ("Real-money test with a very small budget, approved trade by trade by the owner. Tokenized stocks are "
              "issued by Ondo and are not the shares themselves. Not investment advice.")
FINAL = {"success", "refunded", "failed", "rejected", "shadow_filled", "hold"}
SPENT = {"executing", "deposited", "success"}          # statuses that count against the caps


# ------------------------------------------------------------------ config
class LiveConfig(BaseModel):
    trading_enabled: bool = False
    rpc: str = "https://rpc.mainnet.near.org"
    usdc_contract: str = "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1"
    usdc_decimals: int = 6
    pay_with: str = "near"               # "near" (native NEAR, owner's choice 2026-11-09) or "usdc"
    near_asset_id: str = "nep141:wrap.near"   # how 1Click names NEAR; a plain NEAR transfer to the deposit address pays it
    near_reserve: float = 0.05           # NEAR always left in the account for fees
    intents_contract: str = "intents.near"
    max_trade_usd: float = 5.0
    max_day_usd: float = 5.0
    max_total_usd: float = 5.0
    min_trade_usd: float = 1.0
    price_band_pct: float = 3.0          # quoted token price vs the stock's last close (close up to 1 day old)
    band_per_stale_day_pct: float = 1.5  # extra band per further day of age of that close
    max_band_pct: float = 8.0
    max_cost_pct: float = 2.0            # (in - out) / in of the real quote
    slippage_bps: int = 100
    deadline_minutes: int = 30
    poll_seconds: float = 5.0
    poll_timeout_seconds: float = 600.0
    shadow_budget_usd: float = 1000.0
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
    side: str = "buy"                          # buy | hold (the agent proposed to do nothing)
    topic: str
    ticker: str
    symbol: str                                # token symbol, e.g. INTCon
    asset_id: str
    usd: float
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
    chain: Optional[dict] = None               # NEAR testnet record of that fingerprint

    def mark(self, status: str, note: str = "", now: Optional[datetime] = None) -> None:
        self.status = status
        self.history.append(Event(at=now or datetime.now(timezone.utc), status=status, note=note[:300]))


class TradingState(BaseModel):
    proposals: list[Proposal] = Field(default_factory=list)
    updated_at: Optional[datetime] = None

    def get(self, pid: str) -> Optional[Proposal]:
        return next((p for p in self.proposals if p.id == pid or p.id.startswith(pid)), None)

    def spent(self, mode: str = "live", day: Optional[str] = None) -> float:
        tot = 0.0
        for p in self.proposals:
            if p.mode != mode or p.status not in SPENT:
                continue
            if day and not any(e.status == "executing" and e.at.astimezone(timezone.utc).date().isoformat() == day for e in p.history):
                continue
            tot += p.usd
        return round(tot, 2)


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
    data = p.model_dump(mode="json", exclude={"sha256", "chain"})
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# ------------------------------------------------------------------ limits (pure code)
def check_limits(state: TradingState, p: Proposal, cfg: LiveConfig, *, kill_switch: bool, now: datetime) -> list[str]:
    """Every reason this proposal may NOT be executed live right now. Empty list = allowed."""
    bad: list[str] = []
    if kill_switch:
        bad.append("kill switch is on (STOP file present)")
    if not cfg.trading_enabled:
        bad.append("trading_enabled is false in config/funds.yaml")
    if p.side != "buy":
        bad.append("only buys are implemented")
    if p.usd < cfg.min_trade_usd:
        bad.append(f"amount ${p.usd:.2f} is below the minimum ${cfg.min_trade_usd:.2f}")
    if p.usd > cfg.max_trade_usd + 1e-9:
        bad.append(f"amount ${p.usd:.2f} is above the per-trade cap ${cfg.max_trade_usd:.2f}")
    day = now.astimezone(timezone.utc).date().isoformat()
    if state.spent("live", day) + p.usd > cfg.max_day_usd + 1e-9:
        bad.append(f"daily cap ${cfg.max_day_usd:.2f} would be exceeded (already ${state.spent('live', day):.2f} today)")
    if state.spent("live") + p.usd > cfg.max_total_usd + 1e-9:
        bad.append(f"total cap ${cfg.max_total_usd:.2f} would be exceeded (already ${state.spent('live'):.2f} in total)")
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
            out["errors"].append("account not found on mainnet")
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
            res = await acc.function_call(contract, method, args, gas=gas, amount=deposit)
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
            res = await acc.send_money(receiver, amount_yocto)
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
              deadline: datetime) -> dict:
        body = {"dry": dry, "swapType": "EXACT_INPUT", "slippageTolerance": slippage_bps, "originAsset": pay_asset,
                "depositType": "ORIGIN_CHAIN", "destinationAsset": dest_asset, "amount": str(amount_units),
                "refundTo": account, "refundType": "ORIGIN_CHAIN", "recipient": account, "recipientType": "INTENTS",
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
    def shadow_fill(self, state: TradingState, p: Proposal, account: str = "intents.near") -> Proposal:
        if p.mode != "shadow" or p.status != "proposed":
            raise RuntimeError("only a fresh shadow proposal can be shadow-filled")
        try:
            q = self.dry_quote(p.asset_id, p.usd, account)
        except (RuntimeError, httpx.HTTPError) as exc:
            p.error = str(exc)[:200]
            p.mark("failed", "shadow: no quote (" + p.error + ")", self._now())
            p.sha256 = fingerprint(p)
            save_state(state, self.state_path)
            return p
        problems = check_quote(q, p, self.cfg, self._now())
        p.quote = q
        if problems:
            p.error = "; ".join(problems)
            p.mark("failed", "shadow: " + p.error, self._now())
        else:
            p.mark("shadow_filled", f"would receive {q.get('amountOutFormatted')} {p.symbol} for ${p.usd:.2f} (nothing was sent)", self._now())
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

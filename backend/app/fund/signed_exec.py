"""Signed-order execution on the PRIVATE route (Confidential Intents): the way near.com itself trades.

BUILT 2026-11-09 AND SWITCHED OFF. It can only run when ALL of these hold:
  * `live.route: confidential` and `live.signed_route_enabled: true` in config/funds.yaml (false by default);
  * `live.trading_enabled: true`, the kill switch is off, and every cap in app/fund/live.py passes;
  * the owner approves that one proposal in their terminal (scripts/fund_trade.py approve, typed confirmation).

Why: two real trades paid from the WALLET to a deposit address stayed "PROCESSING" for hours, while swaps placed
from the balance inside near.com were instant. The owner's login run then showed that the near.com balance is the
account's Confidential Intents balance and that the wallet key can open a session and get quotes there.

One buy, step by step (the first three move nothing):
  1. login: sign an EMPTY order -> short session token;
  2. check the private balance covers the amount;
  3. real quote on the private route -> a deposit address; then ask the service for the order it wants signed;
  4. VERIFY that order before signing: it must be exactly one transfer of exactly the approved amount of the pay
     token (plain id, or the private balance's `imt:<bridge>:<id>` form of it), from this account, to exactly the quote's deposit address, addressed to an allowed verifier, with a
     well-formed nonce and a future deadline. Anything else: refuse, nothing is signed;
  5. save the proposal as "executing", sign the order (NEP-413) and submit it ONCE; an unclear submit error is
     recorded as "deposited" and never retried (resume only polls);
  6. the public status endpoint answers 404 for private-route deposit addresses, so the code instead watches the PRIVATE
     balance with the same session (2026-11-10): when the bought token (or, for a sale, the NEAR) arrives, the order is
     marked success with the amounts seen; if nothing arrives in time it stays "deposited" for the owner's `confirm`.

A SALE (owner's written yes 2026-11-10; `live.sells_enabled`) is the same flow in the other direction: the stock token in the
private balance is paid in, NEAR comes back. The order check is identical (one transfer of exactly the approved amount of
that token to the quote's deposit address), and the quote must pass `check_sell_quote` (cost cap; price not far below the
stock's last close).
The first real run of steps 3-6 is the integration test: generating and submitting an order on the private route has
not been exercised, so the checks in step 4 are deliberately strict and report what they saw.
"""

from __future__ import annotations

import base64
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

import httpx

from app.fund.intents_signed import NONCE_MAGIC, SignedIntents, sign_nep413
from app.fund.live import (Executor, LiveConfig, OneClickLive, Proposal, TradingState, check_limits, check_quote, check_sell_quote,
                           fingerprint, save_state)

ROUTE = "CONFIDENTIAL_INTENTS"


def verify_order(order: dict, *, account: str, deposit_address: str, pay_asset: str, units: int,
                 allowed_recipients: list[str], now: datetime) -> list[str]:
    """Every reason NOT to sign this generated order. Empty list = it does exactly what was approved."""
    bad: list[str] = []
    if not isinstance(order, dict) or order.get("standard") != "nep413":
        return [f"unexpected order standard {order.get('standard') if isinstance(order, dict) else type(order).__name__!r}"]
    payload = order.get("payload") or {}
    extra = set(payload) - {"message", "nonce", "recipient", "callbackUrl"}
    if extra:
        bad.append(f"unexpected payload fields {sorted(extra)}")
    if payload.get("callbackUrl"):
        bad.append("the order carries a callback URL")
    if payload.get("recipient") not in allowed_recipients:
        bad.append(f"the order is addressed to {payload.get('recipient')!r}, not one of {allowed_recipients}")
    try:
        nonce = base64.b64decode(payload.get("nonce") or "", validate=True)
    except (ValueError, TypeError):
        nonce = b""
    if len(nonce) != 32 or nonce[:4] != NONCE_MAGIC:
        bad.append("the nonce is not a 32-byte versioned nonce")
    try:
        msg = json.loads(payload.get("message") or "")
    except ValueError:
        return bad + ["the order message is not JSON"]
    if not isinstance(msg, dict):
        return bad + ["the order message is not an object"]
    unknown = set(msg) - {"deadline", "intents", "signer_id", "verifying_contract", "nonce"}
    if unknown:
        bad.append(f"unexpected message fields {sorted(unknown)}")
    if msg.get("signer_id") != account:
        bad.append(f"the signer is {msg.get('signer_id')!r}, not {account!r}")
    intents = msg.get("intents")
    if not isinstance(intents, list) or len(intents) != 1:
        bad.append(f"the order has {len(intents) if isinstance(intents, list) else 'no'} actions; exactly one transfer is allowed")
    else:
        it = intents[0] if isinstance(intents[0], dict) else {}
        if it.get("intent") != "transfer":
            bad.append(f"the action is {it.get('intent')!r}, not a transfer")
        if set(it) - {"intent", "receiver_id", "tokens", "memo"}:
            bad.append(f"unexpected action fields {sorted(set(it) - {'intent', 'receiver_id', 'tokens', 'memo'})}")
        if it.get("receiver_id") != deposit_address:
            bad.append("the transfer does not go to the quote's deposit address")
        if not _moves_exactly(it.get("tokens"), pay_asset, units):
            bad.append(f"the transfer moves {it.get('tokens')}, not exactly {units} of {pay_asset}")
    try:
        deadline = datetime.fromisoformat(str(msg.get("deadline")).replace("Z", "+00:00"))
        if deadline <= now:
            bad.append("the order deadline has already passed")
    except ValueError:
        bad.append("the order deadline is not a date")
    return bad


def _moves_exactly(tokens: Any, pay_asset: str, units: int) -> bool:
    """One token, exactly `units`. The asset may be the plain id (public balance) or the private balance's form of the
    same asset, `imt:<64-hex bridge id>:<plain id>` (seen in the first real private-route order, 2026-11-10)."""
    if not isinstance(tokens, dict) or len(tokens) != 1:
        return False
    (key, amount), = tokens.items()
    if str(amount) != str(units):
        return False
    return key == pay_asset or re.fullmatch(r"imt:[0-9a-f]{64}:" + re.escape(pay_asset), str(key)) is not None


def submit_signed_order(http: httpx.Client, api: str, api_key: Optional[str], order: dict, private_key: str) -> str:
    """Sign the (already verified) order and submit it. Returns the intent hash. THE ONLY CALL THAT MOVES FUNDS HERE."""
    payload = order["payload"]
    public_key, signature = sign_nep413(private_key, payload["message"], base64.b64decode(payload["nonce"]), payload["recipient"])
    body = {"type": "swap_transfer", "signedData": {"standard": "nep413", "payload": payload, "public_key": public_key, "signature": signature}}
    r = http.post(f"{api.rstrip('/')}/v0/submit-intent", json=body, headers={"X-API-Key": api_key} if api_key else {})
    data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code >= 300 or not data.get("intentHash"):
        raise RuntimeError(f"the service refused the order: {str(data.get('message') or r.status_code)[:200]}")
    return str(data["intentHash"])


def held(balances: list[dict], asset: str) -> int:
    """Available units of `asset` in the private balance (plain id or its `imt:<bridge>:<id>` form)."""
    tot = 0
    for b in balances:
        tid = str(b.get("tokenId") or "")
        if tid == asset or re.fullmatch(r"imt:[0-9a-f]{64}:" + re.escape(asset), tid):
            try:
                tot += int(b.get("available") or 0)
            except (TypeError, ValueError):
                pass
    return tot


_QUOTE_KEYS = ("amountIn", "amountInFormatted", "amountInUsd", "amountOut", "amountOutFormatted", "amountOutUsd", "minAmountOut",
               "timeEstimate", "depositAddress", "deadline", "timeWhenInactive", "correlationId")


class SignedExecutor:
    def __init__(self, cfg: LiveConfig, state_path: Path, api: SignedIntents, oneclick: OneClickLive, *, account: str, private_key: str,
                 salt_reader: Callable[[], str], submitter: Optional[Callable[[dict, str], str]] = None, kill_file: Optional[Path] = None,
                 now: Callable[[], datetime] = lambda: datetime.now(timezone.utc), sleep: Optional[Callable[[float], None]] = None) -> None:
        self.cfg, self.state_path, self.api, self.account, self._key = cfg, state_path, api, account, private_key
        self._salt_reader, self._submit, self._now = salt_reader, submitter, now
        self._sleep = sleep or time.sleep
        kw: dict[str, Any] = {"pay_asset": cfg.near_asset_id, "kill_file": kill_file, "now": now, "sleep": self._sleep}
        self._poller = Executor(cfg, state_path, oneclick, **kw)       # reused for the kill switch and status polling only

    def kill_switch(self) -> bool:
        return self._poller.kill_switch()

    def execute(self, state: TradingState, p: Proposal) -> Proposal:
        cfg = self.cfg
        if p.mode != "live":
            raise RuntimeError("not a live proposal")
        if p.status != "approved":
            raise RuntimeError(f"proposal is '{p.status}', not 'approved' (a proposal is never sent twice; use resume to re-check)")
        blocked = check_limits(state, p, cfg, kill_switch=self.kill_switch(), now=self._now())
        if cfg.route != "confidential":
            blocked.append("live.route is not 'confidential'")
        if not cfg.signed_route_enabled:
            blocked.append("the signed-order route is built but switched off (live.signed_route_enabled is false)")
        if blocked:
            raise RuntimeError("blocked by limits: " + "; ".join(blocked))

        def refuse(why: str) -> RuntimeError:
            p.error = why
            p.mark("failed", "refused before signing: " + why, self._now())
            save_state(state, self.state_path)
            return RuntimeError("refused before signing (nothing was sent): " + why)

        # ---- steps 1-3: nothing moves
        selling = p.side == "sell"
        try:
            session = self.api.login(self.account, self._key, self._salt_reader())
            token = session["accessToken"]
            balances = self.api.balances(token)
            if selling:
                pay, dest = p.asset_id, cfg.near_asset_id
                have = held(balances, pay)
                if have <= 0:
                    raise RuntimeError(f"the private balance holds no {p.symbol}")
                units = have if (p.fraction or 0) >= 0.999 else int(have * (p.fraction or 0))
                if units <= 0:
                    raise RuntimeError(f"{p.fraction} of the {p.symbol} holding is nothing")
            else:
                pay, dest = cfg.near_asset_id, p.asset_id
                price = next((float(t["price"]) for t in self.api.tokens() if t.get("assetId") == cfg.near_asset_id and t.get("price")), None)
                if not price:
                    raise RuntimeError("no NEAR price in the token list")
                units = int(p.usd / price * 10 ** 24)
                have = held(balances, pay)
                if have < units:
                    raise RuntimeError(f"the private balance holds {have / 1e24:.3f} NEAR, less than the {units / 1e24:.3f} NEAR needed for ${p.usd:.2f}")
            before = held(balances, dest)
            q = self.api.quote(route=ROUTE, pay_asset=pay, dest_asset=dest, amount_units=units, account=self.account,
                               dry=False, session_token=token, slippage_bps=cfg.slippage_bps)
            deposit = q.get("depositAddress")
            problems = check_sell_quote(q, p, cfg, self._now()) if selling else check_quote(q, p, cfg, self._now())
            if not deposit:
                problems.append("quote has no deposit address")
            if str(q.get("amountIn")) != str(units):
                problems.append("quote amountIn differs from the approved amount")
            order = self.api.unsigned_order(deposit, self.account) if deposit else {}
            if deposit:
                problems += verify_order(order, account=self.account, deposit_address=deposit, pay_asset=pay, units=units,
                                         allowed_recipients=cfg.order_recipients, now=self._now())
        except (RuntimeError, ValueError, KeyError, httpx.HTTPError) as exc:
            raise refuse(str(exc)[:300]) from None
        if problems:
            p.quote = {k: q.get(k) for k in _QUOTE_KEYS}
            raise refuse("; ".join(problems))

        # ---- step 5: record first, then sign and submit exactly once
        p.quote = {k: q.get(k) for k in _QUOTE_KEYS}
        p.quote["route"] = "confidential"
        p.deposit_address = deposit
        what = (f"a sale of {q.get('amountInFormatted')} {p.symbol} (about ${float(q.get('amountInUsd') or 0):.2f}) for NEAR" if selling
                else f"a transfer of ${p.usd:.2f} of NEAR")
        p.mark("executing", f"order verified; signing {what} from the private balance (the service may take until {q.get('deadline')})", self._now())
        save_state(state, self.state_path)
        try:
            intent_hash = self._submit(order, self._key) if self._submit else None
            if intent_hash is None:
                raise RuntimeError("no submitter configured")
        except Exception as exc:  # noqa: BLE001
            p.error = f"submit step raised: {str(exc)[:240]}".replace(self._key, "***")
            p.mark("deposited", "the order may or may not have been accepted; check with resume before anything else", self._now())
            save_state(state, self.state_path)
            raise RuntimeError(p.error + " (status kept as 'deposited': run resume, never approve again)") from None
        p.deposit_tx = None
        p.mark("deposited", f"signed order submitted, intent {intent_hash}; watching the private balance for the result", self._now())
        save_state(state, self.state_path)
        return self.settle(state, p, token, dest, before)

    def settle(self, state: TradingState, p: Proposal, token: str, dest: str, before: int) -> Proposal:
        """Watch the PRIVATE balance (same session; reads only) until what was bought or sold for arrives. Sends nothing."""
        q = p.quote or {}
        expected = int(q.get("minAmountOut") or q.get("amountOut") or 0)
        waited = 0.0
        rounds = int(self.cfg.poll_timeout_seconds / self.cfg.poll_seconds) if self.cfg.poll_seconds > 0 else 3
        for _ in range(max(1, rounds)):
            self._sleep(self.cfg.poll_seconds)
            waited += self.cfg.poll_seconds
            try:
                got = held(self.api.balances(token), dest) - before
            except (RuntimeError, ValueError, httpx.HTTPError) as exc:
                p.history[-1].note += f" (balance check stopped: {str(exc)[:80]})"
                break
            if got > 0 and (not expected or got >= expected * 0.98):
                ratio = got / int(q.get("amountOut") or got)
                p.result = {"status": "SUCCESS (seen in the private balance)", "amountInFormatted": q.get("amountInFormatted"),
                            "amountOutFormatted": str(round(float(q.get("amountOutFormatted") or 0) * ratio, 12)),
                            "amountOutUsd": str(round(float(q.get("amountOutUsd") or 0) * ratio, 4)), "received_units": str(got)}
                p.mark("success", f"{'NEAR' if p.side == 'sell' else p.symbol} arrived in the private balance after about {waited:.0f}s", self._now())
                p.sha256 = fingerprint(p)
                save_state(state, self.state_path)
                return p
        p.history.append(type(p.history[-1])(at=self._now(), status=p.status,
                                             note=f"nothing arrived within {waited:.0f}s: check near.com, then `fund_trade.py confirm {p.id}` (or `refunded`)"))
        save_state(state, self.state_path)
        return p

"""Pay the report agent out of the trading agent's PRIVATE near.com balance (Confidential Intents), owner 2026-11-10.

Why: the trading agent's money sits in its near.com balance, not in its wallet (the wallet held 0.099 NEAR after the first
two report purchases). A dry quote on 2026-11-10 showed NEAR Intents pays NEAR out of that balance into another account's
wallet (recipientType DESTINATION_CHAIN): 4.3 NEAR in, 4.3 NEAR out, about 10 s.

One payment, step by step (the first three move nothing):
  1. login (signed empty order, as for trades) and check the private balance holds the price;
  2. real quote: NEAR from the private balance -> NEAR to the report agent's wallet; the quote must pay out at least
     98% of the price and take exactly the price in;
  3. the order the service generates is checked like every trade order: exactly one transfer of exactly the price, from
     this account, to the quote's deposit address, addressed to an allowed verifier (verify_order);
  4. the purchase is saved as "sending" BEFORE signing; the order is signed and submitted ONCE;
  5. the code watches the report agent's account until the NEAR (native, or wrapped as wNEAR) arrives, then marks it paid.
Nothing here runs unless economy.enabled, live.signed_route_enabled and live.trading_enabled are all true.
"""

from __future__ import annotations

import base64
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

import httpx

from app.fund.economy import EconomyConfig, EconomyState, Price, Purchase, account_near, near_to_yocto, save_economy
from app.fund.signed_exec import ROUTE, held, verify_order

WNEAR = "nep141:wrap.near"


def wnear_balance(http: httpx.Client, rpc: str, account: str) -> int:
    body = {"jsonrpc": "2.0", "id": "fs-pay", "method": "query",
            "params": {"request_type": "call_function", "finality": "final", "account_id": "wrap.near", "method_name": "ft_balance_of",
                       "args_base64": base64.b64encode(json.dumps({"account_id": account}).encode()).decode()}}
    try:
        return int(json.loads(bytes(http.post(rpc, json=body, timeout=30).json()["result"]["result"]).decode()) or 0)
    except Exception:  # noqa: BLE001
        return 0


def received(read_native: Callable[[], int], read_wnear: Callable[[], int]) -> int:
    return read_native() + read_wnear()


def pay_from_private(*, state: EconomyState, path: Path, price: Price, account: str, private_key: str, cfg: EconomyConfig,
                     api: Any, salt_reader: Callable[[], str], submit: Callable[[dict, str], str], allowed_recipients: list[str],
                     read_seller_total: Callable[[], int], now: Callable[[], datetime], sleep: Callable[[float], None] = time.sleep,
                     poll_seconds: float = 5.0, poll_timeout_seconds: float = 300.0) -> Purchase:
    """Returns the Purchase (paid | sending | failed). Raises RuntimeError, with nothing signed, when a check fails before signing."""
    units = near_to_yocto(price.price_near)
    session = api.login(account, private_key, salt_reader())
    token = session["accessToken"]
    have = held(api.balances(token), WNEAR)
    if have < units:
        raise RuntimeError(f"the near.com balance holds {have / 1e24:.3f} NEAR, less than the {price.price_near:g} NEAR price")
    q = api.quote(route=ROUTE, pay_asset=WNEAR, dest_asset=WNEAR, amount_units=units, account=account, dry=False, session_token=token,
                  recipient=cfg.seller_account, recipient_type="DESTINATION_CHAIN")
    deposit = q.get("depositAddress")
    problems = []
    if not deposit:
        problems.append("quote has no deposit address")
    if str(q.get("amountIn")) != str(units):
        problems.append("quote amountIn differs from the price")
    if int(q.get("minAmountOut") or q.get("amountOut") or 0) < units * 0.98:
        problems.append(f"the report agent would receive less than 98% of the price ({q.get('amountOutFormatted')} NEAR)")
    order = api.unsigned_order(deposit, account) if deposit else {}
    if deposit:
        problems += verify_order(order, account=account, deposit_address=deposit, pay_asset=WNEAR, units=units,
                                 allowed_recipients=allowed_recipients, now=now())
    if problems:
        raise RuntimeError("refused before signing (nothing was sent): " + "; ".join(problems))

    before = read_seller_total()
    p = Purchase(id=uuid.uuid4().hex[:10], run_id=price.run_id, topic=price.topic, price_near=price.price_near, buyer=account,
                 seller=cfg.seller_account, at=now(), note="paid from the near.com balance; saved before signing, never sent twice")
    state.purchases.append(p)
    save_economy(state, path)                                         # point of no return: recorded first
    try:
        intent = submit(order, private_key)
    except Exception as exc:  # noqa: BLE001
        p.note = f"submit step raised ({str(exc)[:160].replace(private_key, '***')}); kept as 'sending': check the report agent's account"
        save_economy(state, path)
        return p
    p.tx_hash = None
    p.note = f"signed order submitted from the near.com balance, intent {intent}; watching the report agent's account"
    save_economy(state, path)
    expected = int(q.get("minAmountOut") or units)
    waited = 0.0
    rounds = int(poll_timeout_seconds / poll_seconds) if poll_seconds > 0 else 3
    for _ in range(max(1, rounds)):
        sleep(poll_seconds)
        waited += poll_seconds
        got = read_seller_total() - before
        if got >= expected * 0.98:
            p.status = "paid"
            p.note = (f"paid {got / 1e24:.4f} NEAR from the near.com balance (intent {intent}); seen arriving in "
                      f"{cfg.seller_account} after about {waited:.0f}s")
            save_economy(state, path)
            return p
    p.note += f"; nothing arrived within {waited:.0f}s: check {cfg.seller_account} on nearblocks"
    save_economy(state, path)
    return p


def seller_total_reader(http: httpx.Client, rpc: str, seller: str) -> Callable[[], int]:
    """Native NEAR plus wNEAR held by the report agent (the payout may arrive as either)."""
    return lambda: account_near(http, rpc, seller)[0] + wnear_balance(http, rpc, seller)


def new_id() -> str:
    return uuid.uuid4().hex[:10]

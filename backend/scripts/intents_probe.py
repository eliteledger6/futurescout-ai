"""Quotes-only probe of the NEAR Intents routes. NOTHING here can move funds: there is no submit step in the code.

  python scripts\\intents_probe.py                 dry quotes on the wallet route and the internal route, per stock and size
  python scripts\\intents_probe.py --order GOOGL   also request a REAL quote on the internal route and print the UNSIGNED
                                                   order the service would want signed (it simply expires if unused)
  python scripts\\intents_probe.py --login         OWNER ONLY. Signs an EMPTY order (the documented ownership proof; it
                                                   moves no tokens) with the fund key from .env to get a short-lived
                                                   session, then shows the private balances and dry quotes on the
                                                   confidential route (the one near.com appears to use)

The session token is kept in memory only and never printed. See app/fund/intents_signed.py for the formats.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.fund import load_fund_config, tradable_tokens  # noqa: E402
from app.fund.intents_signed import SignedIntents  # noqa: E402
from app.fund.live import rpc_view  # noqa: E402
from app.fund.signed_exec import verify_order  # noqa: E402

SIZES = (10, 20, 30)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--order", metavar="TICKER", help="real quote + unsigned order on the internal route for this ticker")
    ap.add_argument("--usd", type=float, default=10.0, help="size for --order")
    ap.add_argument("--login", action="store_true", help="owner only: sign an empty order to read private balances and confidential quotes")
    args = ap.parse_args()
    s, cfg = get_settings(), load_fund_config()
    key = s.oneclick_api_key.get_secret_value().strip() if s.oneclick_api_key else None
    api = SignedIntents(cfg.intents.api, api_key=key or None)
    account = (s.fund_mainnet_account_id or "").strip() or "intents.near"
    toks = api.tokens()
    near = cfg.live.near_asset_id
    px = next((float(t["price"]) for t in toks if t.get("assetId") == near and t.get("price")), None)
    if not px:
        print("could not read the NEAR price from the token list")
        return 1
    cands = tradable_tokens(service.RUNS_DIR / "funds")
    if not cands:
        print("no tradable token in the funds; run scripts\\funds.py first")
        return 1

    def units(usd: float) -> int:
        return int(usd / px * 10 ** 24)

    def table(route: str, token: str | None = None) -> None:
        print(f"\nroute {route}" + ("  (private balance, session login)" if token else ""))
        for c in cands:
            cells = []
            for usd in SIZES:
                try:
                    q = api.quote(route=route, pay_asset=near, dest_asset=c["asset_id"], amount_units=units(usd), account=account, session_token=token)
                    cells.append(f"${usd}: ok, cost {(float(q['amountInUsd']) - float(q['amountOutUsd'])) / float(q['amountInUsd']) * 100:.2f}%")
                except RuntimeError as exc:
                    cells.append(f"${usd}: {str(exc)[:30]}")
            print(f"  {c['symbol']:8} " + " | ".join(cells))

    print(f"account {account} · NEAR ${px:.2f} · dry quotes, nothing is sent")
    table("ORIGIN_CHAIN")
    table("INTENTS")

    if args.order:
        c = next((x for x in cands if x["ticker"].upper() == args.order.upper()), None)
        if not c:
            print(f"\n{args.order} is not on the allowlist")
            return 1
        try:
            q = api.quote(route="INTENTS", pay_asset=near, dest_asset=c["asset_id"], amount_units=units(args.usd), account=account, dry=False)
            order = api.unsigned_order(q["depositAddress"], account)
        except RuntimeError as exc:
            print(f"\nreal quote / order refused: {exc}")
            return 1
        msg = json.loads(order["payload"]["message"])
        print(f"\nUNSIGNED order for ${args.usd:.2f} of {c['symbol']} (internal route). It is not signed and not submitted; it expires unused.")
        print(f"  would pay {q.get('amountInFormatted')} NEAR for {q.get('amountOutFormatted')} {c['symbol']} (estimate {q.get('timeEstimate')} s)")
        print(f"  the order transfers {msg['intents'][0]['tokens']} from {msg['signer_id']} to the swap address {msg['intents'][0]['receiver_id'][:16]}...")
        print(f"  it is valid until {msg['deadline']} and would be signed for {order['payload']['recipient']}")

    if args.login:
        creds = s.fund_mainnet_credentials()
        if not creds:
            print("\nFUND_MAINNET_ACCOUNT_ID / FUND_MAINNET_PRIVATE_KEY are not set in .env")
            return 1
        print(f"\nLOGIN: this signs an EMPTY order for {creds[0]} with the key in .env. It proves ownership and moves no tokens.")
        if input("Type LOGIN to continue (anything else cancels): ").strip() != "LOGIN":
            print("cancelled")
            return 1
        try:
            salt = rpc_view(httpx.Client(timeout=30), cfg.live.rpc, cfg.live.intents_contract, "current_salt", {})
            session = api.login(creds[0], creds[1], str(salt))
        except (RuntimeError, ValueError, httpx.HTTPError) as exc:
            print(f"login failed: {str(exc)[:300]}")
            return 1
        print(f"logged in (session valid about {session.get('expiresIn')} s)")
        try:
            bal = api.balances(session["accessToken"])
            by = {t["assetId"]: t for t in toks}
            print("private balances:" + (" none" if not bal else ""))
            for b in bal:
                t = by.get(b.get("tokenId"), {})
                qty = int(b.get("available", "0")) / 10 ** int(t.get("decimals", 24))
                print(f"  {t.get('symbol', b.get('tokenId'))}: {qty:.6f}" + (f"  (about ${qty * float(t['price']):.2f})" if t.get("price") else ""))
        except RuntimeError as exc:
            print(f"balances refused: {exc}")
        if not key:
            print("\nconfidential-route quotes need a partner API key as well as this login: get a free one at "
                  "https://partners.near-intents.org and put it in .env as ONECLICK_API_KEY, then run this again.")
        else:
            table("CONFIDENTIAL_INTENTS", session["accessToken"])
            if args.order:
                from datetime import datetime, timezone
                c = next((x for x in cands if x["ticker"].upper() == args.order.upper()), None)
                try:
                    q = api.quote(route="CONFIDENTIAL_INTENTS", pay_asset=near, dest_asset=c["asset_id"], amount_units=units(args.usd), account=creds[0],
                                  dry=False, session_token=session["accessToken"])
                    order = api.unsigned_order(q["depositAddress"], creds[0])
                except (RuntimeError, TypeError) as exc:
                    print(f"\nprivate-route real quote / order refused: {exc}")
                    return 1
                msg = json.loads(order["payload"]["message"])
                problems = verify_order(order, account=creds[0], deposit_address=q["depositAddress"], pay_asset=near, units=units(args.usd),
                                        allowed_recipients=cfg.live.order_recipients, now=datetime.now(timezone.utc))
                print(f"\nUNSIGNED private-route order for ${args.usd:.2f} of {c['symbol']}. Not signed, not submitted; it expires unused.")
                print(f"  quote: {q.get('amountInFormatted')} NEAR -> {q.get('amountOutFormatted')} {c['symbol']}, estimate {q.get('timeEstimate')} s, "
                      f"service deadline {q.get('deadline')}")
                print(f"  order: addressed to {order['payload'].get('recipient')}; fields {sorted(order['payload'])}; message fields {sorted(msg)}")
                print(f"  actions: {json.dumps(msg.get('intents'))[:400]}")
                print("  safety check of this order: " + ("PASSES (it is exactly one transfer of the quoted amount to the quote's address)" if not problems
                                                         else "WOULD BE REFUSED: " + "; ".join(problems)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

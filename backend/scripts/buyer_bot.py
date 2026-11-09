"""Demo BUYER bot: a separate agent that pays FUTURESCOUT for a research report (NEAR testnet).

  python scripts\\buyer_bot.py                      pick the hottest radar topic's newest report, pay, download, verify
  python scripts\\buyer_bot.py --report <run id>    buy a specific report
  python scripts\\buyer_bot.py --dry-run            show what it would buy and the price; send nothing

Needs the API running (python scripts\\serve.py) and, in .env, BUYER_TESTNET_ACCOUNT_ID + BUYER_TESTNET_PRIVATE_KEY
(a dedicated testnet account with free testnet NEAR; never the seller's). Flow:
  1. GET /api/market -> listings (free teasers, price, seller account)
  2. choose a report (hottest topic on /api/radar, else newest)
  3. send `price` NEAR to the seller on testnet (native transfer, signed by the buyer key)
  4. POST /api/market/{id}/purchase with the tx hash -> the API verifies the payment on-chain and returns the full report
  5. recompute the report's SHA-256 and compare it with the fingerprint FUTURESCOUT recorded on NEAR
Testnet NEAR has no monetary value. Mainnet accounts are refused.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402

from app.chain.near_record import TESTNET_RPC, check_testnet, report_digest  # noqa: E402
from app.chain.payments import near_to_yocto  # noqa: E402
from app.config import BACKEND_DIR, get_settings, quiet_network_logs  # noqa: E402
from app.schemas.research import ResearchReport  # noqa: E402

API = "http://127.0.0.1:8000"


def pick_report(http: httpx.Client, wanted: str | None, api: str) -> dict:
    market = http.get(f"{api}/api/market").json()
    if not market["enabled"]:
        sys.exit("The marketplace is disabled on the seller side (NEAR_TESTNET_ACCOUNT_ID not set).")
    reports = market["reports"]
    if not reports:
        sys.exit("No reports for sale yet.")
    if wanted:
        return next((r for r in reports if r["id"] == wanted), None) or sys.exit(f"report {wanted} not found")
    try:  # the buyer's own 'research strategy': the hottest topic on the radar, newest report about it
        radar = http.get(f"{api}/api/radar").json()
        for t in radar["topics"]:
            if t["rank"]:
                match = [r for r in reports if r["topic"].lower() == t["topic"].lower()]
                if match:
                    print(f"Hottest radar topic with a report: {t['topic']} (heat {t['heat']}%)")
                    return match[0]
    except Exception:  # noqa: BLE001
        pass
    return reports[0]


def pay(buyer: str, key: str, seller: str, amount_near: float) -> str:
    """Native NEAR transfer on testnet, signed by the buyer. Returns the transaction hash."""
    from py_near.account import Account

    check_testnet(buyer, TESTNET_RPC)
    check_testnet(seller, TESTNET_RPC)

    async def go() -> str:
        acc = Account(buyer, key, rpc_addr=TESTNET_RPC)
        await acc.startup()
        res = await acc.send_money(seller, near_to_yocto(amount_near))
        tx = getattr(getattr(res, "transaction", None), "hash", None) or getattr(res, "transaction_hash", None) or res
        return str(tx)
    return asyncio.run(go())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", help="run id to buy")
    ap.add_argument("--dry-run", action="store_true", help="choose and show, but do not pay")
    ap.add_argument("--api", default=API)
    args = ap.parse_args()
    quiet_network_logs()
    api = args.api
    s = get_settings()
    creds = s.buyer_credentials()
    http = httpx.Client(timeout=60.0)

    chosen = pick_report(http, args.report, api)
    print(f"Chosen report: {chosen['id']}\n  topic: {chosen['topic']}  score: {chosen['score']}  findings: {chosen['findings']}  sources: {chosen['sources']}")
    print(f"  price: {chosen['price_near']} NEAR (testnet)  seller: {chosen['seller_account']}  fingerprint: {chosen['sha256'][:16]}…")
    print(f"  teaser: {(chosen['summary'] or '')[:220]}…")
    if args.dry_run:
        print("\nDry run: nothing sent.")
        return 0
    if not creds:
        print("\nBUYER_TESTNET_ACCOUNT_ID / BUYER_TESTNET_PRIVATE_KEY are not set in .env; cannot pay.")
        return 1
    buyer, key = creds
    if buyer == chosen["seller_account"]:
        print("\nRefusing: the buyer account is the seller account.")
        return 1

    print(f"\nPaying {chosen['price_near']} NEAR from {buyer} to {chosen['seller_account']} on testnet...")
    tx_hash = pay(buyer, key, chosen["seller_account"], chosen["price_near"])
    print(f"  payment tx: {tx_hash}  https://testnet.nearblocks.io/txns/{tx_hash}")

    r = http.post(f"{api}/api/market/{chosen['id']}/purchase", json={"buyer_account": buyer, "tx_hash": tx_hash})
    if r.status_code != 200:
        print(f"  purchase refused: HTTP {r.status_code} {r.json().get('detail')}")
        return 1
    body = r.json()
    report = ResearchReport.model_validate(body["report"])
    out = BACKEND_DIR / "runs" / f"bought_{chosen['id']}.md"
    out.write_text(body.get("markdown") or "", encoding="utf-8")
    digest = report_digest(report)
    onchain = (report.chain_record or {}).get("sha256")
    print(f"\nUnlocked. Receipt: {json.dumps(body['receipt'])}")
    print(f"Report saved: {out}")
    print(f"Fingerprint check: computed {digest[:16]}… vs recorded on NEAR {str(onchain)[:16]}… -> "
          + ("MATCH" if onchain == digest else "no on-chain record for this report" if not onchain else "MISMATCH"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

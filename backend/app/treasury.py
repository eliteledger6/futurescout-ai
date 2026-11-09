"""Treasury: what the agent EARNS (report sales on NEAR testnet) against what it SPENDS on research (model + X data).

Everything is read from records that already exist: the purchase ledger, the saved runs' usage tables, and the
seller account's balance on NEAR testnet (free RPC view). No model, no trading. Testnet NEAR has no value; the
point is the loop (an agent funding its own research), not the number.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Optional

import httpx

from app.chain.near_record import TESTNET_RPC, NearRecordError, check_testnet
from app.chain.payments import yocto_to_near


def read_balance(http: httpx.Client, rpc: str, account_id: str) -> dict:
    """view_account on NEAR testnet -> {'available_near', 'locked_near', 'storage_bytes'}. Read-only, no key."""
    check_testnet(account_id, rpc)
    body = {"jsonrpc": "2.0", "id": "fs-bal", "method": "query",
            "params": {"request_type": "view_account", "finality": "final", "account_id": account_id}}
    try:
        payload: Any = http.post(rpc, json=body, timeout=30).json()
    except (httpx.HTTPError, ValueError) as exc:
        raise NearRecordError(f"could not read the balance from NEAR testnet ({type(exc).__name__})") from None
    if "error" in payload or "result" not in payload:
        raise NearRecordError(f"NEAR RPC error: {str(payload.get('error', payload))[:200]}")
    res = payload["result"]
    return {"available_near": round(yocto_to_near(int(res.get("amount", "0"))), 4),
            "locked_near": round(yocto_to_near(int(res.get("locked", "0"))), 4),
            "storage_bytes": int(res.get("storage_usage", 0))}


def treasury_report(
    *,
    seller: Optional[str],
    runs: list[dict],                           # store.list() rows (have total_cost_usd, generated_at, id, topic)
    purchases_for: Callable[[str], list[dict]], # ledger.purchases(run_id)
    price_near: float,
    balance_reader: Optional[Callable[[str], dict]] = None,
    near_usd: Optional[float] = None,           # optional reference price, only to put both numbers in one unit
) -> dict:
    sales: list[dict] = []
    for r in runs:
        for p in purchases_for(r["id"]):
            amount = yocto_to_near(int(p["amount_yocto"])) if p.get("amount_yocto") else price_near
            sales.append({"run_id": r["id"], "topic": r["topic"], "buyer": p["buyer_account"], "amount_near": round(amount, 4),
                          "tx_hash": p["tx_hash"], "purchased_at": p.get("purchased_at"),
                          "explorer_url": f"https://testnet.nearblocks.io/txns/{p['tx_hash']}"})
    earned_near = round(sum(s["amount_near"] for s in sales), 4)
    spent_usd = round(sum(float(r.get("total_cost_usd") or 0) for r in runs), 4)
    balance: Optional[dict] = None
    balance_error: Optional[str] = None
    if seller and balance_reader is not None:
        try:
            balance = balance_reader(seller)
        except NearRecordError as exc:
            balance_error = str(exc)
    per_run = [{"run_id": r["id"], "topic": r["topic"], "generated_at": r["generated_at"], "cost_usd": r.get("total_cost_usd"),
                "sales": sum(1 for s in sales if s["run_id"] == r["id"]),
                "earned_near": round(sum(s["amount_near"] for s in sales if s["run_id"] == r["id"]), 4)} for r in runs]
    reports_to_break_even = None
    if near_usd and price_near > 0 and runs:
        avg_cost = spent_usd / len(runs)
        reports_to_break_even = round(avg_cost / (price_near * near_usd), 1)
    return {
        "network": "testnet", "seller_account": seller, "price_near": price_near,
        "earned_near": earned_near, "sales": len(sales), "spent_usd": spent_usd, "runs": len(runs),
        "avg_cost_per_run_usd": round(spent_usd / len(runs), 4) if runs else None,
        "balance": balance, "balance_error": balance_error,
        "near_usd_reference": near_usd, "sales_per_report_to_break_even": reports_to_break_even,
        "per_run": per_run, "recent_sales": sales[-10:][::-1],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": "Testnet tokens have no value. This shows the loop (reports sold -> research paid), not real income.",
    }


def default_balance_reader(rpc: str = TESTNET_RPC) -> Callable[[str], dict]:
    http = httpx.Client(timeout=30.0)
    return lambda account: read_balance(http, rpc, account)

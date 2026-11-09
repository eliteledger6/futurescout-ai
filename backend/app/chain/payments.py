"""Verify a NEAR payment for a report (testnet). No custom contract: the buyer sends a native NEAR
transfer to the seller account and hands us the transaction hash; we read the transaction from the
chain and check it ourselves.

RPC: method "tx" with {"tx_hash", "sender_account_id", "wait_until": "FINAL"} returns the signed
transaction (signer_id, receiver_id, actions[{Transfer: {deposit}}]) and its final status.
Checks: final success, signer == buyer, receiver == seller, total Transfer deposit >= price,
and (in the repository) that the hash has not been redeemed before. Nothing here signs or sends;
the seller key is never needed to verify.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional

import httpx

from app.chain.near_record import TESTNET_RPC, NearRecordError, check_testnet

YOCTO = 10**24


def near_to_yocto(amount_near: float) -> int:
    """Exact: 0.1 NEAR -> 10**23 (float multiplication gave ...8388608, seen live)."""
    return int((Decimal(str(amount_near)) * YOCTO).to_integral_value())


def yocto_to_near(yocto: int) -> float:
    return yocto / YOCTO


@dataclass
class VerifiedPayment:
    tx_hash: str
    buyer: str
    seller: str
    amount_yocto: int
    block_hash: Optional[str]

    @property
    def amount_near(self) -> float:
        return yocto_to_near(self.amount_yocto)


def parse_transfer(payload: Any, *, tx_hash: str, buyer: str, seller: str, min_yocto: int) -> VerifiedPayment:
    """Check a `tx` RPC result. Raises NearRecordError with a plain reason when it does not qualify."""
    if not isinstance(payload, dict):
        raise NearRecordError("RPC response had an unexpected shape")
    if "error" in payload:
        raise NearRecordError(f"transaction not found or RPC error: {str(payload['error'].get('data') or payload['error'])[:160]}")
    result = payload.get("result") or {}
    status = result.get("status") or {}
    if "SuccessValue" not in status and "SuccessReceiptId" not in status:
        raise NearRecordError("transaction did not succeed (or is not final yet)")
    tx = result.get("transaction") or {}
    if tx.get("hash") and tx["hash"] != tx_hash:
        raise NearRecordError("transaction hash mismatch")
    if tx.get("signer_id") != buyer:
        raise NearRecordError(f"transaction was signed by {tx.get('signer_id')}, not by the buyer {buyer}")
    if tx.get("receiver_id") != seller:
        raise NearRecordError(f"transaction paid {tx.get('receiver_id')}, not the seller {seller}")
    total = 0
    for action in tx.get("actions") or []:
        if isinstance(action, dict) and "Transfer" in action:
            total += int(action["Transfer"].get("deposit") or 0)
    if total < min_yocto:
        raise NearRecordError(f"payment too small: {yocto_to_near(total):.4f} NEAR, price is {yocto_to_near(min_yocto):.4f} NEAR")
    return VerifiedPayment(tx_hash=tx_hash, buyer=buyer, seller=seller, amount_yocto=total,
                           block_hash=(result.get("transaction_outcome") or {}).get("block_hash"))


def fetch_transaction(http: httpx.Client, rpc: str, tx_hash: str, sender: str) -> Any:
    check_testnet(sender, rpc)
    body = {"jsonrpc": "2.0", "id": "fs-pay", "method": "tx",
            "params": {"tx_hash": tx_hash, "sender_account_id": sender, "wait_until": "FINAL"}}
    try:
        return http.post(rpc, json=body, timeout=30).json()
    except (httpx.HTTPError, ValueError) as exc:
        raise NearRecordError(f"could not read the transaction from NEAR testnet ({type(exc).__name__})") from None


def verify_payment(tx_hash: str, buyer: str, seller: str, price_near: float, *, rpc: str = TESTNET_RPC,
                   http: Optional[httpx.Client] = None) -> VerifiedPayment:
    check_testnet(seller, rpc)
    payload = fetch_transaction(http or httpx.Client(timeout=30.0), rpc, tx_hash, buyer)
    return parse_transfer(payload, tx_hash=tx_hash, buyer=buyer, seller=seller, min_yocto=near_to_yocto(price_near))

"""Report marketplace API (NEAR testnet payments).

  GET  /api/market                      listings: every saved report with its price, seller account and a free teaser
  GET  /api/market/{id}?buyer=acct      the teaser, or the FULL report if `buyer` has paid for it
  POST /api/market/{id}/purchase        {buyer_account, tx_hash}: verify the NEAR transfer on-chain, unlock, return the report
  GET  /api/market/{id}/purchases       who bought it (public: accounts and payment transactions)

The seller is the research platform's NEAR account (NEAR_TESTNET_ACCOUNT_ID). Payment verification
reads the chain and needs no key. If the seller key is configured, each sale is also noted on-chain.
The owner dashboard (/api/runs) is separate and never locked.
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional, Protocol

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.api.store import ReportStore, summarize
from app.chain.near_record import NearRecordError, NearRecorder, report_digest
from app.chain.payments import VerifiedPayment, verify_payment
from app.config import Settings
from app.report.markdown import DISCLAIMER

log = logging.getLogger("futurescout.market")


class PurchaseRequest(BaseModel):
    buyer_account: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9._-]+$")
    tx_hash: str = Field(min_length=32, max_length=64, pattern=r"^[A-Za-z0-9]+$")


class Ledger(Protocol):
    def has_access(self, run_id: str, buyer: str) -> bool: ...
    def tx_used(self, tx_hash: str) -> bool: ...
    def record(self, run_id: str, p: VerifiedPayment, sale_record: Optional[dict]) -> None: ...
    def purchases(self, run_id: str) -> list[dict]: ...


class FileLedger:
    """Purchases in a JSON file (used when there is no database)."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()

    def _load(self) -> list[dict]:
        return json.loads(self.path.read_text(encoding="utf-8")) if self.path.is_file() else []

    def has_access(self, run_id: str, buyer: str) -> bool:
        return any(p["run_id"] == run_id and p["buyer_account"] == buyer for p in self._load())

    def tx_used(self, tx_hash: str) -> bool:
        return any(p["tx_hash"] == tx_hash for p in self._load())

    def record(self, run_id: str, p: VerifiedPayment, sale_record: Optional[dict]) -> None:
        with self._lock:
            rows = self._load()
            rows.append({"run_id": run_id, "buyer_account": p.buyer, "seller_account": p.seller, "tx_hash": p.tx_hash,
                         "amount_yocto": str(p.amount_yocto), "network": "testnet",
                         "purchased_at": datetime.now(timezone.utc).isoformat(), "sale_record": sale_record})
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def purchases(self, run_id: str) -> list[dict]:
        return [p for p in self._load() if p["run_id"] == run_id]


class DbLedger:
    def __init__(self, sessions) -> None:
        self._sessions = sessions

    def has_access(self, run_id: str, buyer: str) -> bool:
        from app.db import has_access
        with self._sessions() as s:
            return has_access(s, run_id, buyer)

    def tx_used(self, tx_hash: str) -> bool:
        from app.db import tx_already_used
        with self._sessions() as s:
            return tx_already_used(s, tx_hash)

    def record(self, run_id: str, p: VerifiedPayment, sale_record: Optional[dict]) -> None:
        from app.db import record_purchase
        with self._sessions() as s:
            record_purchase(s, run_id=run_id, buyer=p.buyer, seller=p.seller, tx_hash=p.tx_hash, amount_yocto=p.amount_yocto,
                            purchased_at=datetime.now(timezone.utc), sale_record=sale_record)
            s.commit()

    def purchases(self, run_id: str) -> list[dict]:
        from app.db import purchases_for
        with self._sessions() as s:
            return [{"buyer_account": p.buyer_account, "tx_hash": p.tx_hash, "amount_yocto": p.amount_yocto,
                     "purchased_at": p.purchased_at.isoformat(), "sale_record": p.sale_record} for p in purchases_for(s, run_id)]


def teaser(run_id: str, report, price_near: float, seller: Optional[str]) -> dict:
    """What a buyer sees before paying: enough to decide, not the evidence."""
    s = summarize(run_id, report)
    draft = report.investment.draft if report.investment else None
    return {
        **s, "locked": True, "price_near": price_near, "seller_account": seller, "network": "testnet",
        "summary": draft.summary if draft else None,
        "themes": [t.name for t in draft.themes] if draft else [],
        "sha256": report_digest(report), "chain_record": report.chain_record,
        "disclaimer": DISCLAIMER.replace("**", ""),
        "how_to_buy": (f"Send at least {price_near} NEAR (testnet) from your account to {seller or '<seller not configured>'}, "
                       f"then POST /api/market/{run_id}/purchase with your account id and the transaction hash."),
    }


def market_router(
    settings: Settings,
    store: ReportStore,
    ledger: Ledger,
    *,
    verifier: Callable[[str, str, str, float], VerifiedPayment] = verify_payment,
    recorder_factory: Optional[Callable[[], Optional[NearRecorder]]] = None,
) -> APIRouter:
    router = APIRouter(prefix="/api/market", tags=["market"])
    seller = (settings.near_testnet_account_id or "").strip() or None
    price = settings.report_price_near

    def make_recorder() -> Optional[NearRecorder]:
        if recorder_factory is not None:
            return recorder_factory()
        creds = settings.near_testnet_credentials()
        return NearRecorder(*creds) if creds else None

    @router.get("")
    def listings(limit: int = Query(50, ge=1, le=200)) -> dict:
        rows = []
        for s in store.list(limit=limit):
            found = store.get(s["id"])
            if found:
                rows.append(teaser(s["id"], found[0], price, seller))
        return {"seller_account": seller, "price_near": price, "network": "testnet", "enabled": seller is not None, "reports": rows}

    @router.get("/{run_id}")
    def view(run_id: str, buyer: Optional[str] = Query(None, max_length=64)) -> dict:
        found = store.get(run_id)
        if found is None:
            raise HTTPException(404, "report not found")
        report, markdown = found
        if buyer and ledger.has_access(run_id, buyer):
            return {"locked": False, "summary": summarize(run_id, report), "report": report.model_dump(mode="json"), "markdown": markdown}
        return teaser(run_id, report, price, seller)

    @router.post("/{run_id}/purchase")
    def purchase(run_id: str, req: PurchaseRequest) -> dict:
        if seller is None:
            raise HTTPException(503, "marketplace disabled: the seller account (NEAR_TESTNET_ACCOUNT_ID) is not configured")
        found = store.get(run_id)
        if found is None:
            raise HTTPException(404, "report not found")
        report, markdown = found
        if ledger.has_access(run_id, req.buyer_account):
            return {"locked": False, "already_purchased": True, "report": report.model_dump(mode="json"), "markdown": markdown}
        if ledger.tx_used(req.tx_hash):
            raise HTTPException(409, "this payment transaction was already used to unlock a report")
        try:
            payment = verifier(req.tx_hash, req.buyer_account, seller, price)
        except NearRecordError as exc:
            raise HTTPException(402, f"payment not accepted: {exc}") from None
        sale_record = None
        try:
            rec = make_recorder()
            if rec is not None:
                sale_record = rec.record_sale(run_id, payment.buyer, payment.tx_hash, payment.amount_yocto).as_dict()
        except NearRecordError as exc:   # the sale still stands; the public note is best effort
            log.warning("sale record failed: %s", exc)
        ledger.record(run_id, payment, sale_record)
        return {"locked": False, "receipt": {"buyer": payment.buyer, "seller": payment.seller, "amount_near": payment.amount_near,
                                              "tx_hash": payment.tx_hash, "network": "testnet", "sale_record": sale_record},
                "sha256": report_digest(report), "report": report.model_dump(mode="json"), "markdown": markdown}

    @router.get("/{run_id}/purchases")
    def purchases(run_id: str) -> list[dict]:
        if store.get(run_id) is None:
            raise HTTPException(404, "report not found")
        return ledger.purchases(run_id)

    return router

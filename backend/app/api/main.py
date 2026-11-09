"""FastAPI backend for the dashboard.

  GET  /api/health              is the server up, where reports come from
  GET  /api/config              agents, models per agent, whether new runs are enabled, disclaimer
  GET  /api/runs                saved runs (newest first), ?topic= filter
  GET  /api/runs/{id}           one full report (all findings, sources, score, usage) + Markdown
  POST /api/runs                start a new research run (only if ENABLE_RUN_API=true; one at a time)
  GET  /api/jobs/{id}           status of a started run

Runs locally on 127.0.0.1 (see scripts/serve.py). Never returns keys, prompts or the database URL.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app import service
from app.api.market import DbLedger, FileLedger, Ledger, market_router
from app.api.store import DbStore, FileStore, ReportStore, summarize
from app.chain.near_record import NearRecorder
from app.chain.payments import VerifiedPayment, verify_payment
from app.chain import NearRecordError, read_record, report_digest, verify
from app.chain.near_record import SOCIALDB_TESTNET, TESTNET_RPC
from app.config import ConfigError, Settings, get_settings
from app.graph.workflow import AGENTS_NOT_BUILT
from app.models.config import load_model_config
from app.portfolio import load_portfolio, portfolio_payload, save_portfolio, sync_from_store
from app.radar import load_radar
from app.treasury import default_balance_reader, treasury_report
from app.watch import load_state as load_watch_state
from app.report.markdown import DISCLAIMER

log = logging.getLogger("futurescout.api")

DASHBOARD_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
ESTIMATED_RUN_COST_USD = 0.17  # measured on two live runs, 2026-11-08 (0.170 and 0.166)


class RunRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=120)
    question: Optional[str] = Field(default=None, max_length=500)
    sector: Optional[str] = Field(default=None, max_length=40)
    news: bool = False  # GDELT has refused this network so far; off by default


@dataclass
class Job:
    id: str
    topic: str
    status: str = "running"            # running | done | failed
    started_at: float = field(default_factory=time.time)
    finished_at: Optional[float] = None
    run_id: Optional[str] = None       # database id or report file name
    error: Optional[str] = None

    def as_dict(self) -> dict:
        end = self.finished_at or time.time()
        return {"id": self.id, "topic": self.topic, "status": self.status, "run_id": self.run_id,
                "error": self.error, "elapsed_s": round(end - self.started_at, 1)}


def _read_testnet(account: str, key: str, contract: str) -> Optional[dict]:
    with httpx.Client(timeout=20.0) as http:
        return read_record(http, TESTNET_RPC, contract, account, key)


SAMPLES_DIR = service.BACKEND_DIR / "samples"   # real past runs shipped with the repo (scripts/export_samples.py)


def _default_store(settings: Settings) -> ReportStore:
    url = settings.database_url_value()
    if url:
        try:
            return DbStore(url)
        except Exception as exc:  # noqa: BLE001
            log.warning("database unavailable (%s); serving report files instead", type(exc).__name__)
    if not list(service.RUNS_DIR.glob("report_*.json")) and list(SAMPLES_DIR.glob("report_*.json")):
        log.info("no runs yet: serving the sample reports in %s", SAMPLES_DIR)
        return FileStore(SAMPLES_DIR)
    return FileStore(service.RUNS_DIR)


def create_app(
    settings: Optional[Settings] = None,
    store: Optional[ReportStore] = None,
    runner: Optional[Callable[[RunRequest, Settings], str]] = None,
    chain_reader: Optional[Callable[[str, str, str], Optional[dict]]] = None,
    ledger: Optional[Ledger] = None,
    payment_verifier: Optional[Callable[[str, str, str, float], VerifiedPayment]] = None,
    sale_recorder: Optional[Callable[[], Optional[NearRecorder]]] = None,
    balance_reader: Optional[Callable[[str], dict]] = None,
    portfolio_path: Optional[Path] = None,
) -> FastAPI:
    settings = settings or get_settings()
    read_onchain = chain_reader or _read_testnet
    store = store or _default_store(settings)
    if ledger is None:
        ledger = DbLedger(store._sessions) if isinstance(store, DbStore) else FileLedger(service.RUNS_DIR / "purchases.json")
    portfolio_path = portfolio_path or (service.RUNS_DIR / "portfolio.json")
    balances = balance_reader if balance_reader is not None else default_balance_reader()
    jobs: dict[str, Job] = {}
    lock = threading.Lock()

    def default_runner(req: RunRequest, s: Settings) -> str:
        outcome = service.execute(req.topic, s, question=req.question, sector=req.sector, news=req.news, warn=log.warning)
        return outcome.run_id or outcome.json_path.stem

    run = runner or default_runner

    app = FastAPI(title="FUTURESCOUT AI API", version="0.1.0",
                  description="Research information only, not investment advice.")
    app.add_middleware(CORSMiddleware, allow_origins=DASHBOARD_ORIGINS, allow_methods=["GET", "POST"],
                       allow_headers=["Content-Type"],
                       allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$")  # any local dev port

    @app.get("/api/health")
    def health() -> dict:
        return {"ok": True, "store": store.kind}

    @app.get("/api/config")
    def config() -> dict:
        cfg = load_model_config()
        agents = {name: cfg.models[a.primary].id for name, a in cfg.agents.items() if name not in AGENTS_NOT_BUILT}
        return {
            "run_api_enabled": settings.enable_run_api,
            "estimated_run_cost_usd": ESTIMATED_RUN_COST_USD,
            "agents": agents,
            "agents_not_built": AGENTS_NOT_BUILT,
            "store": store.kind,
            "disclaimer": DISCLAIMER.replace("**", ""),
            "model_provider": "NEAR AI Cloud",
        }

    @app.get("/api/sectors")
    def sectors() -> list[dict]:
        """The technology sectors (config/sectors.yaml) with their topic and company counts."""
        from app.agents.market.agent import load_companies
        from app.radar import load_sectors, load_topics
        topics, companies = load_topics(), load_companies()
        return [{"key": s.key, "name": s.name, "hints": s.hints, "discovery_queries": s.discovery_queries,
                 "topics": sum(1 for t in topics if t.sector == s.key), "companies": sum(1 for c in companies if c.sector == s.key)}
                for s in load_sectors()]

    @app.get("/api/radar")
    def radar() -> dict:
        """Hot-topic radar (code-computed counts, no model). Produced by scripts/run_radar.py."""
        data = load_radar()
        if data is None:
            raise HTTPException(404, "No radar yet. Run: python scripts\\run_radar.py")
        return data.model_dump(mode="json")

    @app.get("/api/watch")
    def watch() -> dict:
        """Watch-mode status: last X scan, topics mentioned, research runs it started, recent decisions."""
        st = load_watch_state()
        recent = list(reversed(st.events[-40:]))
        return {
            "active": st.last_scan_at is not None,
            "last_scan_at": st.last_scan_at.isoformat() if st.last_scan_at else None,
            "scan_interval_minutes": settings.watch_x_interval_minutes,
            "runs_started": list(reversed(st.runs_started[-20:])),
            "runs_today": st.runs_today(datetime.now(timezone.utc)),
            "max_runs_per_day": settings.watch_max_runs_per_day,
            "latest_mentions": (st.mention_history[-1]["mentions"] if st.mention_history else {}),
            "events": recent,
        }

    @app.get("/api/runs")
    def runs(limit: int = Query(50, ge=1, le=200), topic: Optional[str] = Query(None, max_length=120)) -> list[dict]:
        return store.list(limit=limit, topic=topic)

    @app.get("/api/runs/{run_id}")
    def run_detail(run_id: str) -> dict:
        found = store.get(run_id)
        if found is None:
            raise HTTPException(404, "run not found")
        report, markdown = found
        return {"summary": summarize(run_id, report), "report": report.model_dump(mode="json"), "markdown": markdown}

    @app.get("/api/runs/{run_id}/verify")
    def verify_run(run_id: str) -> dict:
        """Recompute the report fingerprint and compare it with the value stored on NEAR testnet (free read)."""
        found = store.get(run_id)
        if found is None:
            raise HTTPException(404, "run not found")
        report, _ = found
        rec = report.chain_record
        if not rec:
            return {"status": "not_recorded", "sha256": report_digest(report)}
        try:
            onchain = read_onchain(rec["account"], rec["key"], rec.get("contract", SOCIALDB_TESTNET))
        except NearRecordError as exc:
            return {"status": "unavailable", "detail": str(exc), "sha256": report_digest(report)}
        return {**verify(report, onchain), "explorer_url": rec.get("explorer_url"), "account": rec["account"],
                "contract": rec.get("contract"), "network": "testnet"}

    @app.post("/api/runs", status_code=202)
    def start_run(req: RunRequest) -> dict:
        if not settings.enable_run_api:
            raise HTTPException(403, "Starting runs from the dashboard is switched off. Set ENABLE_RUN_API=true in .env "
                                     "and restart the server (each run costs about $0.17 of NEAR AI credit).")
        try:
            settings.require_near_key()
        except ConfigError as exc:
            raise HTTPException(400, str(exc)) from None
        with lock:
            if any(j.status == "running" for j in jobs.values()):
                raise HTTPException(409, "A research run is already in progress; wait for it to finish.")
            job = Job(id=str(uuid.uuid4()), topic=req.topic.strip())
            jobs[job.id] = job

        def work() -> None:
            try:
                job.run_id = run(req, settings)
                job.status = "done"
            except Exception as exc:  # noqa: BLE001
                log.exception("research run failed")
                job.status, job.error = "failed", f"{type(exc).__name__}: {str(exc)[:300]}"
            finally:
                job.finished_at = time.time()

        threading.Thread(target=work, daemon=True).start()
        return job.as_dict()

    @app.get("/api/jobs/{job_id}")
    def job_status(job_id: str) -> dict:
        job = jobs.get(job_id)
        if job is None:
            raise HTTPException(404, "job not found")
        return job.as_dict()

    @app.get("/api/portfolio")
    def portfolio() -> dict:
        """The paper portfolio (SIMULATION). Positions are synced from saved reports here; prices via scripts/portfolio.py."""
        pf = load_portfolio(portfolio_path, notional=settings.portfolio_notional_usd, per_report=settings.portfolio_positions_per_report)
        if sync_from_store(pf, store):
            save_portfolio(pf, portfolio_path)
        return portfolio_payload(pf, prices_configured=bool(settings.alpha_vantage_key_value()))

    balance_cache: dict = {}

    def cached_balance(account: str) -> dict:
        """The on-chain balance read is slow-ish (public RPC); remember it for two minutes."""
        hit = balance_cache.get(account)
        if hit and time.time() - hit[0] < 120:
            return hit[1]
        value = balances(account)
        balance_cache[account] = (time.time(), value)
        return value

    @app.get("/api/treasury")
    def treasury() -> dict:
        """Earned (report sales, testnet NEAR) versus spent (model + X costs of every saved run)."""
        seller = (settings.near_testnet_account_id or "").strip() or None
        return treasury_report(seller=seller, runs=store.list(limit=200), purchases_for=ledger.purchases,
                               price_near=settings.report_price_near, balance_reader=cached_balance)

    app.include_router(market_router(settings, store, ledger, verifier=payment_verifier or verify_payment,
                                     recorder_factory=sale_recorder))
    return app

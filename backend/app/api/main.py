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
import os
import re
import threading
import time
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import httpx
from fastapi import Header, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app import service
from app.api.store import DbStore, FileStore, ReportStore, summarize
from app.chain import NearRecordError, read_record, report_digest, verify
from app.chain.near_record import MAINNET_RPC, SOCIALDB_TESTNET, TESTNET_RPC, network_of
from app.config import ConfigError, Settings, get_settings
from app.graph.workflow import AGENTS_NOT_BUILT
from app.models.config import load_model_config
from app.fund import DISCLAIMER as FUND_DISCLAIMER, fund_payload, latest_closes, list_funds, load_fund, load_fund_config, tradable_tokens
from app.fund.strategy import RULES as STRATEGY_RULES
from app.fund.live import DISCLAIMER as LIVE_DISCLAIMER, load_state as load_trading_state, performance, read_balances, shadow_portfolio
from app.portfolio import load_portfolio, portfolio_payload, save_portfolio, sync_from_store
from app.radar import load_radar
from app.watch import load_state as load_watch_state
from app.report.markdown import DISCLAIMER
from app.report.verdict import build_verdict

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
        return read_record(http, TESTNET_RPC if network_of(contract) == "testnet" else MAINNET_RPC, contract, account, key)


SAMPLES_DIR = service.BACKEND_DIR / "samples"   # real past runs shipped with the repo (scripts/export_samples.py)


class ProposalRequest(BaseModel):
    """A visitor proposes a technology topic (free; limited per day; screened by an AI reviewer)."""
    topic: str = Field(min_length=2, max_length=200)


class ProposalSync(BaseModel):
    """The owner's report-agent loop reports what happened to proposals and collects new ones."""
    updates: list[dict] = Field(default_factory=list, max_length=200)


class BuyRequest(BaseModel):
    """A trading bot redeems its NEAR payment for early access to a fresh report."""
    run_id: str = Field(max_length=80)
    tx_hash: str = Field(max_length=80)
    buyer: str = Field(max_length=64)


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
    portfolio_path: Optional[Path] = None,
    funds_dir: Optional[Path] = None,
    trading_dir: Optional[Path] = None,
) -> FastAPI:
    settings = settings or get_settings()
    read_onchain = chain_reader or _read_testnet
    store = store or _default_store(settings)
    portfolio_path = portfolio_path or (service.RUNS_DIR / "portfolio.json")
    funds_dir = funds_dir or (service.RUNS_DIR / "funds")
    trading_dir = trading_dir or (service.RUNS_DIR / "trading")
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
        runs_dir = getattr(store, "runs_dir", None)
        snap = service.BACKEND_DIR / "site_data"
        return {"ok": True, "store": store.kind, "data": runs_dir.name if runs_dir else None,
                "reports": len(list(runs_dir.glob("report_*.json"))) if runs_dir else None,
                # where the server looks for the hosted snapshot (folder names and counts only, nothing private)
                "snapshot": {"exists": snap.is_dir(), "files": len(list(snap.iterdir())) if snap.is_dir() else 0,
                             "reports": len(list(snap.glob("report_*.json"))) if snap.is_dir() else 0,
                             "data_dir_setting": bool(os.environ.get("FUTURESCOUT_DATA_DIR")),
                             "backend_folder": service.BACKEND_DIR.name}}

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
        from app.radar import load_sectors, load_topics
        topics = load_topics()
        return [{"key": s.key, "name": s.name, "hints": s.hints, "discovery_queries": s.discovery_queries,
                 "topics": sum(1 for t in topics if t.sector == s.key)}
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

    # ---------------------------------------------------------------- report market (owner 2026-11-10)
    from app.fund.economy import load_economy, price_report
    from app.fund.report_market import buy as market_buy, demo_free, is_locked, load_market, unlock_at
    econ_path = trading_dir.parent / "economy" / "state.json"
    sales_path = trading_dir.parent / "economy" / "sales.json"
    px_cache: dict = {}
    price_inputs: dict = {}      # run id -> (when read, what the report's price is made from)

    def live_token_prices() -> dict:
        """ticker -> (price, when, source) for the Ondo tokenized stocks, from the public NEAR Intents token list (no key);
        cached 10 minutes. Empty when the list cannot be read."""
        hit = px_cache.get("tokens")
        if hit and time.time() - hit[0] < 600:
            return hit[1]
        out = {}
        try:
            from app.fund.intents_signed import SignedIntents
            for t in SignedIntents(load_fund_config().intents.api).tokens():
                sym = str(t.get("symbol") or "")
                if sym.endswith("on") and sym[:-2].isupper() and t.get("price"):
                    out[sym[:-2]] = (float(t["price"]), str(t.get("priceUpdatedAt") or "")[:16].replace("T", " ") + " UTC",
                                     "NEAR Intents price of the tokenized stock")
        except Exception:  # noqa: BLE001  (no live price: the latest close is used)
            out = {}
        px_cache["tokens"] = (time.time(), out)
        return out

    def near_usd() -> float:
        hit = px_cache.get("near")
        if hit and time.time() - hit[0] < 600:
            return hit[1]
        from app.fund.live import OneClickLive
        fc = load_fund_config()
        px = OneClickLive(fc.intents.api).price_usd(fc.live.near_asset_id)
        px_cache["near"] = (time.time(), px)
        return px

    def report_price(run_id: str, report, ec=None) -> dict:  # noqa: ANN001
        ec = ec or load_fund_config().economy
        known = None if ec.max_price_usd else load_economy(econ_path).prices.get(run_id)   # dollar prices follow the live NEAR price
        if known:
            return {"price_near": known.price_near, "price_usd": known.price_usd}
        # What a price is made from does not change for a saved report, so it is read from the report once an hour at
        # most (the report list would otherwise open every locked report on every request). The NEAR price stays live.
        hit = price_inputs.get(run_id)
        if not hit or time.time() - hit[0] > 3600:
            if report is None:
                found = store.get(run_id)
                if not found:
                    raise KeyError(run_id)
                report = found[0]
            v = build_verdict(report)
            searches = int(((report.patent.source_usage or {}).get("requests") or 0) if report.patent else 0)
            hit = (time.time(), {"topic": report.topic, "cost_usd": report.total_cost_usd or 0.0, "score": v.get("score"),
                                 "confidence_pct": v.get("confidence_pct"), "patent_searches": searches})
            price_inputs[run_id] = hit
        p = price_report(run_id=run_id, near_usd=near_usd(), cfg=ec, now=datetime.now(timezone.utc), **hit[1])
        return {"price_near": p.price_near, "price_usd": p.price_usd}

    def lock_info(run_id: str, report, generated_at: Optional[datetime] = None, ec=None) -> Optional[dict]:  # noqa: ANN001
        """`report` may be None when only the list row is at hand: then `generated_at` is given and the report is opened
        only if its price inputs are not remembered yet. `ec`: the economy settings, when the caller has read them already."""
        ec = ec or load_fund_config().economy
        generated_at = generated_at or report.generated_at
        if not is_locked(generated_at, ec, datetime.now(timezone.utc), run_id):
            return None
        try:
            price = report_price(run_id, report, ec)
        except Exception:  # noqa: BLE001  (no price feed: still locked, price shown as unknown)
            price = {"price_near": None, "price_usd": None}
        until = unlock_at(generated_at, ec)
        return {"locked": True, "unlock_at": until.isoformat() if until else None, "pay_to": ec.seller_account,
                "network": "NEAR mainnet", **price,
                "how_to_buy": ["Send price_near NEAR to pay_to with an ordinary NEAR transfer (mainnet).",
                               "POST /api/market/buy with JSON {run_id, tx_hash, buyer} (buyer = the account that paid).",
                               "Use the returned access_token as ?access=... or the X-Report-Access header on /api/runs/{run_id}."]}

    @app.get("/api/runs")
    def runs(limit: int = Query(50, ge=1, le=200), topic: Optional[str] = Query(None, max_length=120)) -> list[dict]:
        topic = (topic or "").replace("\x00", "").strip() or None      # PostgreSQL refuses NUL in text (seen as HTTP 500)
        rows = store.list(limit=limit, topic=topic)
        ec = load_fund_config().economy
        now = datetime.now(timezone.utc)
        for r in rows:
            if is_locked(datetime.fromisoformat(r["generated_at"]), ec, now, r["id"]):
                info = lock_info(r["id"], None, datetime.fromisoformat(r["generated_at"]), ec)
                if info:
                    r.update({k: info[k] for k in ("locked", "unlock_at", "price_near")})
            elif demo_free(datetime.fromisoformat(r["generated_at"]), ec, r["id"]):
                r["demo_free"] = True                     # open only because the owner unlocked it for the demo
        return rows

    # ---- topic proposals (owner 2026-11-11): stored here, reviewed and researched in the owner's loop ----------
    proposals_path = trading_dir.parent / "proposals" / "state.json"

    def proposals_open() -> bool:
        """Open when enabled and somebody will collect them: locally always; on the hosted snapshot only with the shared secret."""
        from app.proposals import load_config
        hosted = service.RUNS_DIR.name == "site_data"
        return load_config().enabled and (not hosted or bool(settings.proposals_token))

    @app.get("/api/proposals")
    def list_proposals() -> dict:
        from app.proposals import left_today, load_config, load_state, public_view
        pc, st = load_config(), load_state(proposals_path)
        return {"open": proposals_open(), "per_day": pc.per_day, "left_today": left_today(st, pc, datetime.now(timezone.utc)),
                "agent_market_url": pc.agent_market_url, "proposals": public_view(st)}

    @app.post("/api/proposals", status_code=201)
    def propose(req: ProposalRequest) -> dict:
        from app.proposals import load_config, submit
        if not proposals_open():
            raise HTTPException(503, "Topic proposals are closed right now. You can hire the report agent on NEAR Agent Market.")
        try:
            p = submit(proposals_path, req.topic, load_config(), datetime.now(timezone.utc))
        except OverflowError as exc:
            raise HTTPException(429, str(exc)) from None
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from None
        return p.model_dump(mode="json")

    @app.post("/api/proposals/sync")
    def sync_proposals(req: ProposalSync, x_proposals_token: Optional[str] = Header(None)) -> dict:
        import hmac
        from app.proposals import apply_updates
        secret = settings.proposals_token.get_secret_value().strip() if settings.proposals_token else ""
        if not secret or not hmac.compare_digest(secret, (x_proposals_token or "").strip()):
            raise HTTPException(401, "not allowed")
        st = apply_updates(proposals_path, req.updates, datetime.now(timezone.utc))
        return {"proposals": [p.model_dump(mode="json") for p in st.proposals]}

    @app.get("/api/market")
    def market() -> dict:
        """Fresh reports on sale to any trading bot (early access), with price and the account to pay. Read-only."""
        ec = load_fund_config().economy
        items, seen = [], set()
        for r in store.list(limit=200):                      # newest first: the newest scored report per topic is on sale
            if r.get("score") is None or r["topic"] in seen:
                continue
            seen.add(r["topic"])
            if not is_locked(datetime.fromisoformat(r["generated_at"]), ec, datetime.now(timezone.utc), r["id"]):
                continue
            info = lock_info(r["id"], None, datetime.fromisoformat(r["generated_at"]), ec)
            if info:
                items.append({"run_id": r["id"], "topic": r["topic"], "sector": r.get("sector"), "generated_at": r["generated_at"],
                              "score": r.get("score"), **{k: info[k] for k in ("unlock_at", "price_near", "price_usd")}})
        return {"open": ec.market_open, "embargo_hours": ec.embargo_hours, "pay_to": ec.seller_account, "network": "NEAR mainnet",
                "reports": items, "sold": len(load_market(sales_path).sales),
                "how_to_buy": ["GET /api/market to see fresh reports and their price in NEAR.",
                               "Send price_near NEAR to pay_to with an ordinary NEAR mainnet transfer.",
                               "POST /api/market/buy with JSON {run_id, tx_hash, buyer}; you get the full report and an access token.",
                               "Reports are never free on the website: paid access only." if ec.embargo_hours is None else
                               f"Every report becomes free on the website {ec.embargo_hours:g} hours after it was written."]}

    @app.post("/api/market/buy")
    def market_buy_endpoint(req: BuyRequest) -> dict:
        """Grant access after checking the buyer's NEAR payment on chain (reads only; nothing is signed here)."""
        from app.fund.economy import read_tx
        found = store.get(req.run_id)
        if found is None:
            raise HTTPException(404, "run not found")
        report, markdown = found
        info = lock_info(req.run_id, report)
        if not info:
            raise HTTPException(409, "this report is no longer in early access: it is free at /api/runs/" + req.run_id)
        if info.get("price_near") is None:
            raise HTTPException(503, "no NEAR price available right now; try again in a minute")
        ec = load_fund_config().economy
        try:
            with httpx.Client(timeout=60.0) as http:
                sale = market_buy(state=load_market(sales_path), path=sales_path, run_id=req.run_id, buyer=req.buyer, tx_hash=req.tx_hash,
                                  price_near=info["price_near"] * 0.97, cfg=ec,   # 3% leeway: the NEAR price moves between quote and payment
                                  read=lambda h, who: read_tx(http, ec.rpc, h, who),
                                  now=datetime.now(timezone.utc))
        except ValueError as exc:
            raise HTTPException(402, {"message": str(exc), **info}) from None
        return {"access_token": sale.token, "paid_near": sale.amount_near, "tx_hash": sale.tx_hash,
                "summary": summarize(req.run_id, report), "report": report.model_dump(mode="json"), "markdown": markdown,
                "verdict": build_verdict(report)}

    @app.get("/api/runs/{run_id}")
    def run_detail(run_id: str, access: Optional[str] = Query(None, max_length=80),
                   x_report_access: Optional[str] = Header(None)) -> dict:
        found = store.get(run_id)
        if found is None:
            raise HTTPException(404, "run not found")
        report, markdown = found
        info = lock_info(run_id, report)
        if info:
            sale = load_market(sales_path).by_token(access or x_report_access or "")
            if not sale or sale.run_id != run_id:
                msg = ("Paid report: buy access from the report agent in NEAR." if not info["unlock_at"] else
                       "Fresh report: early access is sold to trading bots. It is free here after " + info["unlock_at"])
                raise HTTPException(402, {"message": msg, **info, "summary": summarize(run_id, report)})
        summary = summarize(run_id, report)
        if not info and demo_free(report.generated_at, load_fund_config().economy, run_id):
            summary["demo_free"] = True
        return {"summary": summary, "report": report.model_dump(mode="json"), "markdown": markdown,
                "verdict": build_verdict(report)}

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
                "contract": rec.get("contract"), "network": rec.get("network") or network_of(rec.get("contract") or SOCIALDB_TESTNET)}

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

    @app.get("/api/funds")
    def funds() -> dict:
        """Topic funds (SIMULATION, stages 1-2). Built and updated by scripts/funds.py; read-only here."""
        items = [{"topic": f.topic, "slug": f.slug, "sector": f.sector, "updated_at": f.updated_at.isoformat() if f.updated_at else None,
                  "history": [h.model_dump() for h in f.history[-60:]], **f.summary()} for f in list_funds(funds_dir)]
        items.sort(key=lambda x: -(x["last_score"] if x["last_score"] is not None else -1))   # strongest research first
        return {"funds": items, "label": "simulation", "disclaimer": FUND_DISCLAIMER}

    @app.get("/api/funds/{slug}")
    def fund_detail(slug: str) -> dict:
        if not re.fullmatch(r"[a-z0-9-]{1,60}", slug):
            raise HTTPException(status_code=404, detail="fund not found")
        f = load_fund(funds_dir / f"{slug}.json")
        if f is None:
            raise HTTPException(status_code=404, detail="fund not found")
        out = fund_payload(f)
        old = "each decision is fingerprinted on NEAR testnet so it cannot be changed afterwards."
        new = ("decisions made up to 11 November 2026 were sealed on NEAR (the link next to each one); later ones carry "
               "their own fingerprint only, because only reports are sealed now.")
        notes = (out.get("fund") or out).get("notes")
        if isinstance(notes, list):
            notes[:] = [n.replace(old, new) if isinstance(n, str) else n for n in notes]
        return out

    trading_cache: dict = {}
    economy_cache: dict = {}

    @app.get("/api/economy")
    def economy() -> dict:
        """Agent economy, READ-ONLY: report prices, the trading agent's report purchases (paid in NEAR, checked on chain)
        and the report agent's stake for NEAR AI credits. Nothing here can move money or shows a key."""
        from app.fund.economy import YOCTO, account_near, load_economy, staked_amount
        ec = load_fund_config().economy
        st = load_economy(trading_dir.parent / "economy" / "state.json")

        def market_income_summary() -> dict:
            """Fees of accepted NEAR Agent Market hires (recorded by the report agent); they join the 70/30 split."""
            from app import market_income
            inc = market_income.load(trading_dir.parent / market_income.FILE)
            return {"hires": len(inc.fees), "usd": inc.usd(), "near": inc.near()}
        wallet = staked = None
        if ec.seller_account:
            hit = economy_cache.get(ec.seller_account)
            if hit and time.time() - hit[0] < 20:
                wallet, staked = hit[1]
            else:
                try:
                    with httpx.Client(timeout=15.0) as http:
                        liquid, _ = account_near(http, ec.rpc, ec.seller_account)
                        pool = staked_amount(http, ec, ec.seller_account)
                    wallet, staked = round(liquid / YOCTO, 4), (round(pool / YOCTO, 4) if pool is not None else None)
                    economy_cache[ec.seller_account] = (time.time(), (wallet, staked))
                except Exception:  # noqa: BLE001
                    pass
        return {
            "enabled": ec.enabled, "seller_account": ec.seller_account, "staking_contract": ec.staking_contract or None,
            "limits": {"max_price_near": ec.max_price_near, "budget_share_of_fund": ec.budget_share_of_fund,
                       "stake_share": ec.stake_share, "min_stake_near": ec.min_stake_near,
                       "min_price_usd": ec.min_price_usd, "max_price_usd": ec.max_price_usd, "margin_usd": ec.margin_usd},
            "spent_near": st.spent_near(), "report_agent_wallet_near": wallet, "report_agent_staked_near": staked,
            "kept_near": st.kept_near, "second_trader_at_usd": ec.second_trader_at_usd,
            "market_income": market_income_summary(),
            "prices": sorted((p.model_dump(mode="json") for p in st.prices.values()), key=lambda p: -p["price_near"]),
            "purchases": [p.model_dump(mode="json") for p in reversed(st.purchases[-30:])],
            "stakes": [e.model_dump(mode="json") for e in reversed(st.stakes[-10:])],
            "explorer_tx": "https://nearblocks.io/txns/{tx}",
        }

    def holding_briefs(checks: Optional[list] = None) -> dict:
        """The newest daily holding briefs the trading agent bought from the report agent (read-only), each with what
        the trading agent decided when it read it: its first real-money look at or after the brief."""
        from app.fund import holding_brief as hb
        st = hb.load_state(trading_dir.parent / "briefs" / "state.json")
        ec = load_fund_config().economy
        rows = [{"id": b.id, "ticker": b.ticker, "topic": b.topic, "at": b.at.isoformat(), "price_now": b.price_now, "gain_pct": b.gain_pct,
                 "posts_read": b.posts_read, "summary": b.note.summary if b.note else None, "what_changed": b.note.what_changed if b.note else None,
                 "risks": b.note.risks if b.note else [], "urgency": b.note.urgency if b.note else None,
                 "signals": [s.model_dump() for s in b.signals[:5]], "price_usd": b.price_usd, "price_near": b.price_near, "status": b.status,
                 "errors": b.errors} for b in reversed(st.briefs[-6:])]
        looks = sorted((c for c in (checks or []) if c.get("mode") == "live" and c.get("action") in ("buy", "sell", "hold")),
                       key=lambda c: str(c.get("at")))
        for row in rows:
            hit = next((c for c in looks if str(c.get("at")) >= row["at"][:19]), None)
            row["decision"] = ({"at": hit["at"], "action": hit["action"], "ticker": hit.get("ticker"), "summary": hit.get("summary"),
                                "why_woken": [t.get("kind") for t in hit.get("triggers", [])]} if hit else None)
        return {"price_usd": ec.brief_usd, "every_hours": ec.brief_hours, "enabled": ec.enabled and ec.brief_usd > 0,
                "owed_near": round(sum(b.price_near for b in st.owed()), 4), "briefs": rows}

    @app.get("/api/trading")
    def trading() -> dict:
        """Stage 3 live-trading test + shadow mode: READ-ONLY view (limits, balances, proposals). Trades are approved
        only from the owner's terminal (scripts/fund_trade.py approve); nothing here can move money or shows a key."""
        cfg = load_fund_config()
        lv = cfg.live
        state = load_trading_state(trading_dir / "state.json")
        tokens = tradable_tokens(funds_dir)
        account = (settings.fund_mainnet_account_id or "").strip() or None
        balances = None
        if account:
            hit = trading_cache.get(account)
            if hit and time.time() - hit[0] < 60:
                balances = hit[1]
            else:
                try:
                    balances = read_balances(httpx.Client(timeout=20.0), lv, account, tokens)
                except Exception as exc:  # noqa: BLE001
                    balances = {"account": account, "near": None, "usdc": None, "holdings": [], "errors": [type(exc).__name__]}
                trading_cache[account] = (time.time(), balances)
        today = datetime.now(timezone.utc).date().isoformat()
        closes = latest_closes(service.RUNS_DIR / "funds")
        prices = {t: (c, d, "latest daily close") for t, (c, d) in closes.items()}
        prices.update(live_token_prices())                           # live NEAR Intents prices win (as near.com shows)
        return {
            "network": "NEAR mainnet (NEAR Intents has no testnet)", "account": account,
            "key_configured": settings.fund_mainnet_credentials() is not None,
            "trading_enabled": lv.trading_enabled, "kill_switch": (trading_dir / "STOP").exists(),
            "limits": {"max_trade_usd": lv.max_trade_usd, "max_day_usd": lv.max_day_usd, "max_total_usd": lv.max_total_usd,
                       "price_band_pct": lv.price_band_pct, "max_cost_pct": lv.max_cost_pct, "shadow_budget_usd": lv.shadow_budget_usd},
            "spent": {"live_total_usd": state.spent("live"), "live_today_usd": state.spent("live", today),
                      "shadow_filled_usd": round(sum(p.usd for p in state.proposals if p.mode == "shadow" and p.status == "shadow_filled" and p.side == "buy"), 2),
                      "live_proceeds_usd": state.proceeds("live"), "live_counted_usd": state.invested("live", lv.budget_mode)},
            "selling": {"enabled": lv.sells_enabled, "budget_mode": lv.budget_mode, "max_sells_per_day": lv.max_sells_per_day},
            # each holding with the live price the trading agent read at its last check (owner 2026-11-12)
            "live_holdings": [{**h, "watch": state.holding_prices.get("live:" + h["ticker"])} for h in state.live_holdings()],
            "balances": balances,
            "shadow_portfolio": shadow_portfolio(state, {f"{t}on": v[0] for t, v in prices.items()}, lv.shadow_budget_usd),
            "performance": performance(state, prices, lv.shadow_budget_usd),
            "briefs": holding_briefs(state.checks),
            "pay_with": lv.pay_with,
            "strategy": {"rules": STRATEGY_RULES, "config": lv.strategy.model_dump(), "last_check_at": state.last_check_at.isoformat() if state.last_check_at else None},
            "checks": list(reversed((state.checks or [])[-40:])),
            "pending_live": [p.id for p in state.proposals if p.mode == "live" and p.status == "proposed"],
            "auto_approve": lv.auto_approve,
            "allowlist": [{k: t[k] for k in ("ticker", "symbol", "topic", "band", "score", "confidence_pct", "price")} for t in tokens],
            "proposals": [p.model_dump(mode="json") for p in reversed(state.proposals[-60:]) if p.id not in state.hidden],
            "private_near": state.private_near,
            "private_checked_at": state.private_checked_at.isoformat() if state.private_checked_at else None,
            "owner_sales": [{"symbol": p.symbol, "bought_usd": p.usd, "bought_at": p.created_at.isoformat()}
                            for p in state.proposals if p.id in state.hidden],   # sold later by the owner by hand in near.com
            "explorer_tx": lv.explorer_tx,
            "approval": ("automatic: the agent's orders run when every code check passes (owner's setting live.auto_approve)" if lv.auto_approve
                         else "owner's terminal only: python scripts\\fund_trade.py approve <id>"),
            "disclaimer": LIVE_DISCLAIMER,
        }

    return app

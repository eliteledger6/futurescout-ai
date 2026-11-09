"""One full research run: build the clients, run the agents, write report files, save to the database.
Shared by scripts/run_research.py (command line) and the API (dashboard), so both behave the same."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import httpx

from app.chain import NearRecorder, NearRecordError
from app.config import BACKEND_DIR, Settings
from app.db import make_engine, make_session_factory, save_report
from app.graph.workflow import run_research
from app.models.config import load_model_config
from app.models.router import ModelRouter
from app.report import render_markdown
from app.schemas.research import ResearchReport
from app.sources.arxiv import ArxivClient
from app.sources.base import SourceError
from app.sources.edgar import EdgarClient
from app.sources.edgar_fulltext import EdgarFullTextClient
from app.sources.sec_facts import SecFactsClient
from app.sources.epo import EpoOpsClient
from app.sources.prices import AlphaVantageClient
from app.sources.serpapi_patents import SerpApiPatentsClient
from app.sources.gdelt import GdeltClient
from app.sources.openalex import OpenAlexClient
from app.sources.x import XClient

RUNS_DIR = BACKEND_DIR / "runs"


@dataclass
class RunOutcome:
    report: ResearchReport
    markdown: str
    md_path: Path
    json_path: Path
    run_id: Optional[str]  # database id, None if not saved
    usage: Optional[dict] = None   # per-source usage of this run: openalex_usd, serpapi_searches, x_usd, model_usd


def save_to_database(settings: Settings, report: ResearchReport, markdown: str, warn: Callable[[str], None]) -> Optional[str]:
    """Save the run if DATABASE_URL is set. A database problem never loses the report files."""
    if not settings.database_url_value():
        warn("(DATABASE_URL not set: run saved to files only)")
        return None
    try:
        engine = make_engine(settings=settings)
        with make_session_factory(engine)() as session:
            run_id = save_report(session, report, markdown)
            session.commit()
        return run_id
    except Exception as exc:  # noqa: BLE001
        # message only, never the URL (it contains the password)
        warn(f"WARNING: could not save to the database ({type(exc).__name__}); the report files above are complete. "
             "Check that PostgreSQL is running and run: python -m alembic upgrade head")
        return None


def record_on_testnet(settings: Settings, key: str, report: ResearchReport, warn: Callable[[str], None]) -> Optional[dict]:
    """Store the report fingerprint on NEAR testnet. Never blocks or loses a report if it fails."""
    creds = settings.near_testnet_credentials()
    if not creds:
        warn("(NEAR_TESTNET_ACCOUNT_ID / NEAR_TESTNET_PRIVATE_KEY not set: report not recorded on NEAR testnet)")
        return None
    try:
        return NearRecorder(*creds).record(key, report).as_dict()
    except NearRecordError as exc:
        warn(f"WARNING: NEAR testnet record failed: {exc}")
        return None


def execute(
    topic: str,
    settings: Settings,
    *,
    question: Optional[str] = None,
    sector: Optional[str] = None,
    patents_live: Optional[bool] = None,          # override SERPAPI_CACHE_ONLY for this run
    patent_search_budget: Optional[int] = None,   # hard ceiling on SerpApi searches for this run
    news: bool = True,
    use_x: bool = True,
    from_year: Optional[int] = None,
    max_papers: int = 12,
    save_db: bool = True,
    record_on_near: bool = True,
    warn: Callable[[str], None] = print,
    runs_dir: Path = RUNS_DIR,
) -> RunOutcome:
    """Run the whole pipeline once. Raises ConfigError if NEAR_AI_API_KEY is missing."""
    settings.require_near_key()
    if not settings.openalex_key_value():
        warn("WARNING: OPENALEX_API_KEY is not set; OpenAlex will probably reject requests.")
    edgar = discovery = facts = None
    if settings.edgar_user_agent:
        try:
            edgar = EdgarClient(settings.edgar_user_agent)
            discovery = EdgarFullTextClient(settings.edgar_user_agent)
            facts = SecFactsClient(settings.edgar_user_agent)
        except SourceError as exc:
            warn(f"WARNING: {exc}. Market agent will run without SEC filings.")
    else:
        warn("WARNING: EDGAR_USER_AGENT is not set; the Market agent will not read SEC filings.")
    gdelt = GdeltClient(user_agent=settings.http_user_agent) if news else None
    x_client = None
    if use_x and settings.x_token_value():
        x_client = XClient(settings.x_token_value() or "")
    elif use_x:
        warn("WARNING: X_BEARER_TOKEN is not set; the X agent will not run.")
    prices = None
    if settings.alpha_vantage_key_value():
        prices = AlphaVantageClient(settings.alpha_vantage_key_value() or "")
    else:
        warn("WARNING: ALPHA_VANTAGE_API_KEY is not set; the price & timing risk check will not run.")
    patent_client = None      # SerpApi (Google Patents) first, EPO OPS if configured instead
    creds = settings.epo_credentials()
    if settings.serpapi_key_value():
        cache_only = settings.serpapi_cache_only if patents_live is None else not patents_live
        patent_client = SerpApiPatentsClient(settings.serpapi_key_value() or "", cache_only=cache_only, max_searches=patent_search_budget)
    elif creds:
        patent_client = EpoOpsClient(*creds)
    else:
        warn("WARNING: no patent source configured (SERPAPI_API_KEY or EPO keys); the Patent agent will not run.")

    http = httpx.Client(timeout=30.0, headers={"User-Agent": settings.http_user_agent}, follow_redirects=True)
    router = ModelRouter(load_model_config(), settings)
    openalex = OpenAlexClient(settings.openalex_key_value(), http=http)
    report = run_research(
        topic, router=router,
        openalex=openalex,
        arxiv=ArxivClient(http=http),
        edgar=edgar, gdelt=gdelt, discovery=discovery, facts=facts, x_client=x_client, epo=patent_client, prices=prices,
        question=question, sector=sector, from_year=from_year, max_papers=max_papers,
    )

    runs_dir.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    md_path, json_path = runs_dir / f"report_{stamp}.md", runs_dir / f"report_{stamp}.json"
    if record_on_near:
        report.chain_record = record_on_testnet(settings, f"report_{stamp}", report, warn)
    markdown = render_markdown(report)
    md_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    run_id = save_to_database(settings, report, markdown, warn) if save_db else None
    x_usd = sum(u.get("cost_usd", 0.0) for u in report.usage if u.get("agent") == "x (data)")
    usage = {"openalex_usd": openalex.cost_usd, "openalex_requests": openalex.requests, "openalex_remaining_usd": openalex.remaining_usd,
             "serpapi_searches": getattr(patent_client, "searches_used", 0) if patent_client else 0,
             "x_usd": round(x_usd, 4), "model_usd": round(report.total_cost_usd - x_usd, 6)}
    return RunOutcome(report, markdown, md_path, json_path, run_id, usage)

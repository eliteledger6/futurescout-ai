"""Paper portfolio: "what if someone had acted on the reports?"  A SIMULATION. No money moves, nothing is traded.

Rules (all code, no model):
  * Every saved report contributes its top Company Scout candidates (SEC-listed, with a ticker) as pretend positions.
  * Each position is a fixed pretend notional (PORTFOLIO_NOTIONAL_USD) "bought" at the first daily close on or
    after the report's generation date. Until that close exists the position is "pending".
  * Prices come from Alpha Vantage daily data (last ~100 trading days, free plan: 25 requests/day), so a position
    older than ~100 trading days cannot be priced from scratch; its entry is kept once recorded.
  * A benchmark ETF (default SOXX) is tracked over the same dates for comparison.
  * The record is derived from reports that are fingerprinted on NEAR testnet, so entries cannot be backdated.

This measures whether the research points at companies that later did well; it is not advice and not a track record
anyone should invest on. Labels in the UI say "simulation".
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from pydantic import BaseModel, Field

from app.schemas.research import ResearchReport
from app.sources.base import SourceError
from app.sources.prices import AlphaVantageClient, Bar

log = logging.getLogger("futurescout.portfolio")


class Position(BaseModel):
    run_id: str
    topic: str
    report_date: str                      # YYYY-MM-DD (UTC) of the report; entry is the first close on/after it
    ticker: str
    company: str
    next_runner_score: Optional[float] = None
    notional_usd: float
    status: str = "pending"               # pending | open | error
    entry_date: Optional[str] = None
    entry_close: Optional[float] = None
    shares: Optional[float] = None
    last_date: Optional[str] = None
    last_close: Optional[float] = None
    value_usd: Optional[float] = None
    return_pct: Optional[float] = None
    note: Optional[str] = None
    price_source_url: Optional[str] = None


class Benchmark(BaseModel):
    ticker: str
    entry_date: Optional[str] = None      # earliest position entry date
    entry_close: Optional[float] = None
    last_date: Optional[str] = None
    last_close: Optional[float] = None
    return_pct: Optional[float] = None
    note: Optional[str] = None


class Portfolio(BaseModel):
    kind: str = "simulation"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    prices_updated_at: Optional[datetime] = None
    notional_usd: float
    positions_per_report: int
    positions: list[Position] = Field(default_factory=list)
    benchmark: Optional[Benchmark] = None
    price_requests_last_update: int = 0
    notes: list[str] = Field(default_factory=lambda: [
        "Simulation only: no money moves and nothing is traded.",
        "Positions are the top Company Scout candidates of each sealed report, bought at the first close on or after the report date.",
        "Equal pretend notional per position; returns are price-only (no dividends, fees or taxes).",
        "Not investment advice; a way to check whether the research pointed at companies that later did well.",
    ])

    # ---- derived summary (computed on read, never stored)
    def summary(self) -> dict:
        open_ = [p for p in self.positions if p.status == "open" and p.value_usd is not None]
        invested = sum(p.notional_usd for p in open_)
        value = sum(p.value_usd or 0 for p in open_)
        ret = (value / invested - 1) * 100 if invested else None
        return {
            "positions": len(self.positions), "open": len(open_),
            "pending": sum(1 for p in self.positions if p.status == "pending"),
            "invested_usd": round(invested, 2), "value_usd": round(value, 2),
            "return_pct": round(ret, 2) if ret is not None else None,
            "benchmark_return_pct": self.benchmark.return_pct if self.benchmark else None,
            "best": max(open_, key=lambda p: p.return_pct or -1e9).ticker if open_ else None,
            "worst": min(open_, key=lambda p: p.return_pct or 1e9).ticker if open_ else None,
            "reports": len({p.run_id for p in self.positions}),
        }


def load_portfolio(path: Path, *, notional: float, per_report: int) -> Portfolio:
    if path.is_file():
        try:
            return Portfolio.model_validate(json.loads(path.read_text(encoding="utf-8")))
        except Exception as exc:  # noqa: BLE001
            log.warning("portfolio file unreadable (%s); starting a new one", type(exc).__name__)
    return Portfolio(notional_usd=notional, positions_per_report=per_report)


_lock = threading.Lock()


def save_portfolio(pf: Portfolio, path: Path) -> None:
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(pf.model_dump_json(indent=2), encoding="utf-8")


def add_positions_from_report(pf: Portfolio, run_id: str, report: ResearchReport) -> int:
    """Add the report's top scout candidates (with tickers) as pending positions. Returns how many were added."""
    if not report.scout or not report.scout.candidates:
        return 0
    have = {(p.run_id, p.ticker) for p in pf.positions}
    already = sum(1 for p in pf.positions if p.run_id == run_id)
    added = 0
    day = report.generated_at.astimezone(timezone.utc).date().isoformat()
    for c in report.scout.candidates:
        if already + added >= pf.positions_per_report:
            break
        if not c.ticker or (run_id, c.ticker.upper()) in have:
            continue
        pf.positions.append(Position(run_id=run_id, topic=report.topic, report_date=day, ticker=c.ticker.upper(),
                                     company=c.name, next_runner_score=c.next_runner_score, notional_usd=pf.notional_usd))
        have.add((run_id, c.ticker.upper()))
        added += 1
    if added:
        pf.updated_at = datetime.now(timezone.utc)
    return added


def sync_from_store(pf: Portfolio, store) -> int:  # noqa: ANN001  (ReportStore protocol)
    """Add positions for every saved report that has scout candidates (no network)."""
    added = 0
    for row in store.list(limit=200):
        found = store.get(row["id"])
        if found:
            added += add_positions_from_report(pf, row["id"], found[0])
    return added


def _first_on_or_after(bars: list[Bar], day: date) -> Optional[Bar]:
    return next((b for b in bars if b.day >= day), None)


def price_position(p: Position, bars: list[Bar], source_url: str) -> None:
    """Fill entry (first close on/after the report date) and the latest valuation from daily bars."""
    if not bars:
        p.status, p.note = "pending", "no price data returned"
        return
    last = bars[-1]
    if p.entry_close is None:
        entry = _first_on_or_after(bars, date.fromisoformat(p.report_date))
        if entry is None:
            p.status, p.note = "pending", f"no close on or after {p.report_date} yet (last bar {last.day.isoformat()})"
            return
        if bars[0].day > date.fromisoformat(p.report_date) and (bars[0].day - date.fromisoformat(p.report_date)).days > 7:
            # the series starts well after the report date: the true first close is not available any more
            p.note = f"price history starts {bars[0].day.isoformat()}, after the report date; entry uses that first bar"
        p.entry_date, p.entry_close = entry.day.isoformat(), entry.close
        p.shares = p.notional_usd / entry.close
    p.last_date, p.last_close = last.day.isoformat(), last.close
    p.value_usd = round((p.shares or 0) * last.close, 2)
    p.return_pct = round((last.close / p.entry_close - 1) * 100, 2) if p.entry_close else None
    p.status = "open"
    p.price_source_url = source_url
    if p.note and p.note.startswith("no close"):
        p.note = None


def update_prices(pf: Portfolio, prices: AlphaVantageClient, *, max_requests: int = 20, benchmark: str = "") -> dict:
    """Refresh every position's valuation with at most `max_requests` price lookups (cache hits are free)."""
    before = prices.requests
    errors: list[str] = []
    tickers: list[str] = []
    for p in sorted(pf.positions, key=lambda p: (p.status != "pending", p.report_date)):
        if p.ticker not in tickers:
            tickers.append(p.ticker)
    series: dict[str, list[Bar]] = {}
    for t in tickers:
        if prices.requests - before >= max_requests:
            errors.append(f"{t}: skipped, request budget ({max_requests}) used")
            continue
        try:
            series[t] = prices.daily(t)
        except SourceError as exc:
            errors.append(f"{t}: {exc.message}")
    for p in pf.positions:
        if p.ticker in series:
            price_position(p, series[p.ticker], prices.source_url(p.ticker))
        elif p.ticker and any(e.startswith(f"{p.ticker}:") for e in errors):
            p.note = next(e for e in errors if e.startswith(f"{p.ticker}:"))
            if p.status == "pending":
                p.status = "error" if "not found" in p.note else "pending"
    if benchmark and prices.requests - before < max_requests:
        entries = [p.entry_date for p in pf.positions if p.entry_date]
        if entries:
            try:
                bars = prices.daily(benchmark)
                start = _first_on_or_after(bars, date.fromisoformat(min(entries)))
                pf.benchmark = Benchmark(ticker=benchmark.upper(), entry_date=start.day.isoformat() if start else None,
                                         entry_close=start.close if start else None,
                                         last_date=bars[-1].day.isoformat() if bars else None, last_close=bars[-1].close if bars else None,
                                         return_pct=round((bars[-1].close / start.close - 1) * 100, 2) if start and bars else None,
                                         note=None if start else "benchmark series does not cover the first entry date")
            except SourceError as exc:
                pf.benchmark = Benchmark(ticker=benchmark.upper(), note=exc.message)
    pf.price_requests_last_update = prices.requests - before
    pf.prices_updated_at = pf.updated_at = datetime.now(timezone.utc)
    return {"requests": prices.requests - before, "cache_hits": prices.cache_hits, "errors": errors,
            "priced": sum(1 for p in pf.positions if p.status == "open")}


def portfolio_payload(pf: Portfolio, *, prices_configured: bool) -> dict:
    return {**pf.model_dump(mode="json"), "summary": pf.summary(), "prices_configured": prices_configured,
            "label": "simulation", "disclaimer": "Simulation of acting on the reports. No money moves. Not investment advice."}

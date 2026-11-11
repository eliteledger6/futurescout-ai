"""Which reports the report agent writes by itself (owner 2026-11-11).

One queue: the Hot-Topic Radar's ranking, without the topics that already have a fresh report. Two things take the
next topic from it:

  1. Top-N guarantee: each of the radar's top `auto_top_n` topics always has a report younger than `auto_fresh_days`.
  2. A sale funds the next report: every report sold on the report market lets the agent research the next topic in
     the queue below the top N (the agent keeps 30% of a $2-3 sale; a report costs about $0.35-0.45 to make).

At most `auto_runs_per_day` such reports a day, and one per pass of the loop, so jobs and proposals are served first.
Hires on NEAR Agent Market and visitors' proposals are separate: they are researched on request and do not use this queue.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

from app.agent_market import MarketConfig, find_recent_report


class AutoRun(BaseModel):
    at: datetime
    topic: str
    reason: str                       # "top 5" | "sale"
    run_id: Optional[str] = None
    note: str = ""


class QueueState(BaseModel):
    sales_used: Optional[int] = None  # report sales already turned into a report (None = not counted yet)
    runs: list[AutoRun] = Field(default_factory=list)

    def today(self, now: datetime) -> int:
        day = now.date()
        return sum(1 for r in self.runs if r.at.date() == day)


def load_state(path: Path) -> QueueState:
    try:
        return QueueState.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return QueueState()


def save_state(state: QueueState, path: Path) -> None:
    state.runs = state.runs[-200:]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(state.model_dump_json(indent=1), encoding="utf-8")


def sales_count(*economy_files: Path) -> int:
    """Reports sold on the report market: paid purchases in the economy record. The trading agent may run on another
    machine, so this machine's own copy and the published snapshot are both read; the larger number counts."""
    best = 0
    for f in economy_files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        best = max(best, sum(1 for p in data.get("purchases", []) if p.get("status") == "paid"))
    return best


def ranked_topics(radar: Any) -> list[str]:
    """Radar topics in rank order (unranked ones, with too small a base, are left out)."""
    rows = [t for t in (radar.topics if radar else []) if t.rank]
    return [t.topic for t in sorted(rows, key=lambda t: t.rank)]


def next_report(*, radar: Any, rows: list[dict], state: QueueState, sales: int, cfg: MarketConfig, now: datetime,
                failed_recently: tuple[str, ...] = ()) -> Optional[tuple[str, str]]:
    """-> (topic, reason) of the one report to write now, or None. `rows` = saved reports, newest first.
    Does not change `state`, except that the first call starts the sales count at today's number (earlier sales fund nothing)."""
    if cfg.auto_runs_per_day <= 0:
        return None
    if state.sales_used is None:
        state.sales_used = sales
    if state.today(now) >= cfg.auto_runs_per_day:
        return None
    fresh = MarketConfig(reuse_hours=cfg.auto_fresh_days * 24.0)
    skip = {t.lower() for t in failed_recently}
    waiting = [t for t in ranked_topics(radar) if t.lower() not in skip and find_recent_report(t, rows, fresh, now) is None]
    top = set(ranked_topics(radar)[: cfg.auto_top_n])
    for t in waiting:
        if t in top:
            return t, f"top {cfg.auto_top_n}"
    if sales > (state.sales_used or 0):
        for t in waiting:
            return t, "sale"
    return None


def failed_topics(state: QueueState, now: datetime, hours: float = 24.0) -> tuple[str, ...]:
    """Topics whose automatic run failed in the last day: not retried every minute."""
    return tuple(r.topic for r in state.runs if not r.run_id and now - r.at < timedelta(hours=hours))


def record(state: QueueState, path: Path, *, topic: str, reason: str, run_id: Optional[str], note: str, now: datetime) -> None:
    state.runs.append(AutoRun(at=now, topic=topic, reason=reason, run_id=run_id, note=note[:200]))
    if reason == "sale" and run_id:
        state.sales_used = (state.sales_used or 0) + 1          # this sale has paid for its report
    save_state(state, path)

"""Where the API reads saved reports from: PostgreSQL if DATABASE_URL is set, otherwise the report
JSON files in backend/runs/ (so the dashboard also works for someone who has no database)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional, Protocol

from sqlalchemy import select

from app.db import list_runs, load_report, make_engine, make_session_factory
from app.db.models import Run
from app.schemas.research import ResearchReport

_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def summarize(run_id: str, report: ResearchReport) -> dict:
    """Small card data for the run list (computed from the stored report)."""
    score = report.investment.score if report.investment else None
    findings = sum(len(p.findings) for p in (report.science, report.risk, report.market, report.x, report.patent, report.timing) if p is not None)
    findings += len(report.risk.challenges) if report.risk else 0
    sources = len({s.id for p in (report.science, report.risk, report.market, report.x, report.patent, report.timing) if p is not None for s in p.sources})
    return {
        "id": run_id, "topic": report.topic, "question": report.question, "sector": report.sector,
        "generated_at": report.generated_at.isoformat(),
        "agents_run": report.agents_run, "agents_not_run": report.agents_not_run,
        "score": score.score if score else None, "score_reportable": bool(score and score.reportable),
        "score_confidence": score.confidence.value if score else None,
        "coverage": score.coverage if score else None,
        "findings": findings, "sources": sources, "errors": len(report.errors),
        "total_cost_usd": report.total_cost_usd,
    }


class ReportStore(Protocol):
    kind: str

    def list(self, limit: int = 50, topic: Optional[str] = None) -> list[dict]: ...
    def get(self, run_id: str) -> Optional[tuple[ResearchReport, Optional[str]]]: ...


class DbStore:
    kind = "database"

    def __init__(self, url: str) -> None:
        self._sessions = make_session_factory(make_engine(url))

    def list(self, limit: int = 50, topic: Optional[str] = None) -> list[dict]:
        with self._sessions() as session:
            ids = [r.id for r in list_runs(session, limit=limit, topic=topic)]
            rows = session.scalars(select(Run).where(Run.id.in_(ids))).all() if ids else []
            by_id = {r.id: r for r in rows}
            return [summarize(i, ResearchReport.model_validate(by_id[i].report_json)) for i in ids if i in by_id]

    def get(self, run_id: str) -> Optional[tuple[ResearchReport, Optional[str]]]:
        with self._sessions() as session:
            run = session.get(Run, run_id)
            if run is None:
                return None
            return load_report(session, run_id), run.report_markdown


class FileStore:
    kind = "files"

    def __init__(self, runs_dir: Path) -> None:
        self.runs_dir = runs_dir
        self._cache: dict[Path, tuple[float, Optional[dict]]] = {}   # path -> (mtime, summary); reports are large

    @staticmethod
    def _id(path: Path) -> str:
        """`report_<database uuid>.json` (exported by scripts/export_site.py) keeps its database id, so links from the
        funds and trading pages (which store that id) still work; other files keep their file name as the id."""
        rest = path.stem[len("report_"):]
        return rest if _UUID.fullmatch(rest) else path.stem

    def _summaries(self) -> list[dict]:
        files = list(self.runs_dir.glob("report_*.json")) if self.runs_dir.exists() else []
        out = []
        for path in files:
            mtime = path.stat().st_mtime
            hit = self._cache.get(path)
            if hit is None or hit[0] != mtime:
                try:
                    summary = summarize(self._id(path), ResearchReport.model_validate(json.loads(path.read_text(encoding="utf-8"))))
                except Exception:  # noqa: BLE001  (a broken file is skipped, not fatal)
                    summary = None
                hit = self._cache[path] = (mtime, summary)
            if hit[1] is not None:
                out.append(hit[1])
        return sorted(out, key=lambda s: s["generated_at"], reverse=True)     # newest first

    def list(self, limit: int = 50, topic: Optional[str] = None) -> list[dict]:
        rows = [s for s in self._summaries() if not topic or topic.lower() in s["topic"].lower()]
        return rows[:limit]

    def get(self, run_id: str) -> Optional[tuple[ResearchReport, Optional[str]]]:
        if "/" in run_id or "\\" in run_id or ".." in run_id:
            return None  # only plain report file names; never arbitrary paths
        if _UUID.fullmatch(run_id):
            run_id = f"report_{run_id}"
        if not run_id.startswith("report_"):
            return None
        path = self.runs_dir / f"{run_id}.json"
        if not path.is_file():
            return None
        report = ResearchReport.model_validate(json.loads(path.read_text(encoding="utf-8")))
        md = path.with_suffix(".md")
        return report, md.read_text(encoding="utf-8") if md.is_file() else None

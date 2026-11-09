"""Where the API reads saved reports from: PostgreSQL if DATABASE_URL is set, otherwise the report
JSON files in backend/runs/ (so the dashboard also works for someone who has no database)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Protocol

from sqlalchemy import select

from app.db import list_runs, load_report, make_engine, make_session_factory
from app.db.models import Run
from app.schemas.research import ResearchReport


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

    def _files(self) -> list[Path]:
        return sorted(self.runs_dir.glob("report_*.json"), reverse=True) if self.runs_dir.exists() else []

    def list(self, limit: int = 50, topic: Optional[str] = None) -> list[dict]:
        out = []
        for path in self._files():
            try:
                report = ResearchReport.model_validate(json.loads(path.read_text(encoding="utf-8")))
            except Exception:  # noqa: BLE001  (a broken file is skipped, not fatal)
                continue
            if topic and topic.lower() not in report.topic.lower():
                continue
            out.append(summarize(path.stem, report))
            if len(out) >= limit:
                break
        return out

    def get(self, run_id: str) -> Optional[tuple[ResearchReport, Optional[str]]]:
        if not run_id.startswith("report_") or "/" in run_id or "\\" in run_id or ".." in run_id:
            return None  # only plain report file names; never arbitrary paths
        path = self.runs_dir / f"{run_id}.json"
        if not path.is_file():
            return None
        report = ResearchReport.model_validate(json.loads(path.read_text(encoding="utf-8")))
        md = path.with_suffix(".md")
        return report, md.read_text(encoding="utf-8") if md.is_file() else None

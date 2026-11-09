"""Save and load research runs. Plain functions over a SQLAlchemy Session."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ErrorRow, FindingRow, Run, Source, Usage
from app.schemas.common import Finding, SourceRecord
from app.schemas.research import ResearchReport


def _finding_row(agent: str, f: Finding, *, targets: Optional[list[str]] = None, severity: Optional[str] = None) -> FindingRow:
    return FindingRow(
        agent=agent, fid=f.fid, claim=f.claim, label=f.label.value, confidence=f.confidence.value,
        horizon=f.horizon.value, source_ids=list(f.source_ids), companies=list(f.companies),
        technologies=list(f.technologies), rationale=f.rationale, supporting_excerpt=f.supporting_excerpt,
        guard_note=f.guard_note, target_finding_ids=list(targets or []), severity=severity,
    )


def _all_sources(report: ResearchReport) -> Iterable[SourceRecord]:
    for part in (report.science, report.risk, report.market, report.x, report.patent, report.timing):
        if part is not None:
            yield from part.sources


def save_report(session: Session, report: ResearchReport, markdown: Optional[str] = None) -> str:
    """Store one run and everything in it. Returns the new run id. Caller commits."""
    from app.schemas.research import strip_control_chars
    report = strip_control_chars(report)
    if markdown:
        markdown = markdown.replace("\x00", "")
    run_id = str(uuid.uuid4())
    score = report.investment.score if report.investment else None
    run = Run(
        id=run_id, topic=report.topic, question=report.question, generated_at=report.generated_at,
        agents_run=list(report.agents_run), agents_not_run=list(report.agents_not_run),
        score=score.score if score else None, score_reportable=bool(score and score.reportable),
        score_coverage=score.coverage if score else None, total_cost_usd=report.total_cost_usd,
        report_json=report.model_dump(mode="json"), report_markdown=markdown,
    )

    seen: set[str] = set()
    for s in _all_sources(report):  # the same paper can be found by Science and Risk: store once
        if s.id in seen:
            continue
        seen.add(s.id)
        run.sources.append(Source(
            source_id=s.id, url=s.url, source_name=s.source_name, content_type=s.content_type.value,
            title=s.title, published_at=s.published_at, retrieved_at=s.retrieved_at, organization=s.organization,
            doi=s.doi, text_depth=s.text_depth, abstract=s.abstract, is_mock=s.is_mock,
        ))

    if report.science:
        run.findings += [_finding_row("science", f) for f in report.science.findings]
    if report.risk:
        run.findings += [_finding_row("risk", f) for f in report.risk.findings]
        run.findings += [_finding_row("risk_challenge", c.finding, targets=c.target_finding_ids, severity=c.severity.value)
                         for c in report.risk.challenges]
    if report.market:
        run.findings += [_finding_row("market", f) for f in report.market.findings]
    if report.x:
        run.findings += [_finding_row("x", f) for f in report.x.findings]
    if report.patent:
        run.findings += [_finding_row("patent", f) for f in report.patent.findings]
    if report.timing:
        run.findings += [_finding_row("timing", f) for f in report.timing.findings]

    run.usage = [Usage(agent=u["agent"], model=u["model"], calls=u.get("calls", 0), failed_calls=u.get("failed_calls", 0),
                       prompt_tokens=u.get("prompt_tokens", 0), completion_tokens=u.get("completion_tokens", 0),
                       cost_usd=u.get("cost_usd", 0.0)) for u in report.usage]
    run.errors = [ErrorRow(agent=e.agent, source=e.source, message=e.message, recoverable=e.recoverable)
                  for e in report.errors]
    session.add(run)
    session.flush()
    return run_id


def load_report(session: Session, run_id: str) -> Optional[ResearchReport]:
    run = session.get(Run, run_id)
    return ResearchReport.model_validate(run.report_json) if run else None


@dataclass
class RunSummary:
    id: str
    topic: str
    generated_at: datetime
    agents_run: list[str]
    score: Optional[float]
    score_reportable: bool
    total_cost_usd: float
    findings: int
    sources: int


def list_runs(session: Session, *, limit: int = 20, topic: Optional[str] = None) -> list[RunSummary]:
    query = select(Run).order_by(Run.generated_at.desc()).limit(limit)
    if topic:
        query = query.where(Run.topic.ilike(f"%{topic}%"))
    return [
        RunSummary(id=r.id, topic=r.topic, generated_at=r.generated_at, agents_run=list(r.agents_run or []),
                   score=r.score, score_reportable=r.score_reportable, total_cost_usd=r.total_cost_usd,
                   findings=len(r.findings), sources=len(r.sources))
        for r in session.scalars(query)
    ]

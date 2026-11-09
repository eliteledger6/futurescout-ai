"""Risk & Contrarian Research Agent.

Two passes:
  1. run_independent: searches for limits / contradictions / hype from the topic alone,
     without seeing the Science agent's conclusions (so it cannot just echo them).
  2. challenge: reviews the Science findings and challenges overstated or unsupported ones.
Both passes use real retrieved papers and the citation guard.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from app.agents.formatting import format_findings, title_map
from app.agents.retrieval import collect_papers, dedupe, format_papers
from app.graph.citation_guard import apply_citation_guard
from app.models.router import ModelRouter, ModelRouterError
from app.schemas.common import AgentError, Label
from app.schemas.research import (
    Challenge, ChallengeReportDraft, RiskReportDraft, RiskResult,
)
from app.schemas.science import ScienceResult
from app.sources.arxiv import ArxivClient
from app.sources.openalex import OpenAlexClient

log = logging.getLogger("futurescout.risk")

_DIR = Path(__file__).parent
DEFAULT_LOOKBACK_YEARS = 3


class RiskAgent:
    name = "risk"

    def __init__(
        self,
        router: Optional[ModelRouter],
        openalex: Optional[OpenAlexClient] = None,
        arxiv: Optional[ArxivClient] = None,
        *,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.router = router
        self.openalex = openalex
        self.arxiv = arxiv
        self._now = now

    # ------------------------------------------------------------------ pass 1
    def run_independent(
        self,
        topic: str,
        queries: list[str],
        *,
        from_year: Optional[int] = None,
        max_papers: int = 12,
        use_llm: bool = True,
    ) -> RiskResult:
        errors: list[AgentError] = []
        from_year = from_year if from_year is not None else self._now().year - DEFAULT_LOOKBACK_YEARS
        records = collect_papers(self.name, self.openalex, self.arxiv, queries, from_year, max_papers, errors)
        result = RiskResult(topic=topic, status="no_data", queries=queries, sources=records, errors=errors)

        if not records:
            result.limitations = ["No papers could be retrieved for the risk queries; no risk analysis was performed."]
            return result
        if not use_llm or self.router is None:
            result.status = "retrieval_only"
            return result

        messages = [
            {"role": "system", "content": (_DIR / "independent_prompt.md").read_text(encoding="utf-8")},
            {"role": "user", "content": (
                f"Topic: {topic}\nToday's date: {self._now().date().isoformat()}\n\n"
                f"Papers ({len(records)}):\n\n{format_papers(records)}"
            )},
        ]
        try:
            reply = self.router.complete(self.name, messages, response_model=RiskReportDraft)
        except ModelRouterError as exc:
            result.errors.append(AgentError(agent=self.name, source="model", message=f"{exc} {exc.attempts}".strip(), recoverable=True))
            result.status = "partial"
            result.limitations = ["Risk papers were retrieved but the model analysis failed."]
            return result

        report: RiskReportDraft = reply.parsed  # type: ignore[assignment]
        guarded = apply_citation_guard(report.findings, {r.id: r for r in records})
        for index, finding in enumerate(guarded.findings, start=1):
            finding.fid = f"R{index}"
        result.findings = guarded.findings
        result.guard_issues = [i.as_dict() for i in guarded.issues]
        result.hype_flags = report.hype_flags
        result.limitations = report.limitations
        result.analyzed = True
        result.status = "ok" if not result.errors else "partial"
        return result

    # ------------------------------------------------------------------ pass 2
    def challenge(self, topic: str, science: Optional[ScienceResult], risk: RiskResult) -> RiskResult:
        """Challenge the Science findings. Returns a copy of `risk` with `challenges` filled."""
        out = risk.model_copy(deep=True)
        if science is None or not science.findings:
            out.limitations.append("No Science findings were available to challenge.")
            return out
        if self.router is None:
            return out

        evidence = dedupe([*science.sources, *risk.sources])
        registry = {r.id: r for r in evidence}
        valid_targets = {f.fid for f in science.findings if f.fid}
        titles = title_map(evidence)
        messages = [
            {"role": "system", "content": (_DIR / "challenge_prompt.md").read_text(encoding="utf-8")},
            {"role": "user", "content": (
                f"Topic: {topic}\n\nScience findings to challenge:\n{format_findings(science.findings, titles)}\n\n"
                f"Your own independent risk findings (for reference):\n{format_findings(risk.findings, titles)}\n\n"
                f"Evidence available to cite ({len(evidence)} papers):\n\n{format_papers(evidence)}"
            )},
        ]
        try:
            reply = self.router.complete(self.name, messages, response_model=ChallengeReportDraft)
        except ModelRouterError as exc:
            out.errors.append(AgentError(agent=self.name, source="model", message=f"challenge pass failed: {exc} {exc.attempts}".strip(), recoverable=True))
            out.status = "partial"
            return out

        report: ChallengeReportDraft = reply.parsed  # type: ignore[assignment]
        guarded = apply_citation_guard(report.challenges, registry)
        # The guard keeps order and count, so drafts and guarded findings line up by index.
        for index, (draft, finding) in enumerate(zip(report.challenges, guarded.findings), start=1):
            finding.fid = f"C{index}"
            targets = [t for t in dict.fromkeys(draft.target_finding_ids) if t in valid_targets]
            if len(targets) != len(set(draft.target_finding_ids)):
                finding.guard_note = ((finding.guard_note + "; ") if finding.guard_note else "") + "unknown target finding id(s) removed"
            if finding.label == Label.VERIFIED_FACT:
                # A challenge is a judgement about another finding; only its quoted excerpt is verified
                # (first live run: "C2 (verified_fact) S6 is labelled verified_fact, but...").
                finding.label = Label.AI_INTERPRETATION
                finding.guard_note = ((finding.guard_note + "; ") if finding.guard_note else "") + (
                    "relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source")
            out.challenges.append(Challenge(finding=finding, target_finding_ids=targets, severity=draft.severity))
        out.guard_issues += [i.as_dict() for i in guarded.issues]
        out.limitations += report.limitations
        return out

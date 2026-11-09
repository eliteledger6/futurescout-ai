"""Science Research Agent.

Flow (deliberately code-driven so retrieval cannot be skipped or faked):
  1. fetch papers from OpenAlex and arXiv with real API clients
  2. register every paper in a source registry (ids/URLs come only from the APIs)
  3. compute paper counts per year + Research Acceleration in code
  4. ask the model (via the router) for a structured analysis that cites paper ids
  5. run the citation guard; anything unsupported is downgraded, not kept as fact
If retrieval returns nothing, the model is NOT called and the result says "no_data".
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from app.agents.retrieval import collect_papers, dedupe, format_papers  # noqa: F401  (re-exported)
from app.agents.science.metrics import compute_acceleration, ytd_from_client
from app.graph.citation_guard import apply_citation_guard
from app.models.router import ModelRouter, ModelRouterError
from app.schemas.common import AgentError, SourceRecord
from app.schemas.science import ScienceReport, ScienceResult
from app.sources.arxiv import ArxivClient
from app.sources.base import SourceError
from app.sources.openalex import OpenAlexClient, clean_phrase

log = logging.getLogger("futurescout.science")

DEFAULT_LOOKBACK_YEARS = 3

_PROMPT_PATH = Path(__file__).with_name("prompt.md")


class ScienceAgent:
    name = "science"

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

    # ------------------------------------------------------------------
    def run(
        self,
        topic: str,
        *,
        queries: Optional[list[str]] = None,
        from_year: Optional[int] = None,
        max_papers: int = 15,
        use_llm: bool = True,
    ) -> ScienceResult:
        queries = queries or [topic]
        errors: list[AgentError] = []
        current_year = self._now().year
        # Investment horizon is 1-5 years, so default to papers from the last 3 years.
        from_year = from_year if from_year is not None else current_year - DEFAULT_LOOKBACK_YEARS

        records = self._collect(queries, from_year, max_papers, errors)
        counts = self._counts(topic, current_year - 6, errors)
        registry = {r.id: r for r in records}

        result = ScienceResult(
            topic=topic,
            from_year=from_year,
            status="no_data",
            sources=records,
            publication_counts=counts,
            acceleration=compute_acceleration(counts, current_year, phrase=clean_phrase(topic)),
            ytd=self._ytd(topic, errors),
            errors=errors,
            coverage_note=(
                "Based on titles, metadata and abstracts only. No full text was read. "
                "arXiv items are preprints and are not peer reviewed."
            ),
        )

        if not records:
            result.limitations = ["No papers could be retrieved; no analysis was performed."]
            return result

        if not use_llm or self.router is None:
            result.status = "retrieval_only"
            result.coverage_note += " Model analysis was skipped (retrieval only)."
            return result

        messages = [
            {"role": "system", "content": _PROMPT_PATH.read_text(encoding="utf-8")},
            {"role": "user", "content": (
                f"Topic: {topic}\nToday's date: {self._now().date().isoformat()}\n\n"
                f"Papers ({len(records)}):\n\n{format_papers(records)}"
            )},
        ]
        try:
            reply = self.router.complete(self.name, messages, response_model=ScienceReport)
        except ModelRouterError as exc:
            # Append to result.errors: pydantic copied the list when `result` was built.
            result.errors.append(AgentError(
                agent=self.name, source="model", message=f"{exc} {exc.attempts}".strip(), recoverable=True
            ))
            result.status = "partial"
            result.limitations = ["Papers were retrieved but the model analysis failed."]
            return result

        report: ScienceReport = reply.parsed  # type: ignore[assignment]
        guarded = apply_citation_guard(report.findings, registry)
        for index, finding in enumerate(guarded.findings, start=1):
            finding.fid = f"S{index}"
        result.findings = guarded.findings
        result.guard_issues = [i.as_dict() for i in guarded.issues]
        result.emerging_directions = report.emerging_directions
        result.open_problems = report.open_problems
        result.limitations = report.limitations
        result.llm_alias = reply.llm_alias
        result.status = "ok" if not result.errors else "partial"
        return result

    # ------------------------------------------------------------------
    def _collect(
        self, queries: list[str], from_year: Optional[int], max_papers: int, errors: list[AgentError]
    ) -> list[SourceRecord]:
        return collect_papers(self.name, self.openalex, self.arxiv, queries, from_year, max_papers, errors)

    def _ytd(self, topic: str, errors: list[AgentError]):  # noqa: ANN202
        if not self.openalex:
            return None
        try:
            return ytd_from_client(self.openalex, clean_phrase(topic), self._now().date())
        except SourceError as exc:
            errors.append(AgentError(agent=self.name, source=exc.source, message=f"year-to-date count: {exc.message}", recoverable=exc.retryable))
            return None

    def _counts(self, topic: str, start_year: int, errors: list[AgentError]) -> dict[int, int]:
        if not self.openalex:
            return {}
        try:
            return self.openalex.count_by_year(topic, start_year)
        except SourceError as exc:
            errors.append(AgentError(agent=self.name, source=exc.source, message=exc.message, recoverable=exc.retryable))
            return {}

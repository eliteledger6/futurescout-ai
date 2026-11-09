"""Patent Intelligence Agent (Google Patents via SerpApi, or EPO Open Patent Services; worldwide).

Flow (code-driven, like the Science agent):
  1. count patent publications per year whose title/abstract mention the topic terms, and compute
     Patent Acceleration in code (never by a model)
  2. fetch the most recent matching publications (title, applicants, date, abstract)
  3. count top applicants among them (code)
  4. the model writes findings citing publication ids; the citation guard checks quoted excerpts
     against the abstract. Findings ids: P1, P2...
If nothing is retrieved, the model is NOT called ("no_data").
"""

from __future__ import annotations

import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from app.agents.market.agent import clean_keywords
from app.agents.science.metrics import compute_acceleration
from app.graph.citation_guard import apply_citation_guard
from app.models.router import ModelRouter, ModelRouterError
from app.schemas.common import AgentError, SourceRecord
from app.schemas.patent import PatentReport, PatentResult
from app.sources.base import SourceError
from typing import Union

from app.sources.epo import EpoOpsClient
from app.sources.serpapi_patents import SerpApiPatentsClient

PatentClient = Union[EpoOpsClient, SerpApiPatentsClient]

log = logging.getLogger("futurescout.patent")

_PROMPT_PATH = Path(__file__).with_name("prompt.md")
LOOKBACK_YEARS = 3
COUNT_YEARS = 4   # years counted before the current one (each year = 1 request; SerpApi quota is small)
ABSTRACT_CHARS = 1200


def format_patents(records: list[SourceRecord]) -> str:
    return "\n\n".join(
        f"id: {r.id}\ntitle: {r.title}\napplicants: {', '.join(r.authors) or 'unknown'}\n"
        f"published: {r.published_at or 'unknown'} | type: {r.publication_type} | text_depth: {r.text_depth}\n"
        f"abstract: {(r.abstract or '(no abstract available)')[:ABSTRACT_CHARS]}"
        for r in records
    )


class PatentAgent:
    name = "patent"

    def __init__(
        self,
        router: Optional[ModelRouter],
        client: Optional["PatentClient"],
        *,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.router = router
        self.client = client
        self._now = now

    def run(self, topic: str, *, keywords: Optional[list[str]] = None, max_results: int = 25, use_llm: bool = True) -> PatentResult:
        terms = clean_keywords([topic, *(keywords or [])])[:4]
        year = self._now().year
        result = PatentResult(
            topic=topic, status="no_data", terms=terms,
            coverage_note=(
                f"Worldwide patent publications from {getattr(self.client, 'SOURCE', 'the patent source')} matching the "
                "search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications "
                "include applications, which are claims of invention, not proof that a technology works. Patents are "
                "published about 18 months after filing, so the latest years are undercounted."
            ),
        )
        if self.client is None:
            result.limitations = ["Patents were not searched (no patent source configured: SERPAPI_API_KEY or EPO keys)."]
            return result

        try:
            result.publication_counts = self.client.count_by_year(terms, year - COUNT_YEARS)
            result.acceleration = compute_acceleration(result.publication_counts, year)
            if result.acceleration:
                result.acceleration.basis = (
                    f"{getattr(self.client, 'SOURCE', 'Patent')} publications per publication year matching any of {terms} "
                    "(worldwide, applications and grants, one family can count several times). Recent years are "
                    "undercounted because of the ~18-month publication delay. The current partial year is excluded."
                )
        except SourceError as exc:
            result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"counts: {exc.message}", recoverable=exc.retryable))
        try:
            result.total_matches, docs = self.client.search(terms, from_year=year - LOOKBACK_YEARS, max_results=max_results)
        except SourceError as exc:
            result.errors.append(AgentError(agent=self.name, source=exc.source, message=exc.message, recoverable=exc.retryable))
            docs = []
        result.sources = docs
        result.source_usage = {k: getattr(self.client, k) for k in ("searches_used", "cache_hits", "requests") if hasattr(self.client, k)}
        counter = Counter(a for d in docs for a in d.authors[:1])   # first applicant per publication
        result.top_applicants = counter.most_common(8)

        if not docs:
            result.status = "partial" if result.errors else "no_data"
            result.limitations = ["No patent publications could be retrieved; no analysis was performed."]
            return result
        if not use_llm or self.router is None:
            result.status = "retrieval_only"
            return result

        counts_line = ", ".join(f"{y}: {c}" for y, c in sorted(result.publication_counts.items())) or "unavailable"
        apps_line = ", ".join(f"{n} ({c})" for n, c in result.top_applicants) or "unknown"
        messages = [
            {"role": "system", "content": _PROMPT_PATH.read_text(encoding="utf-8")},
            {"role": "user", "content": (
                f"Topic: {topic}\nSearch terms: {', '.join(terms)}\nToday's date: {self._now().date().isoformat()}\n"
                f"Publications per year (computed by code): {counts_line}\n"
                f"Most frequent first applicants among the {len(docs)} retrieved publications (computed by code): {apps_line}\n\n"
                f"Patent publications ({len(docs)} most recent of {result.total_matches} since {year - LOOKBACK_YEARS}):\n\n"
                f"{format_patents(docs)}"
            )},
        ]
        try:
            reply = self.router.complete(self.name, messages, response_model=PatentReport)
        except ModelRouterError as exc:
            result.errors.append(AgentError(agent=self.name, source="model", message=f"{exc} {exc.attempts}".strip(), recoverable=True))
            result.status = "partial"
            result.limitations = ["Patents were retrieved but the model analysis failed."]
            return result

        report: PatentReport = reply.parsed  # type: ignore[assignment]
        guarded = apply_citation_guard(report.findings, {r.id: r for r in docs})
        for index, finding in enumerate(guarded.findings, start=1):
            finding.fid = f"P{index}"
        result.findings = guarded.findings
        result.guard_issues = [i.as_dict() for i in guarded.issues]
        result.limitations = report.limitations
        result.llm_alias = reply.llm_alias
        result.status = "ok" if not result.errors else "partial"
        return result

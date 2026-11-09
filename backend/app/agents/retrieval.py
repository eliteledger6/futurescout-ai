"""Paper retrieval shared by the Science and Risk agents (real API clients only)."""

from __future__ import annotations

import re
from itertools import zip_longest
from typing import Optional

from app.schemas.common import AgentError, SourceRecord
from app.sources.arxiv import ArxivClient
from app.sources.base import SourceError
from app.sources.openalex import OpenAlexClient

ABSTRACT_CHARS = 1500


def _title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def dedupe(records: list[SourceRecord]) -> list[SourceRecord]:
    """Drop repeats by DOI or normalised title; keeps first occurrence."""
    seen: set[str] = set()
    unique: list[SourceRecord] = []
    for rec in records:
        keys = {_title_key(rec.title)}
        if rec.doi:
            keys.add("doi:" + rec.doi.lower())
        if keys & seen:
            continue
        seen |= keys
        unique.append(rec)
    return unique


def format_papers(records: list[SourceRecord]) -> str:
    """Numbered-by-id text block given to a model. Only real retrieved data goes in."""
    blocks = []
    for rec in records:
        abstract = (rec.abstract or "(no abstract available)")[:ABSTRACT_CHARS]
        blocks.append(
            f"id: {rec.id}\n"
            f"title: {rec.title}" + (" [RETRACTED by the publisher: do not rely on it]" if rec.is_retracted else "") + "\n"
            f"source: {rec.source_name} | type: {rec.publication_type or 'unknown'} | "
            f"published: {rec.published_at or 'unknown'} | venue: {rec.venue or 'unknown'} | "
            f"cited_by: {rec.cited_by_count if rec.cited_by_count is not None else 'n/a'} | "
            f"text_depth: {rec.text_depth}\n"
            f"abstract: {abstract}"
        )
    return "\n\n".join(blocks)


def collect_papers(
    agent: str,
    openalex: Optional[OpenAlexClient],
    arxiv: Optional[ArxivClient],
    queries: list[str],
    from_year: Optional[int],
    max_papers: int,
    errors: list[AgentError],
) -> list[SourceRecord]:
    """Search both sources for every query. Failures become AgentErrors, never fake data."""
    openalex_hits: list[SourceRecord] = []
    arxiv_hits: list[SourceRecord] = []
    for query in queries:
        if openalex:
            try:
                openalex_hits += openalex.search_works(query, from_year=from_year, per_page=max_papers)
            except SourceError as exc:
                errors.append(AgentError(agent=agent, source=exc.source, message=exc.message, recoverable=exc.retryable))
        if arxiv:
            try:
                arxiv_hits += arxiv.search(query, max_results=max_papers, from_year=from_year)
            except SourceError as exc:
                errors.append(AgentError(agent=agent, source=exc.source, message=exc.message, recoverable=exc.retryable))
    # Interleave so neither source crowds out the other, then dedupe and cap.
    mixed = [r for pair in zip_longest(openalex_hits, arxiv_hits) for r in pair if r is not None]
    return dedupe(mixed)[:max_papers]

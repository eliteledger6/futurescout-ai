"""Structured output of the Science Research Agent."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.common import AgentError, Finding, FindingDraft, SourceRecord


class ScienceReport(BaseModel):
    """What the model must return (validated before use)."""

    findings: list[FindingDraft] = Field(default_factory=list)
    emerging_directions: list[str] = Field(default_factory=list)
    open_problems: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class AccelerationMetric(BaseModel):
    """Research Acceleration, computed by code from OpenAlex counts (not by a model)."""

    last_full_year: int
    last_full_year_count: int
    previous_year: int
    previous_year_count: int
    yoy_growth_pct: Optional[float] = None
    basis: str = (
        "Number of OpenAlex works matching the search text per publication year. "
        "Not normalised for overall growth in publishing; the current (partial) year is excluded."
    )


class YtdMetric(BaseModel):
    """Year-to-date momentum: papers from 1 January to `cutoff` this year vs the SAME dates last year (code-computed).

    Catches a topic that is collapsing (or exploding) during the current, unfinished year, which the full-year
    comparison cannot see until next January. The cutoff sits LAG_DAYS before today because OpenAlex needs weeks to
    index new papers; using the same cutoff for both years keeps the comparison fair.
    """

    year: int
    previous_year: int
    cutoff: str                      # MM-DD, inclusive, applied to both years
    count: int
    previous_count: int
    growth_pct: Optional[float] = None
    trend: Optional[Literal["rising", "flat", "cooling"]] = None
    basis: str = ""


class ScienceResult(BaseModel):
    topic: str
    from_year: Optional[int] = None  # earliest publication year searched for papers
    status: Literal["ok", "partial", "no_data", "retrieval_only"]
    sources: list[SourceRecord] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    emerging_directions: list[str] = Field(default_factory=list)
    open_problems: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    coverage_note: str = ""
    publication_counts: dict[int, int] = Field(default_factory=dict)
    acceleration: Optional[AccelerationMetric] = None
    ytd: Optional[YtdMetric] = None   # same-period comparison inside the current year (added 2026-11-09)
    errors: list[AgentError] = Field(default_factory=list)
    guard_issues: list[dict] = Field(default_factory=list)
    llm_alias: Optional[str] = None

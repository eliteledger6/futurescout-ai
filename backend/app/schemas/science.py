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
    errors: list[AgentError] = Field(default_factory=list)
    guard_issues: list[dict] = Field(default_factory=list)
    llm_alias: Optional[str] = None

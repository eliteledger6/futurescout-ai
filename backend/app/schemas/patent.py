"""Structured output of the Patent Intelligence Agent."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.common import AgentError, Finding, FindingDraft, SourceRecord
from app.schemas.science import AccelerationMetric


class PatentReport(BaseModel):
    """What the model must return (validated before use)."""

    findings: list[FindingDraft] = Field(default_factory=list)
    top_applicants_note: Optional[str] = None
    limitations: list[str] = Field(default_factory=list)


class PatentResult(BaseModel):
    topic: str
    status: Literal["ok", "partial", "no_data", "retrieval_only"]
    terms: list[str] = Field(default_factory=list)
    total_matches: Optional[int] = None                       # publications matching since from_year
    publication_counts: dict[int, int] = Field(default_factory=dict)
    acceleration: Optional[AccelerationMetric] = None          # Patent Acceleration (code-computed)
    top_applicants: list[tuple[str, int]] = Field(default_factory=list)  # among retrieved documents
    sources: list[SourceRecord] = Field(default_factory=list)
    source_usage: dict = Field(default_factory=dict)          # e.g. SerpApi searches used / cache hits
    findings: list[Finding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    coverage_note: str = ""
    errors: list[AgentError] = Field(default_factory=list)
    guard_issues: list[dict] = Field(default_factory=list)
    llm_alias: Optional[str] = None

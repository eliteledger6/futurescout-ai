"""Structured output of the Market Intelligence Agent."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.common import AgentError, Finding, FindingDraft, SourceRecord


class MarketReport(BaseModel):
    """What the model must return (validated before use)."""

    findings: list[FindingDraft] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class CompanyCheck(BaseModel):
    """What retrieval found for one configured company (computed by code, not a model)."""

    ticker: str
    name: str
    filings_checked: int = 0
    filings_with_mentions: int = 0
    error: Optional[str] = None
    discovered: bool = False                 # found by SEC full-text search, not on the configured list
    mentions_in_search: Optional[int] = None  # filings in the search window that mention the topic
    cik: Optional[int] = None
    press_releases_read: int = 0              # 8-K EX-99 exhibits read
    fundamentals: Optional[dict] = None       # SEC XBRL: revenue, growth, R&D, size class (computed by code)


class MarketResult(BaseModel):
    topic: str
    status: Literal["ok", "partial", "no_data", "retrieval_only"]
    keywords: list[str] = Field(default_factory=list)
    companies: list[CompanyCheck] = Field(default_factory=list)
    news_query: Optional[str] = None
    sources: list[SourceRecord] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    coverage_note: str = ""
    errors: list[AgentError] = Field(default_factory=list)
    guard_issues: list[dict] = Field(default_factory=list)
    llm_alias: Optional[str] = None

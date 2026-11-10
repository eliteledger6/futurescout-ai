"""Structured output of the Company Scout (code only: no model is involved).

The scout answers the owner's question "which companies are actually working on this, and could a
smaller one be the next runner?" It collects company names from three real places (patent assignees,
company-type author affiliations on papers, SEC filings that mention the topic), matches them to the
SEC's own ticker file, pulls XBRL fundamentals and computes a transparent heuristic score.

The score is a FORECAST-labelled heuristic, never a recommendation.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.common import AgentError, Finding


class CompanySignal(BaseModel):
    name: str                                   # display name (SEC title when matched, else as found)
    aliases: list[str] = Field(default_factory=list)  # raw names seen in sources that were merged into this company
    ticker: Optional[str] = None
    cik: Optional[int] = None
    sec_listed: bool = False                    # matched to the SEC ticker file
    incumbent: bool = False                     # explicitly passed as a known big name (none by default since 2026-11-10)
    patents: int = 0                            # retrieved patent publications naming it as assignee
    patent_source_ids: list[str] = Field(default_factory=list)
    papers: int = 0                             # retrieved papers with an author affiliated to it
    paper_source_ids: list[str] = Field(default_factory=list)
    filings: int = 0                            # SEC reports in the search window mentioning the topic
    filing_source_ids: list[str] = Field(default_factory=list)
    fundamentals: Optional[dict] = None         # SEC XBRL (code-computed); None when not available
    fundamentals_error: Optional[str] = None
    sic: Optional[str] = None                   # SEC industry code from the company's submissions record
    industry: Optional[str] = None              # its description, e.g. "Semiconductors & Related Devices"
    off_sector: bool = False                    # finance / insurance / retail etc.: topic mentions are usually risk-factor boilerplate
    next_runner_score: Optional[float] = None   # 0-100 heuristic (forecast), only for SEC-listed companies
    score_reasons: list[str] = Field(default_factory=list)
    signal_types: int = 0                       # how many of patents / papers / filings are non-zero

    @property
    def all_source_ids(self) -> list[str]:
        return [*self.patent_source_ids, *self.paper_source_ids, *self.filing_source_ids]


class ScoutResult(BaseModel):
    topic: str
    status: Literal["ok", "partial", "no_data"]
    candidates: list[CompanySignal] = Field(default_factory=list)   # SEC-listed, not on the incumbent list, by score
    incumbents: list[CompanySignal] = Field(default_factory=list)   # configured big names that also showed up
    unlisted: list[CompanySignal] = Field(default_factory=list)     # found, but not in the SEC ticker file (private / foreign)
    findings: list[Finding] = Field(default_factory=list)           # K1.. one per top candidate, code-written
    basis: str = ""                                                  # how the score is computed (shown to readers)
    coverage_note: str = ""
    limitations: list[str] = Field(default_factory=list)
    errors: list[AgentError] = Field(default_factory=list)
    lookups: int = 0                                                 # SEC XBRL requests made

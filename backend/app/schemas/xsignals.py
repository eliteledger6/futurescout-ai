"""Structured output of the X Intelligence Agent (social signals from approved accounts)."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.common import AgentError, Finding, FindingDraft, SourceRecord


class XReport(BaseModel):
    """What the model must return (validated before use)."""

    findings: list[FindingDraft] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class XResult(BaseModel):
    topic: str
    status: Literal["ok", "partial", "no_data", "retrieval_only"]
    keywords: list[str] = Field(default_factory=list)
    accounts: list[str] = Field(default_factory=list)      # approved handles searched
    query: Optional[str] = None
    sources: list[SourceRecord] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    coverage_note: str = ""
    x_usage: dict = Field(default_factory=dict)            # posts/users read and estimated X cost
    suggested_accounts: list[dict] = Field(default_factory=list)   # accounts the agent found posting on the topic
    watchlist_changes: list[str] = Field(default_factory=list)     # adds/removes the agent made (auto_manage on)
    errors: list[AgentError] = Field(default_factory=list)
    guard_issues: list[dict] = Field(default_factory=list)
    llm_alias: Optional[str] = None

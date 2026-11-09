"""Price & timing risk (part of the Risk agent). Numbers are computed by code; never a buy/sell signal."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.common import AgentError, Finding, FindingDraft, SourceRecord


class PriceMetrics(BaseModel):
    ticker: str
    company: str
    source_id: str
    last_date: str
    last_close: float
    bars: int
    window_start: str
    return_1m_pct: Optional[float] = None
    return_3m_pct: Optional[float] = None
    vs_50d_avg_pct: Optional[float] = None
    volatility_20d_pct: Optional[float] = None
    from_window_high_pct: float
    from_window_low_pct: float
    timing_risk: str
    reasons: list[str] = Field(default_factory=list)
    high_volatility: bool = False
    closes: list[float] = Field(default_factory=list)   # daily closes in the window, oldest first (for the chart); added 2026-11-09


class TimingReport(BaseModel):
    findings: list[FindingDraft] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class PriceTimingResult(BaseModel):
    status: str = "no_data"
    metrics: list[PriceMetrics] = Field(default_factory=list)
    sources: list[SourceRecord] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    coverage_note: str = ""
    requests_used: int = 0
    errors: list[AgentError] = Field(default_factory=list)
    llm_alias: Optional[str] = None

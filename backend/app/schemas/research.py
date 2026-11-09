"""Structured outputs for the Chief, Risk and Investment agents and the final report."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.common import AgentError, Confidence, Finding, FindingDraft, Horizon, Label, SourceRecord
from app.schemas.market import MarketResult
from app.schemas.science import ScienceResult
from app.schemas.patent import PatentResult
from app.schemas.scout import ScoutResult
from app.schemas.timing import PriceTimingResult
from app.schemas.xsignals import XResult


# ---------------------------------------------------------------- Chief
class ResearchPlan(BaseModel):
    source: Literal["model", "default"] = "model"  # "default" = the model failed and a plain plan was used
    topic_summary: str
    science_queries: list[str] = Field(min_length=1, max_length=6)
    risk_queries: list[str] = Field(min_length=1, max_length=6)
    # terms looked for in company filings / news (e.g. abbreviations such as "HBM")
    market_keywords: list[str] = Field(default_factory=list, max_length=8)
    key_questions: list[str] = Field(default_factory=list)


class GapReview(BaseModel):
    sufficient: bool
    gaps: list[str] = Field(default_factory=list)
    extra_science_queries: list[str] = Field(default_factory=list, max_length=3)


# ---------------------------------------------------------------- Risk
class RiskReportDraft(BaseModel):
    findings: list[FindingDraft] = Field(default_factory=list)
    hype_flags: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class ChallengeDraft(FindingDraft):
    target_finding_ids: list[str] = Field(default_factory=list)  # science findings being challenged
    severity: Confidence = Confidence.MEDIUM                      # how serious the problem is


class ChallengeReportDraft(BaseModel):
    challenges: list[ChallengeDraft] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class Challenge(BaseModel):
    finding: Finding
    target_finding_ids: list[str]
    severity: Confidence


class RiskResult(BaseModel):
    topic: str
    status: Literal["ok", "partial", "no_data", "retrieval_only"]
    analyzed: bool = False  # True once a model analysis of the retrieved papers succeeded
    queries: list[str] = Field(default_factory=list)
    sources: list[SourceRecord] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    hype_flags: list[str] = Field(default_factory=list)
    challenges: list[Challenge] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    errors: list[AgentError] = Field(default_factory=list)
    guard_issues: list[dict] = Field(default_factory=list)


# ---------------------------------------------------------------- Investment
class Referenced(BaseModel):
    """Something that must point at findings by id. Code checks the ids (see investment agent)."""

    label: Label = Label.AI_INTERPRETATION
    finding_ids: list[str] = Field(default_factory=list)
    note: Optional[str] = None  # set by code when the reference check changed something


class Evidenced(Referenced):
    text: str


class ScenarioDraft(Referenced):
    label: Label = Label.FORECAST
    narrative: str


class HorizonView(Referenced):
    label: Label = Label.FORECAST
    horizon: Horizon
    assessment: str
    confidence: Confidence = Confidence.LOW


class CompanyMention(Referenced):
    name: str
    relevance: str


class ThesisDraft(BaseModel):
    name: str
    technologies: list[str] = Field(default_factory=list)
    horizons: list[HorizonView] = Field(default_factory=list)
    bull: ScenarioDraft
    base: ScenarioDraft
    bear: ScenarioDraft
    catalysts: list[Evidenced] = Field(default_factory=list)
    risks: list[Evidenced] = Field(default_factory=list)
    companies: list[CompanyMention] = Field(default_factory=list)
    invalidation_conditions: list[Evidenced] = Field(default_factory=list)
    conflicting_evidence: list[Evidenced] = Field(default_factory=list)


class DimensionRatingDraft(Referenced):
    dimension: str                       # key from scoring.yaml, e.g. "research_momentum"
    rating: Optional[int] = None         # 0-5, or null when the evidence cannot support a rating
    confidence: Confidence = Confidence.LOW
    rationale: str = ""


class InvestmentDraft(BaseModel):
    summary: str
    themes: list[ThesisDraft] = Field(default_factory=list)
    dimension_ratings: list[DimensionRatingDraft] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class DimensionScore(BaseModel):
    key: str
    label: str
    weight: float
    status: Literal["scored", "missing"]
    rating: Optional[int] = None
    confidence: Optional[Confidence] = None
    rationale: str = ""
    finding_ids: list[str] = Field(default_factory=list)
    missing_reason: Optional[str] = None


class OpportunityScore(BaseModel):
    reportable: bool
    score: Optional[float] = None          # 0-100 after risk adjustment; None if nothing was scored
    base_score: Optional[float] = None     # before risk adjustment
    coverage: float = 0.0                  # share of total weight that has cited evidence
    confidence: Confidence = Confidence.LOW
    risk_rating: Optional[int] = None
    risk_penalty_pct: Optional[float] = None
    commercialization_gap: Optional[float] = None  # momentum rating minus readiness rating (-5..5)
    dimensions: list[DimensionScore] = Field(default_factory=list)
    missing_dimensions: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    formula: str = ""


class InvestmentResult(BaseModel):
    topic: str
    status: Literal["ok", "partial", "no_data"]
    draft: Optional[InvestmentDraft] = None
    score: Optional[OpportunityScore] = None
    reference_issues: list[dict] = Field(default_factory=list)
    errors: list[AgentError] = Field(default_factory=list)


# ---------------------------------------------------------------- Final report
class ResearchReport(BaseModel):
    topic: str
    question: Optional[str] = None
    sector: Optional[str] = None                 # key from config/sectors.yaml (added 2026-11-09; digest ignores None)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agents_run: list[str] = Field(default_factory=list)
    agents_not_run: list[str] = Field(default_factory=list)
    plan: Optional[ResearchPlan] = None
    gap_reviews: list[GapReview] = Field(default_factory=list)
    science: Optional[ScienceResult] = None
    risk: Optional[RiskResult] = None
    market: Optional[MarketResult] = None
    x: Optional[XResult] = None
    patent: Optional[PatentResult] = None
    timing: Optional[PriceTimingResult] = None   # price & timing risk (part of the Risk agent)
    scout: Optional[ScoutResult] = None          # Company Scout: emerging companies from patents, papers and filings
    investment: Optional[InvestmentResult] = None
    usage: list[dict] = Field(default_factory=list)
    total_cost_usd: float = 0.0
    chain_record: Optional[dict] = None  # NEAR testnet fingerprint record (excluded from the fingerprint itself)
    errors: list[AgentError] = Field(default_factory=list)

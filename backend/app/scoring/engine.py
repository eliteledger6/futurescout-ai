"""Explainable Semiconductor Technology Opportunity Score.

Plain code, no model. Models only supply 0-5 ratings that must cite findings; this module
turns those ratings into a number and refuses to hide gaps:
  * a dimension without cited evidence is "missing", never silently zero
  * the score is only "reportable" when enough of the total weight has evidence
  * every dimension, weight, rating, rationale and missing reason is returned
The weights are initial assumptions (config/scoring.yaml). This is not a validated
predictor of stock performance.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import yaml
from pydantic import BaseModel, model_validator

from app.config import CONFIG_DIR
from app.schemas.common import Confidence
from app.schemas.research import DimensionRatingDraft, DimensionScore, OpportunityScore


class DimensionConfig(BaseModel):
    label: str
    weight: float


class RiskAdjustmentConfig(BaseModel):
    label: str = "Risk Adjustment"
    max_penalty: float = 0.30


class ScoringConfig(BaseModel):
    dimensions: dict[str, DimensionConfig]
    risk_adjustment: RiskAdjustmentConfig = RiskAdjustmentConfig()
    min_coverage_to_report: float = 0.5
    confidence_thresholds: dict[str, float] = {"medium": 0.6, "high": 0.85}

    @model_validator(mode="after")
    def _weights_sum_to_one(self) -> "ScoringConfig":
        total = sum(d.weight for d in self.dimensions.values())
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"dimension weights must sum to 1.0 (got {total:.4f})")
        return self


def load_scoring_config(path: Optional[Path] = None) -> ScoringConfig:
    with open(path or (CONFIG_DIR / "scoring.yaml"), "r", encoding="utf-8") as fh:
        return ScoringConfig.model_validate(yaml.safe_load(fh))


RISK_KEY = "risk_adjustment"
_CONF_VALUE = {Confidence.LOW: 0, Confidence.MEDIUM: 1, Confidence.HIGH: 2}

FORMULA = (
    "base = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100; "
    "score = base x (1 - max_penalty x risk_rating/5). Dimensions without cited findings are "
    "'missing', not zero."
)


def _valid_rating(rating: Optional[int]) -> bool:
    return isinstance(rating, int) and not isinstance(rating, bool) and 0 <= rating <= 5


def compute_opportunity_score(
    ratings: Iterable[DimensionRatingDraft],
    valid_finding_ids: set[str],
    config: ScoringConfig,
) -> OpportunityScore:
    by_key: dict[str, DimensionRatingDraft] = {}
    notes: list[str] = [
        "Weights are initial assumptions, not fitted to data. The score is an explainable "
        "heuristic, not a validated prediction of stock performance.",
        "Sources are de-duplicated by URL/DOI/title. A single announcement reported by several "
        "outlets is not yet merged into one event.",
    ]
    for r in ratings:
        if r.dimension in by_key:
            notes.append(f"Duplicate rating for '{r.dimension}' ignored (first one kept).")
        elif r.dimension != RISK_KEY and r.dimension not in config.dimensions:
            notes.append(f"Unknown dimension '{r.dimension}' ignored.")
        else:
            by_key[r.dimension] = r

    def checked(key: str) -> tuple[Optional[DimensionRatingDraft], list[str], Optional[str]]:
        """Returns (rating, valid cited ids, missing_reason)."""
        draft = by_key.get(key)
        if draft is None:
            return None, [], "not rated (no agent supplied evidence for this dimension)"
        ids = [i for i in dict.fromkeys(draft.finding_ids) if i in valid_finding_ids]
        if not _valid_rating(draft.rating):
            return None, ids, "no valid 0-5 rating given"
        if not ids:
            return None, [], "rating had no valid cited finding, so it was not used"
        return draft, ids, None

    dims: list[DimensionScore] = []
    scored_weight = 0.0
    weighted_sum = 0.0
    ratings_by_key: dict[str, int] = {}
    for key, dc in config.dimensions.items():
        draft, ids, reason = checked(key)
        if draft is None:
            dims.append(DimensionScore(key=key, label=dc.label, weight=dc.weight, status="missing", missing_reason=reason))
            continue
        assert draft.rating is not None
        scored_weight += dc.weight
        weighted_sum += dc.weight * draft.rating / 5
        ratings_by_key[key] = draft.rating
        dims.append(DimensionScore(
            key=key, label=dc.label, weight=dc.weight, status="scored", rating=draft.rating,
            confidence=draft.confidence, rationale=draft.rationale, finding_ids=ids,
        ))

    total_weight = sum(d.weight for d in config.dimensions.values())
    coverage = round(scored_weight / total_weight, 4) if total_weight else 0.0
    missing = [d.label for d in dims if d.status == "missing"]

    thresholds = config.confidence_thresholds
    confidence = Confidence.LOW
    if coverage >= thresholds.get("high", 0.85):
        confidence = Confidence.HIGH
    elif coverage >= thresholds.get("medium", 0.6):
        confidence = Confidence.MEDIUM
    # Coverage alone is not confidence: wide but weak evidence must not read as "high"
    # (first live run, 2026-11-08: 90% coverage gave "high" although most ratings were low/medium).
    scored = [d for d in dims if d.status == "scored"]
    if scored:
        avg = sum(_CONF_VALUE[d.confidence or Confidence.LOW] * d.weight for d in scored) / sum(d.weight for d in scored)
        evidence_conf = Confidence.HIGH if avg >= 1.5 else Confidence.MEDIUM if avg >= 0.75 else Confidence.LOW
        if _CONF_VALUE[evidence_conf] < _CONF_VALUE[confidence]:
            notes.append(f"Confidence lowered to '{evidence_conf.value}': coverage is {coverage:.0%}, but the cited "
                         "ratings themselves are mostly of lower confidence.")
            confidence = evidence_conf

    base_score = score = risk_rating = penalty_pct = None
    if scored_weight > 0:
        base_score = round(weighted_sum / scored_weight * 100, 1)
        risk_draft, _, risk_reason = checked(RISK_KEY)
        if risk_draft is not None:
            assert risk_draft.rating is not None
            risk_rating = risk_draft.rating
            penalty = config.risk_adjustment.max_penalty * risk_rating / 5
            penalty_pct = round(penalty * 100, 1)
            score = round(base_score * (1 - penalty), 1)
        else:
            score = base_score
            notes.append(f"Risk adjustment NOT applied: {risk_reason}. Confidence capped at medium.")
            if confidence == Confidence.HIGH:
                confidence = Confidence.MEDIUM

    reportable = score is not None and coverage >= config.min_coverage_to_report
    if score is not None and not reportable:
        notes.append(
            f"Only {coverage:.0%} of the total weighting has cited evidence (minimum "
            f"{config.min_coverage_to_report:.0%}). The number is indicative only and must not be "
            "compared with other technologies."
        )
    if score is None:
        notes.append("No dimension had cited evidence, so no score was computed.")

    gap = None
    if "research_momentum" in ratings_by_key and "commercial_readiness" in ratings_by_key:
        gap = float(ratings_by_key["research_momentum"] - ratings_by_key["commercial_readiness"])

    return OpportunityScore(
        reportable=reportable, score=score, base_score=base_score, coverage=coverage,
        confidence=confidence, risk_rating=risk_rating, risk_penalty_pct=penalty_pct,
        commercialization_gap=gap, dimensions=dims, missing_dimensions=missing, notes=notes,
        formula=FORMULA,
    )

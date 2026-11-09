"""Explainable Technology Opportunity Score and Confidence.

Plain code, no model. Models only supply 0-5 ratings that must cite findings; this module turns those ratings into
two numbers and refuses to hide gaps:
  * a dimension without cited evidence is "missing", never silently zero
  * the score is only "reportable" when enough of the total weight has evidence
  * every dimension, weight, rating, rationale and missing reason is returned

Method v2 (owner decision 2026-11-09): "how good does it look" and "how sure are we" are separate numbers.
  OPPORTUNITY SCORE (0-100) = weighted average of the evidenced dimension ratings. Risk no longer cuts it: an
      unproven technology already scores low on commercial readiness, customers and supply chain, so the old
      30% risk penalty counted the same weakness twice.
  CONFIDENCE (0-100%) = evidence confidence x risk multiplier
      evidence confidence = coverage, the confidence of the cited ratings, and the share of verified facts among
          the findings (weights in config/scoring.yaml)
      risk multiplier = 1 - 0.10 x risk rating  (risk 1 -> x0.9, 2 -> x0.8, ... 5 -> x0.5)
The weights are initial assumptions (config/scoring.yaml). Neither number is a validated predictor of stock
performance, and confidence is not a probability of profit.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import yaml
from pydantic import BaseModel, model_validator

from app.config import CONFIG_DIR
from app.schemas.common import Confidence
from app.schemas.research import DimensionRatingDraft, DimensionScore, OpportunityScore

SCORING_VERSION = 2


class DimensionConfig(BaseModel):
    label: str
    weight: float


class RiskAdjustmentConfig(BaseModel):
    label: str = "Risk"
    step: float = 0.10                # confidence multiplier = 1 - step x risk rating
    min_multiplier: float = 0.5


class ScoringConfig(BaseModel):
    dimensions: dict[str, DimensionConfig]
    risk_adjustment: RiskAdjustmentConfig = RiskAdjustmentConfig()
    min_coverage_to_report: float = 0.5
    confidence_weights: dict[str, float] = {"coverage": 0.40, "rating_confidence": 0.35, "verified_share": 0.25}
    confidence_labels: dict[str, float] = {"medium": 45.0, "high": 70.0}     # confidence % needed for each label

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
_CONF_VALUE = {Confidence.LOW: 0.0, Confidence.MEDIUM: 0.5, Confidence.HIGH: 1.0}

FORMULA = (
    "score = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100 (risk does not reduce it). "
    "confidence = evidence confidence x (1 - 0.10 x risk rating), where evidence confidence combines evidence "
    "coverage, the confidence of the cited ratings and the share of verified facts. Dimensions without cited "
    "findings are 'missing', not zero."
)


def _valid_rating(rating: Optional[int]) -> bool:
    return isinstance(rating, int) and not isinstance(rating, bool) and 0 <= rating <= 5


def risk_multiplier(risk_rating: Optional[int], config: ScoringConfig) -> float:
    if risk_rating is None:
        return 1.0
    return round(max(config.risk_adjustment.min_multiplier, 1 - config.risk_adjustment.step * risk_rating), 2)


def finalize_score(
    dims: list[DimensionScore],
    risk_rating: Optional[int],
    config: ScoringConfig,
    *,
    verified_share: Optional[float] = None,
    notes: Optional[list[str]] = None,
    risk_missing_reason: Optional[str] = None,
) -> OpportunityScore:
    """Turn already-checked dimension scores into the two numbers. Also used to re-score a stored report."""
    notes = list(notes or [])
    scored = [d for d in dims if d.status == "scored" and d.rating is not None]
    total_weight = sum(d.weight for d in dims)
    scored_weight = sum(d.weight for d in scored)
    coverage = round(scored_weight / total_weight, 4) if total_weight else 0.0
    missing = [d.label for d in dims if d.status == "missing"]

    score = base_score = None
    evidence_conf = confidence_pct = mult = None
    confidence = Confidence.LOW
    if scored_weight > 0:
        base_score = score = round(sum(d.weight * d.rating / 5 for d in scored) / scored_weight * 100, 1)
        rating_conf = sum(_CONF_VALUE[d.confidence or Confidence.LOW] * d.weight for d in scored) / scored_weight
        parts = {"coverage": coverage, "rating_confidence": rating_conf}
        if verified_share is not None:
            parts["verified_share"] = max(0.0, min(1.0, verified_share))
        w = {k: config.confidence_weights.get(k, 0.0) for k in parts}
        wsum = sum(w.values()) or 1.0
        evidence_conf = round(sum(parts[k] * w[k] for k in parts) / wsum * 100, 1)
        mult = risk_multiplier(risk_rating, config)
        confidence_pct = round(evidence_conf * mult, 1)
        labels = config.confidence_labels
        if confidence_pct >= labels.get("high", 70.0):
            confidence = Confidence.HIGH
        elif confidence_pct >= labels.get("medium", 45.0):
            confidence = Confidence.MEDIUM
        if risk_rating is None:
            notes.append(f"Risk was NOT applied to confidence: {risk_missing_reason or 'no risk rating'}. Confidence capped at medium.")
            if confidence == Confidence.HIGH:
                confidence = Confidence.MEDIUM
        if verified_share is None:
            notes.append("Share of verified facts was not available; confidence uses coverage and rating confidence only.")

    reportable = score is not None and coverage >= config.min_coverage_to_report
    if score is not None and not reportable:
        notes.append(
            f"Only {coverage:.0%} of the total weighting has cited evidence (minimum "
            f"{config.min_coverage_to_report:.0%}). The number is indicative only and must not be "
            "compared with other technologies."
        )
    if score is None:
        notes.append("No dimension had cited evidence, so no score was computed.")

    by = {d.key: d.rating for d in scored}
    gap = None
    if "research_momentum" in by and "commercial_readiness" in by:
        gap = float(by["research_momentum"] - by["commercial_readiness"])

    return OpportunityScore(
        reportable=reportable, score=score, base_score=base_score, coverage=coverage,
        confidence=confidence, risk_rating=risk_rating, risk_penalty_pct=None,
        confidence_pct=confidence_pct, evidence_confidence_pct=evidence_conf, risk_multiplier=mult,
        scoring_version=SCORING_VERSION if score is not None else None,
        commercialization_gap=gap, dimensions=dims, missing_dimensions=missing, notes=notes,
        formula=FORMULA,
    )


BASE_NOTES = [
    "Weights are initial assumptions, not fitted to data. Score and confidence are explainable heuristics, not a "
    "validated prediction of stock performance; confidence is not a probability of profit.",
    "Sources are de-duplicated by URL/DOI/title. A single announcement reported by several "
    "outlets is not yet merged into one event.",
]


def compute_opportunity_score(
    ratings: Iterable[DimensionRatingDraft],
    valid_finding_ids: set[str],
    config: ScoringConfig,
    verified_share: Optional[float] = None,
) -> OpportunityScore:
    by_key: dict[str, DimensionRatingDraft] = {}
    notes: list[str] = list(BASE_NOTES)
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
    for key, dc in config.dimensions.items():
        draft, ids, reason = checked(key)
        if draft is None:
            dims.append(DimensionScore(key=key, label=dc.label, weight=dc.weight, status="missing", missing_reason=reason))
            continue
        dims.append(DimensionScore(
            key=key, label=dc.label, weight=dc.weight, status="scored", rating=draft.rating,
            confidence=draft.confidence, rationale=draft.rationale, finding_ids=ids,
        ))
    risk_draft, _, risk_reason = checked(RISK_KEY)
    return finalize_score(dims, risk_draft.rating if risk_draft is not None else None, config,
                          verified_share=verified_share, notes=notes, risk_missing_reason=risk_reason)


def rescore_existing(score: OpportunityScore, config: ScoringConfig, verified_share: Optional[float] = None) -> OpportunityScore:
    """Re-run the arithmetic on a stored score (same ratings, same evidence) with the current method. No model."""
    keep = [n for n in score.notes if n.startswith(("Duplicate rating", "Unknown dimension"))]
    return finalize_score(list(score.dimensions), score.risk_rating, config, verified_share=verified_share,
                          notes=[*BASE_NOTES, *keep], risk_missing_reason="no valid risk rating in the stored report")


def verified_share_of(findings: Iterable) -> Optional[float]:
    """Share of findings labelled verified_fact (0-1), or None when there are no findings."""
    labels = [getattr(getattr(f, "label", None), "value", getattr(f, "label", None)) for f in findings]
    return round(sum(1 for x in labels if x == "verified_fact") / len(labels), 4) if labels else None


def report_findings(report) -> list:  # noqa: ANN001
    """Every finding of a stored report (the same set the Investment agent saw)."""
    out: list = []
    for part in ("science", "risk", "market", "x", "patent", "timing", "scout"):
        res = getattr(report, part, None)
        out.extend(getattr(res, "findings", None) or [])
    if report.risk:
        out.extend(c.finding for c in report.risk.challenges)
    return out

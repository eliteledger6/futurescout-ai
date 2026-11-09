import pytest
from pydantic import ValidationError

from app.schemas.common import Confidence
from app.schemas.research import DimensionRatingDraft
from app.scoring import ScoringConfig, compute_opportunity_score, load_scoring_config

CFG = load_scoring_config()
VALID = {"S1", "S2", "R1"}


def rating(dim, value, ids=("S1",), conf=Confidence.MEDIUM):
    return DimensionRatingDraft(dimension=dim, rating=value, finding_ids=list(ids), confidence=conf, rationale="because")


def test_config_weights_sum_to_one_and_has_eight_dimensions():
    assert len(CFG.dimensions) == 8
    assert sum(d.weight for d in CFG.dimensions.values()) == pytest.approx(1.0)


def test_bad_weights_are_rejected():
    with pytest.raises(ValidationError, match="sum to 1.0"):
        ScoringConfig(dimensions={"a": {"label": "A", "weight": 0.5}})


def test_wide_but_weak_evidence_does_not_read_as_high_confidence():
    """First live run: 90% coverage was shown as 'confidence: high' although ratings were low/medium."""
    low = [rating(k, 4, conf=Confidence.LOW) for k in CFG.dimensions] + [rating("risk_adjustment", 2, conf=Confidence.LOW)]
    s = compute_opportunity_score(low, VALID, CFG)
    assert s.coverage == 1.0 and s.confidence == Confidence.LOW and any("Confidence lowered" in n for n in s.notes)
    mixed = [rating(k, 4, conf=Confidence.MEDIUM) for k in CFG.dimensions] + [rating("risk_adjustment", 2)]
    assert compute_opportunity_score(mixed, VALID, CFG).confidence == Confidence.MEDIUM


def test_partial_evidence_gives_indicative_score_that_is_not_reportable():
    ratings = [rating("research_momentum", 4), rating("technical_feasibility", 3, ("R1",)), rating("risk_adjustment", 2, ("R1",))]
    s = compute_opportunity_score(ratings, VALID, CFG)
    assert s.coverage == pytest.approx(0.30)
    assert s.base_score == 70.0           # (0.15*4/5 + 0.15*3/5) / 0.30 * 100
    assert s.risk_penalty_pct == 12.0     # 30% max * 2/5
    assert s.score == 61.6
    assert s.reportable is False and s.confidence == Confidence.LOW
    assert len(s.missing_dimensions) == 6
    assert any("indicative only" in n for n in s.notes)


def test_full_coverage_is_reportable_and_weighted_correctly():
    ratings = [rating(k, 5, conf=Confidence.HIGH) for k in CFG.dimensions] + [rating("risk_adjustment", 0)]
    s = compute_opportunity_score(ratings, VALID, CFG)
    assert s.reportable and s.score == 100.0 and s.coverage == 1.0 and s.confidence == Confidence.HIGH
    ratings = [rating(k, 0) for k in CFG.dimensions] + [rating("risk_adjustment", 5)]
    assert compute_opportunity_score(ratings, VALID, CFG).score == 0.0
    ratings = [rating(k, 5) for k in CFG.dimensions] + [rating("risk_adjustment", 5)]
    assert compute_opportunity_score(ratings, VALID, CFG).score == 70.0  # full marks minus the 30% maximum penalty


def test_rating_without_valid_cited_finding_is_missing_not_zero():
    s = compute_opportunity_score([rating("research_momentum", 5, ("S99",))], VALID, CFG)
    assert s.score is None and s.coverage == 0
    dim = next(d for d in s.dimensions if d.key == "research_momentum")
    assert dim.status == "missing" and "no valid cited finding" in dim.missing_reason
    assert any("No dimension had cited evidence" in n for n in s.notes)


def test_null_or_out_of_range_rating_is_missing():
    s = compute_opportunity_score([rating("research_momentum", None), rating("technical_feasibility", 9)], VALID, CFG)
    assert s.score is None and s.coverage == 0


def test_missing_risk_adjustment_is_noted_and_caps_confidence():
    s = compute_opportunity_score([rating(k, 5) for k in CFG.dimensions], VALID, CFG)
    assert s.risk_rating is None and s.score == s.base_score == 100.0
    assert s.confidence == Confidence.MEDIUM  # would be HIGH at full coverage
    assert any("Risk adjustment NOT applied" in n for n in s.notes)


def test_duplicates_and_unknown_dimensions_are_ignored_with_notes():
    s = compute_opportunity_score(
        [rating("research_momentum", 5), rating("research_momentum", 0), rating("made_up", 5)], VALID, CFG)
    assert next(d for d in s.dimensions if d.key == "research_momentum").rating == 5
    assert any("Duplicate" in n for n in s.notes) and any("Unknown dimension" in n for n in s.notes)


def test_commercialization_gap_needs_both_ratings():
    both = compute_opportunity_score([rating("research_momentum", 5), rating("commercial_readiness", 2)], VALID, CFG)
    assert both.commercialization_gap == 3.0
    only_one = compute_opportunity_score([rating("research_momentum", 5)], VALID, CFG)
    assert only_one.commercialization_gap is None

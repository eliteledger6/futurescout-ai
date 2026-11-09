"""The verdict is computed by code from a finished report: bands, qualifiers, plain words, nothing invented."""

from app.report import render_markdown
from app.report.verdict import build_verdict
from app.schemas.research import ResearchReport
from app.schemas.timing import PriceMetrics, PriceTimingResult
from tests.test_db import fixture_report


def test_verdict_uses_only_what_the_report_contains():
    report = fixture_report()
    v = build_verdict(report)
    assert v["available"] and v["label"] == "forecast" and "not advice" in v["disclaimer"]
    assert v["band"] in {"strong", "building", "early", "weak", "insufficient"}
    if v["score"] is not None:
        assert v["band"] != "insufficient"
    for line in v["why"] + v["watch"] + v["change"]:
        assert isinstance(line, str) and line
    assert v["plain"]                                   # falls back to the first sentences of the summary
    # timing qualifier appears when most related stocks look stretched
    report.timing = PriceTimingResult(status="ok", metrics=[
        PriceMetrics(ticker="A", company="A Co", source_id="s", last_date="2026-11-01", last_close=1, bars=100, window_start="2026-06-01",
                     from_window_high_pct=-1, from_window_low_pct=50, timing_risk="elevated", reasons=["up 60% over 3 months"])])
    v2 = build_verdict(report)
    assert any("already run hard" in q for q in v2["qualifiers"])
    md = render_markdown(report)
    assert "## Verdict (forecast, computed from the report)" in md and v2["headline"] in md and "names no entry point" in md


def test_verdict_without_an_assessment_is_honest():
    v = build_verdict(ResearchReport(topic="x"))
    assert v["available"] is False and "No verdict" in v["headline"]


def test_confidence_below_70_is_always_stated_first():
    r = fixture_report()
    sc = r.investment.score
    sc.confidence_pct, sc.score, sc.reportable = 47.0, 72.0, True
    v = build_verdict(r)
    assert v["band"] == "strong" and "confidence 47%" in v["qualifiers"][0] and "70%" in v["qualifiers"][0]
    assert v["confidence_pct"] == 47.0
    sc.confidence_pct = 81.0
    assert not any("counts as confident" in q for q in build_verdict(r)["qualifiers"])

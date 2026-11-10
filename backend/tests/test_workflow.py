"""End-to-end graph tests. Network and models are FAKED (fixtures + scripted mock model)."""

from datetime import datetime, timezone

import httpx
import openai
import pytest

from app.config import ConfigError, Settings
from app.graph import workflow
from app.models.config import load_model_config
from app.models.router import ModelRouter
from app.report import render_markdown
from app.schemas.common import make_source_id
from app.sources.arxiv import ArxivClient
from app.sources.base import RateLimiter
from app.sources.openalex import OpenAlexClient
from tests.helpers import FakeClient, Scripted, load_json, load_text, status_error

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
PAPER_A = make_source_id("https://doi.org/10.0000/fixture.001")
ARXIV_D = make_source_id("https://arxiv.org/abs/0000.00001v1")


def clients(oa_ok=True, ax_ok=True):
    def oa(request):
        if not oa_ok:
            return httpx.Response(409)
        body = load_json("openalex_group_by.json") if "group_by" in request.url.params else load_json("openalex_works.json")
        return httpx.Response(200, json=body)

    def ax(request):
        return httpx.Response(200, text=load_text("arxiv_feed.xml")) if ax_ok else httpx.Response(404)

    return (
        OpenAlexClient("k", http=httpx.Client(transport=httpx.MockTransport(oa)), sleep=lambda s: None, now=lambda: NOW),
        ArxivClient(http=httpx.Client(transport=httpx.MockTransport(ax)), limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW),
    )


def replies(**override):
    scenario = lambda text, ids: {"narrative": text, "finding_ids": ids}  # noqa: E731
    base = {
        "ResearchPlan": {"topic_summary": "s", "science_queries": ["chiplet interconnect", "fixture stacking"],
                         "risk_queries": ["chiplet interconnect limitations"], "key_questions": ["q"]},
        "GapReview": [{"sufficient": False, "gaps": ["thin on thermal"], "extra_science_queries": ["fixture thermal"]},
                      {"sufficient": True, "gaps": [], "extra_science_queries": []}],
        "ScienceReport": {
            "findings": [
                {"claim": "A synthetic interconnect reaches fixture bandwidth targets.", "label": "verified_fact", "confidence": "medium",
                 "source_ids": [PAPER_A], "supporting_excerpt": "We report a synthetic interconnect reaching fixture bandwidth"},
                {"claim": "Stacking work appears to centre on thermal limits.", "label": "ai_interpretation", "confidence": "low",
                 "source_ids": [ARXIV_D], "rationale": "one preprint"}],
            "emerging_directions": ["d"], "open_problems": ["thermal"], "limitations": ["abstracts only"]},
        "RiskReportDraft": {
            "findings": [{"claim": "Fixture stacking is limited by thermal limits.", "label": "verified_fact", "confidence": "medium",
                          "source_ids": [ARXIV_D], "supporting_excerpt": "stacking memory dies with fixture thermal limits"}],
            "hype_flags": ["bandwidth headlines ignore thermal cost"], "limitations": ["few papers"]},
        "ChallengeReportDraft": {
            "challenges": [
                {"claim": "S1 rests on a single synthetic abstract.", "label": "ai_interpretation", "confidence": "medium",
                 "severity": "high", "target_finding_ids": ["S1", "S99"], "source_ids": [PAPER_A]},
                {"claim": "This challenge quotes text that is not in any source.", "label": "verified_fact", "confidence": "high",
                 "severity": "low", "target_finding_ids": [], "source_ids": [ARXIV_D], "supporting_excerpt": "never written anywhere at all"}],
            "limitations": ["abstracts only"]},
        "InvestmentDraft": {
            "summary": "Evidence is thin and abstract-only.",
            "themes": [{
                "name": "Chiplet interconnect", "technologies": ["chiplet"],
                "horizons": [{"horizon": "near_0_12m", "assessment": "n", "finding_ids": ["S1"], "confidence": "low"},
                             {"horizon": "medium_1_3y", "assessment": "m", "finding_ids": ["S2", "R1"], "confidence": "low"}],
                "bull": scenario("bull", ["S1"]), "base": scenario("base", ["S1", "S77"]), "bear": scenario("bear", ["R1", "C1"]),
                "catalysts": [{"text": "cat", "finding_ids": ["S1"]}], "risks": [{"text": "r", "finding_ids": ["R1"]}],
                "invalidation_conditions": [{"text": "inv", "finding_ids": ["C1"]}], "conflicting_evidence": [{"text": "conf", "finding_ids": ["C1", "S1"]}],
                "companies": [{"name": "Invented Co", "relevance": "x", "finding_ids": []}]}],
            "dimension_ratings": [
                {"dimension": "research_momentum", "rating": 4, "finding_ids": ["S1"], "confidence": "medium", "rationale": "rm"},
                {"dimension": "technical_feasibility", "rating": 3, "finding_ids": ["R1"], "confidence": "low", "rationale": "tf"},
                {"dimension": "commercial_readiness", "rating": 3, "finding_ids": ["S99"], "confidence": "low", "rationale": "uncited"},
                {"dimension": "risk_adjustment", "rating": 2, "finding_ids": ["R1"], "confidence": "medium", "rationale": "ra"}],
            "missing_data": ["patent, market and X evidence"], "limitations": ["thin"]},
    }
    base.update(override)
    return base


def run(script, *, oa_ok=True, ax_ok=True):
    client = FakeClient(script)
    router = ModelRouter(load_model_config(), Settings(near_ai_api_key="k", _env_file=None),
                         client_factory=lambda s: client, sleep=lambda s: None)
    oa, ax = clients(oa_ok, ax_ok)
    report = workflow.run_research("chiplet interconnect", router=router, openalex=oa, arxiv=ax, max_papers=10, now=lambda: NOW)
    return report, client


def test_full_pipeline_with_one_gap_round_checks_everything():
    script = Scripted(replies())
    report, client = run(script)

    assert report.agents_run == ["chief", "science", "risk", "investment"]
    assert report.agents_not_run == ["patent", "market", "x"]
    # Chief reviewed twice and requested exactly one extra Science round (bounded loop)
    assert script.calls["GapReview"] == 2 and script.calls["ScienceReport"] == 2
    assert script.calls["ResearchPlan"] == 1 and script.calls["ChallengeReportDraft"] == 1 and script.calls["InvestmentDraft"] == 1
    assert len(report.gap_reviews) == 2

    sci, risk, inv = report.science, report.risk, report.investment
    assert [f.fid for f in sci.findings] == ["S1", "S2"] and [f.fid for f in risk.findings] == ["R1"]
    assert sci.findings[0].label.value == "verified_fact"
    # challenges: bad target removed; fabricated excerpt downgraded; ids assigned
    c1, c2 = risk.challenges
    assert c1.finding.fid == "C1" and c1.target_finding_ids == ["S1"] and "unknown target" in c1.finding.guard_note
    assert c2.finding.label.value == "unverified_claim"
    # investment: invented ids / companies removed, score computed and honest about coverage
    theme = inv.draft.themes[0]
    assert theme.base.finding_ids == ["S1"] and theme.companies == []
    assert [v.horizon.value for v in theme.horizons] == ["near_0_12m", "medium_1_3y", "long_3_5y"]
    sc = inv.score
    assert sc.coverage == pytest.approx(0.30) and sc.reportable is False and sc.score == 70.0 and sc.risk_multiplier == 0.8   # v2: risk lowers confidence, not the score
    assert next(d for d in sc.dimensions if d.key == "commercial_readiness").status == "missing"
    # usage is tracked per agent
    assert {u["agent"] for u in report.usage} == {"chief", "science", "risk", "investment"} and report.total_cost_usd > 0

    md = render_markdown(report)
    assert "Research information only, not investment advice" in md
    assert "Agents NOT run in this version: patent, market, x" in md
    assert "Not reportable" in md and "indicative" in md.lower()
    assert "https://doi.org/10.0000/fixture.001" in md and "https://arxiv.org/abs/0000.00001v1" in md
    assert "Bull case" in md and "Bear case" in md and "What would invalidate this thesis" in md
    assert "no company evidence" in md
    # invented ids never appear as references; the report only mentions them in the "removed" notes
    assert "[S1, S77]" not in md and "S99]" not in md and "removed: S77" in md


def test_a_challenge_with_a_real_quote_is_still_an_interpretation_not_a_fact():
    challenge = {"challenges": [
        {"claim": "S1 overstates a single synthetic abstract.", "label": "verified_fact", "confidence": "high",
         "severity": "medium", "target_finding_ids": ["S1"], "source_ids": [PAPER_A],
         "supporting_excerpt": "We report a synthetic interconnect reaching fixture bandwidth"}], "limitations": []}
    report, _ = run(Scripted(replies(ChallengeReportDraft=challenge)))
    [c1] = report.risk.challenges
    assert c1.finding.label.value == "ai_interpretation" and c1.finding.supporting_excerpt
    assert "a challenge is a judgement" in c1.finding.guard_note


def test_gap_loop_is_bounded_even_if_chief_always_asks_for_more():
    always_more = {"sufficient": False, "gaps": ["still thin"], "extra_science_queries": ["another new query"]}
    script = Scripted(replies(GapReview=always_more))
    report, _ = run(script)
    assert script.calls["GapReview"] == 2 and script.calls["ScienceReport"] == 2  # one extra round, then it moves on
    assert report.agents_run[-1] == "investment"


def test_model_down_everywhere_degrades_gracefully_without_crashing_or_inventing():
    report, client = run(lambda n, kw: status_error(openai.BadRequestError, 400, "model unavailable"))
    assert report.investment.status == "no_data" and report.investment.draft is None
    # No model analysis succeeded anywhere, so no agent may be reported as having produced output,
    # even though papers were retrieved and the Chief used a default plan.
    assert report.agents_run == [] and report.plan.source == "default"
    assert len(report.science.sources) > 0 and len(report.risk.sources) > 0
    assert report.science.findings == [] and report.risk.findings == []
    assert any(e.source == "model" for e in report.errors)
    md = render_markdown(report)  # still renders
    assert "No assessment was generated" in md and "ERROR" in md


def test_data_sources_down_means_no_model_analysis_and_no_findings():
    script = Scripted(replies())
    report, _ = run(script, oa_ok=False, ax_ok=False)
    assert script.calls["ScienceReport"] == 0 and script.calls["RiskReportDraft"] == 0 and script.calls["InvestmentDraft"] == 0
    assert report.science.status == "no_data" and report.investment.status == "no_data"
    assert {e.source for e in report.errors} >= {"OpenAlex", "arXiv"}


def test_one_crashing_agent_is_recorded_and_the_rest_continue(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("simulated bug in risk agent")

    monkeypatch.setattr(workflow.RiskAgent, "run_independent", boom)
    report, _ = run(Scripted(replies()))
    assert any(e.agent == "risk_independent" and "simulated bug" in e.message for e in report.errors)
    assert report.risk is None and "science" in report.agents_run and report.investment.draft is not None


def test_missing_credentials_stop_loudly_instead_of_failing_every_node():
    router = ModelRouter(load_model_config(), Settings(_env_file=None, near_ai_api_key=None))
    oa, ax = clients()
    with pytest.raises(ConfigError):
        workflow.run_research("x", router=router, openalex=oa, arxiv=ax)


def test_market_runs_after_science_and_patent_and_receives_their_results():
    """The Market agent reads the filings of the companies the papers and patents point to, so it must get those results."""
    from app.schemas.market import MarketResult
    seen = {}

    class FakeMarket:
        companies = None

        def run(self, topic, *, keywords=None, science=None, patent=None, **kw):
            seen["science"], seen["patent"] = science, patent
            return MarketResult(topic=topic, status="retrieval_only", keywords=keywords or [])
    client = FakeClient(Scripted(replies()))
    router = ModelRouter(load_model_config(), Settings(near_ai_api_key="k", _env_file=None), client_factory=lambda s: client, sleep=lambda s: None)
    oa, ax = clients(True, True)
    report = workflow.run_research("chiplet interconnect", router=router, openalex=oa, arxiv=ax, max_papers=10, now=lambda: NOW, market_agent=FakeMarket())
    assert seen["science"] is not None and seen["science"].findings           # Science had finished before Market ran
    assert seen["patent"] is None                                              # no Patent agent in this test: passed as None, not skipped
    assert report.market is not None and report.market.status == "retrieval_only"

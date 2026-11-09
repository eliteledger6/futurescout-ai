from app.agents.chief.agent import ChiefAgent, clean_queries, fallback_plan
from app.agents.investment.agent import InvestmentAgent, validate_draft
from app.config import Settings
from app.models.config import load_model_config
from app.models.router import ModelRouter
from app.schemas.common import Confidence, Horizon, Label
from app.schemas.research import InvestmentDraft
from tests.helpers import FakeClient, Scripted, make_response, status_error

import openai


def make_router(handler):
    client = FakeClient(handler)
    return ModelRouter(load_model_config(), Settings(near_ai_api_key="k", _env_file=None),
                       client_factory=lambda s: client, sleep=lambda s: None), client


def scenario(text="x", ids=("S1",), label="forecast"):
    return {"narrative": text, "finding_ids": list(ids), "label": label}


def draft_dict(**over):
    base = {
        "summary": "s",
        "themes": [{
            "name": "T", "technologies": [], "horizons": [
                {"horizon": "near_0_12m", "assessment": "a", "finding_ids": ["S1"], "confidence": "low"}],
            "bull": scenario(), "base": scenario(ids=["S1", "S77"]), "bear": scenario(ids=[]),
            "catalysts": [{"text": "c", "finding_ids": ["S1"], "label": "verified_fact"}],
            "risks": [], "invalidation_conditions": [], "conflicting_evidence": [],
            "companies": [{"name": "Real Co", "relevance": "named in S1", "finding_ids": ["S1"]},
                          {"name": "Invented Co", "relevance": "no evidence", "finding_ids": []}],
        }],
        "dimension_ratings": [], "missing_data": [], "limitations": [],
    }
    base.update(over)
    return base


# ---------------- reference validation ----------------
def test_validate_draft_fixes_ids_labels_horizons_and_drops_unsupported_companies():
    draft, issues = validate_draft(InvestmentDraft.model_validate(draft_dict()), {"S1"})
    theme = draft.themes[0]
    assert theme.base.finding_ids == ["S1"] and "unknown finding id" in theme.base.note
    assert theme.bear.label == Label.ASSUMPTION and "no supporting finding" in theme.bear.note
    assert theme.bull.label == Label.FORECAST and theme.bull.note is None
    assert theme.catalysts[0].label == Label.AI_INTERPRETATION  # verified_fact is not allowed here
    assert [c.name for c in theme.companies] == ["Real Co"]     # invented company dropped
    assert [v.horizon for v in theme.horizons] == [Horizon.NEAR, Horizon.MEDIUM, Horizon.LONG]
    assert theme.horizons[2].label == Label.ASSUMPTION and "missing" in theme.horizons[2].note
    actions = {i["action"] for i in issues}
    assert {"removed_unknown_finding_ids", "no_supporting_finding", "company_dropped"} <= actions


def test_investment_agent_without_findings_does_not_call_the_model():
    router, client = make_router(lambda n, kw: make_response("{}"))
    result = InvestmentAgent(router).run("topic", None, None, agents_not_run=["patent"])
    assert result.status == "no_data" and result.draft is None and len(client.calls) == 0
    assert result.errors[0].source == "inputs"


# ---------------- chief ----------------
def test_clean_queries_dedupes_trims_and_limits():
    out = clean_queries(["  hbm   stacking ", "HBM stacking", "", "x" * 200, "a", "b", "c"], limit=3, exclude=["a"])
    assert out == ["hbm stacking", "b", "c"]


def test_chief_plan_puts_topic_first_and_cleans_queries():
    plan_reply = {"topic_summary": "s", "science_queries": ["hbm packaging", "HBM", "hbm packaging"],
                  "risk_queries": ["hbm thermal limits"], "key_questions": []}
    router, _ = make_router(Scripted({"ResearchPlan": plan_reply}))
    plan, errors = ChiefAgent(router).plan("HBM")
    assert plan.science_queries == ["HBM", "hbm packaging"] and plan.risk_queries == ["hbm thermal limits"] and errors == []


def test_chief_plan_falls_back_when_model_fails():
    router, _ = make_router(lambda n, kw: status_error(openai.BadRequestError, 400, "no"))
    plan, errors = ChiefAgent(router).plan("HBM")
    assert plan == fallback_plan("HBM") and errors[0].source == "model" and errors[0].recoverable


def test_chief_review_removes_repeated_queries_and_clears_extras_when_sufficient():
    plan = fallback_plan("HBM")
    reply = {"sufficient": False, "gaps": ["g"], "extra_science_queries": ["HBM", "hbm yield", "HBM limitations"]}
    router, _ = make_router(Scripted({"GapReview": reply}))
    review, _ = ChiefAgent(router).review("HBM", plan, None, None, agents_not_run=["patent"])
    assert review.extra_science_queries == ["hbm yield"]  # 'HBM' and 'HBM limitations' were already planned
    router2, _ = make_router(Scripted({"GapReview": {"sufficient": True, "gaps": [], "extra_science_queries": ["more"]}}))
    review2, _ = ChiefAgent(router2).review("HBM", plan, None, None, agents_not_run=[])
    assert review2.extra_science_queries == []


def test_chief_review_failure_means_no_extra_round():
    router, _ = make_router(lambda n, kw: status_error(openai.BadRequestError, 400, "no"))
    review, errors = ChiefAgent(router).review("HBM", fallback_plan("HBM"), None, None, agents_not_run=[])
    assert review.sufficient and review.extra_science_queries == [] and errors


def test_investment_prompt_has_anchored_risk_scale():
    # 2026-11-09: without anchors the model gave risk 4 to all 8 live topics (a flat 24% cut).
    from app.agents.investment.agent import _PROMPT_PATH
    text = _PROMPT_PATH.read_text(encoding="utf-8")
    assert "RISK SCALE" in text
    for level in range(6):
        assert f"- {level} = " in text, f"risk level {level} has no description"
    assert "Do not default to the same level" in text

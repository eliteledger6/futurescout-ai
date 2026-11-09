"""Science Agent tests. Network and model are FAKED (fixtures + mock model): no real data here."""

import json
from datetime import datetime, timezone

import httpx

from app.agents.science import ScienceAgent
from app.config import Settings
from app.models.config import load_model_config
from app.models.router import ModelRouter
from app.schemas.common import make_source_id
from app.sources.arxiv import ArxivClient
from app.sources.base import RateLimiter
from app.sources.openalex import OpenAlexClient
from tests.helpers import FakeClient, load_json, load_text, make_response, status_error

import openai

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
PAPER_A = make_source_id("https://doi.org/10.0000/fixture.001")


def build_agent(*, openalex_ok=True, arxiv_ok=True, model_handler=None):
    def oa_handler(request):
        if not openalex_ok:
            return httpx.Response(409)
        if "group_by" in request.url.params:
            return httpx.Response(200, json=load_json("openalex_group_by.json"))
        return httpx.Response(200, json=load_json("openalex_works.json"))

    def ax_handler(request):
        return httpx.Response(200, text=load_text("arxiv_feed.xml")) if arxiv_ok else httpx.Response(404)

    oa = OpenAlexClient("k", http=httpx.Client(transport=httpx.MockTransport(oa_handler)), sleep=lambda s: None, now=lambda: NOW)
    ax = ArxivClient(http=httpx.Client(transport=httpx.MockTransport(ax_handler)), limiter=RateLimiter(0),
                     sleep=lambda s: None, now=lambda: NOW)
    client = FakeClient(model_handler or (lambda n, kw: make_response("{}")))
    router = ModelRouter(load_model_config(), Settings(near_ai_api_key="k", _env_file=None),
                         client_factory=lambda s: client, sleep=lambda s: None)
    return ScienceAgent(router, oa, ax, now=lambda: NOW), client, router


def good_model_reply(n, kwargs):
    report = {
        "findings": [
            {"claim": "A synthetic interconnect reaches fixture bandwidth targets.", "label": "verified_fact",
             "confidence": "medium", "source_ids": [PAPER_A],
             "supporting_excerpt": "We report a synthetic interconnect reaching fixture bandwidth"},
            {"claim": "This invented claim has a made-up quote and a made-up source.", "label": "verified_fact",
             "confidence": "high", "source_ids": ["src_madeup0000"], "supporting_excerpt": "text that exists nowhere in any paper"},
            {"claim": "Interconnect work appears to cluster around a few themes.", "label": "ai_interpretation",
             "confidence": "low", "source_ids": [PAPER_A], "rationale": "Only a handful of abstracts."},
        ],
        "emerging_directions": ["synthetic direction"],
        "open_problems": ["fixture thermal limits"],
        "limitations": ["abstracts only"],
    }
    return make_response(json.dumps(report))


def test_full_run_retrieves_dedupes_computes_metrics_and_guards_findings():
    agent, client, router = build_agent(model_handler=good_model_reply)
    result = agent.run("chiplet interconnect", from_year=2024, max_papers=10)

    # 3 OpenAlex + 2 arXiv fixtures; arXiv "PAPER B" duplicates OpenAlex "PAPER B" by title -> 4 unique
    assert result.status == "ok" and len(result.sources) == 4
    assert len({s.id for s in result.sources}) == 4
    assert result.publication_counts == {2024: 100, 2025: 150, 2026: 50}
    assert result.acceleration.yoy_growth_pct == 50.0
    assert "No full text was read" in result.coverage_note

    labels = [f.label.value for f in result.findings]
    assert labels == ["verified_fact", "unverified_claim", "ai_interpretation"]
    assert result.findings[0].guard_note is None
    assert result.findings[1].source_ids == [] and "downgraded" in result.findings[1].guard_note
    assert len(result.guard_issues) == 2
    assert result.llm_alias == "deepseek_v4_1_flash"
    # the model only ever saw real retrieved papers, referenced by id
    prompt = json.dumps(client.calls[0]["messages"])
    assert PAPER_A in prompt and "FIXTURE PAPER A" in prompt
    assert router.usage_summary()[0]["agent"] == "science"


def test_paper_search_defaults_to_last_three_years_and_explicit_year_overrides():
    seen_filters = []

    def oa_handler(request):
        if "group_by" not in request.url.params:
            seen_filters.append(request.url.params.get("filter"))
        body = load_json("openalex_group_by.json") if "group_by" in request.url.params else load_json("openalex_works.json")
        return httpx.Response(200, json=body)

    oa = OpenAlexClient("k", http=httpx.Client(transport=httpx.MockTransport(oa_handler)), sleep=lambda s: None, now=lambda: NOW)
    agent = ScienceAgent(None, oa, None, now=lambda: NOW)
    default = agent.run("chiplet", use_llm=False)
    override = agent.run("chiplet", from_year=2021, use_llm=False)
    assert default.from_year == 2023 and override.from_year == 2021
    searches = [f for f in seen_filters if "title_and_abstract.search" not in (f or "")]   # drop the year-to-date counts
    assert searches == ["from_publication_date:2023-01-01", "from_publication_date:2021-01-01"]
    assert default.ytd is not None and default.ytd.cutoff == "10-09"     # NOW = 2026-11-08 minus the 30-day indexing lag


def test_no_papers_means_no_model_call_and_no_findings():
    agent, client, _ = build_agent(openalex_ok=False, arxiv_ok=False)
    result = agent.run("anything")
    assert result.status == "no_data" and result.findings == [] and result.sources == []
    assert len(client.calls) == 0
    assert {e.source for e in result.errors} == {"OpenAlex", "arXiv"}


def test_one_source_down_still_works_and_error_is_reported():
    agent, _, _ = build_agent(arxiv_ok=False, model_handler=good_model_reply)
    result = agent.run("chiplet interconnect")
    assert result.status == "partial" and len(result.sources) == 3
    assert [e.source for e in result.errors] == ["arXiv"]


def test_model_failure_keeps_retrieved_sources_and_reports_error():
    agent, _, _ = build_agent(model_handler=lambda n, kw: status_error(openai.BadRequestError, 400, "nope"))
    result = agent.run("chiplet interconnect")
    assert result.status == "partial" and len(result.sources) == 4 and result.findings == []
    assert any(e.source == "model" for e in result.errors)


def test_retrieval_only_mode_never_calls_the_model():
    agent, client, _ = build_agent()
    result = agent.run("chiplet interconnect", use_llm=False)
    assert result.status == "retrieval_only" and len(result.sources) == 4 and len(client.calls) == 0

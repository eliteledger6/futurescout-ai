"""EPO OPS client and Patent agent tests. All publications and replies are SYNTHETIC (FIXTURE/MOCK);
EPO is faked with httpx.MockTransport. The JSON layout mirrors the known OPS format but has NOT yet
been confirmed against a live response (see app/sources/epo.py)."""

from datetime import datetime, timezone

import httpx
import pytest

from app.agents.patent import PatentAgent
from app.graph import workflow
from app.report import render_markdown
from app.schemas.common import ContentType, Label, make_source_id
from app.sources.base import RateLimiter, SourceError
from app.sources.epo import EpoOpsClient, espacenet_url, parse_biblio, phrase_query
from tests import test_market_agent as m
from tests.helpers import Scripted
from tests.test_workflow import clients as paper_clients
from tests.test_workflow import replies as workflow_replies

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
KEY, SECRET = "FIXTURE-KEY", "FIXTURE-SECRET-never-shown"


def doc(number, title, applicant, date, abstract=None, many_applicants=False):
    d = {
        "@country": "KR", "@doc-number": number, "@kind": "A",
        "bibliographic-data": {
            "publication-reference": {"document-id": [
                {"@document-id-type": "docdb", "country": {"$": "KR"}, "doc-number": {"$": number}, "date": {"$": date}},
                {"@document-id-type": "epodoc", "doc-number": {"$": f"KR{number}"}, "date": {"$": date}}]},
            "invention-title": [{"@lang": "ko", "$": "FIXTURE"}, {"@lang": "en", "$": title}],
            "parties": {"applicants": {"applicant": (
                [{"@data-format": "epodoc", "applicant-name": {"name": {"$": f"{applicant} [KR]"}}},
                 {"@data-format": "original", "applicant-name": {"name": {"$": "original form"}}},
                 {"@data-format": "epodoc", "applicant-name": {"name": {"$": "SECOND FIXTURE CO [US]"}}}]
                if many_applicants else
                {"@data-format": "epodoc", "applicant-name": {"name": {"$": f"{applicant} [KR]"}}})}},
        },
    }
    if abstract:
        d["abstract"] = {"@lang": "en", "p": {"$": abstract}}
    return {"exchange-document": d}


SEARCH = {"ops:world-patent-data": {"ops:biblio-search": {
    "@total-result-count": "57",
    "ops:search-result": {"exchange-documents": [
        doc("1020260001", "Stacked memory with through-silicon vias", "FIXTURE MEMORY CO", "20260815",
            "FIXTURE: a stacked memory device includes a base die and through-silicon vias for heat dissipation.", True),
        doc("1020250002", "Thermal control for stacked memory", "FIXTURE MEMORY CO", "20250301"),
    ]}}}}
ONE = {"ops:world-patent-data": {"ops:biblio-search": {"@total-result-count": "1",
       "ops:search-result": {"exchange-documents": doc("1020240003", "Single", "OTHER FIXTURE", "20240101")}}}}
DOC1 = make_source_id(espacenet_url("KR", "1020260001", "A"))


def client(year_counts=None, seen=None, status=200):
    year_counts = year_counts or {2020: 3, 2021: 5, 2022: 8, 2023: 12, 2024: 20, 2025: 30, 2026: 9}

    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        if request.url.path.endswith("/auth/accesstoken"):
            assert request.headers["authorization"].startswith("Basic ")
            return httpx.Response(200, json={"access_token": "tok-FIXTURE", "expires_in": "1199"})
        if status != 200:
            return httpx.Response(status)
        q = request.url.params["q"]
        if request.url.params["Range"] == "1-1":
            year = int(q.split('pd within "')[1][:4])
            return httpx.Response(200, json={"ops:world-patent-data": {"ops:biblio-search": {"@total-result-count": str(year_counts.get(year, 0))}}})
        return httpx.Response(200, json=SEARCH)

    return EpoOpsClient(KEY, SECRET, http=httpx.Client(transport=httpx.MockTransport(handler)),
                        limiter=RateLimiter(0, sleep=lambda s: None), sleep=lambda s: None, now=lambda: NOW)


def test_parse_handles_lists_single_objects_languages_and_applicant_formats():
    total, recs = parse_biblio(SEARCH, NOW)
    assert total == 57 and len(recs) == 2
    r = recs[0]
    assert r.title == "Stacked memory with through-silicon vias [KR1020260001A]" and r.published_at == "2026-08-15"
    assert r.authors == ["FIXTURE MEMORY CO", "SECOND FIXTURE CO"]  # epodoc names, country suffix removed
    assert r.content_type == ContentType.PATENT and r.text_depth == "abstract_only" and r.publication_type == "patent application"
    assert r.url == "https://worldwide.espacenet.com/patent/search?q=pn%3DKR1020260001A"
    assert recs[1].text_depth == "metadata_only" and recs[1].abstract is None
    assert parse_biblio(ONE, NOW)[1][0].authors == ["OTHER FIXTURE"]   # single object instead of list
    with pytest.raises(SourceError, match="unexpected shape"):
        parse_biblio({"nope": 1}, NOW)


def test_query_and_counts_and_token_reuse():
    assert phrase_query(["high bandwidth memory", "HBM"]) == '(ti="high bandwidth memory" OR ab="high bandwidth memory" OR ti=HBM OR ab=HBM)'
    seen = []
    c = client(seen=seen)
    counts = c.count_by_year(["stacked memory"], 2023)
    assert counts == {2023: 12, 2024: 20, 2025: 30, 2026: 9}
    assert sum(1 for r in seen if r.url.path.endswith("/auth/accesstoken")) == 1  # token reused
    assert all("Bearer tok-FIXTURE" == r.headers.get("authorization") for r in seen if "search" in r.url.path)


def test_a_refusal_is_waited_out_and_asked_again():
    """EPO blocks a key for a few minutes after too many searches a minute (the radar recount, then a report run)."""
    slept, calls = [], {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/auth/accesstoken"):
            return httpx.Response(200, json={"access_token": "tok-FIXTURE", "expires_in": "1199"})
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(403)                                   # refused once, fine a minute later
        return httpx.Response(200, json={"ops:world-patent-data": {"ops:biblio-search": {"@total-result-count": "7"}}})

    c = EpoOpsClient(KEY, SECRET, http=httpx.Client(transport=httpx.MockTransport(handler)),
                     limiter=RateLimiter(0, sleep=lambda s: None), sleep=slept.append, now=lambda: NOW)
    assert c.count_between(["stacked memory"], NOW.date().replace(month=1, day=1), NOW.date()) == 7
    assert slept == [60.0] and c.refusal_waits == 1 and c._limiter.min_interval == 15.0  # waited once, then slower

    always, waits = client(status=403), []                               # a key that stays refused: two waits, then the error
    always._sleep = waits.append
    for _ in range(3):
        with pytest.raises(SourceError, match="fair use"):
            always.search(["stacked memory"])
    assert waits == [60.0, 60.0]


def test_errors_never_leak_credentials():
    with pytest.raises(SourceError) as info:
        client(status=403).search(["stacked memory"])
    assert "fair use" in str(info.value) and SECRET not in str(info.value) and KEY not in str(info.value)
    with pytest.raises(SourceError, match="not set"):
        EpoOpsClient("", "")


PATENT_REPLY = {"findings": [
    {"claim": "A Fixture Memory Co application describes TSVs in stacked memory for heat dissipation.", "label": "verified_fact",
     "confidence": "low", "source_ids": [DOC1], "companies": ["FIXTURE MEMORY CO"],
     "supporting_excerpt": "a stacked memory device includes a base die and through-silicon vias for heat dissipation"},
    {"claim": "This quote is invented and must be downgraded.", "label": "verified_fact", "confidence": "high",
     "source_ids": [DOC1], "supporting_excerpt": "words that appear in no patent anywhere at all"},
], "top_applicants_note": "One applicant dominates the sample.", "limitations": ["abstracts only"]}


def test_agent_computes_patent_acceleration_and_guards_quotes():
    router, _ = m.router_for(Scripted({"PatentReport": PATENT_REPLY}))
    res = PatentAgent(router, client(), now=lambda: NOW).run("stacked memory")
    assert res.status == "ok" and res.total_matches == 57
    assert res.acceleration.previous_year == 2024 and res.acceleration.yoy_growth_pct == 50.0  # 20 -> 30
    assert "18-month" in res.acceleration.basis
    assert res.top_applicants[0] == ("FIXTURE MEMORY CO", 2)
    p1, p2 = res.findings
    assert (p1.fid, p1.label) == ("P1", Label.VERIFIED_FACT) and p2.label == Label.UNVERIFIED_CLAIM


def test_no_credentials_or_failures_mean_no_model_call():
    script = Scripted({"PatentReport": PATENT_REPLY})
    router, _ = m.router_for(script)
    assert PatentAgent(router, None, now=lambda: NOW).run("x memory").status == "no_data"
    res = PatentAgent(router, client(status=403), now=lambda: NOW).run("stacked memory")
    assert res.status == "partial" and res.findings == [] and res.errors
    assert script.calls["PatentReport"] == 0


def test_workflow_runs_patent_and_feeds_investment():
    script = Scripted(workflow_replies(PatentReport={"findings": [PATENT_REPLY["findings"][0]], "limitations": []}))
    router, rclient = m.router_for(script)
    oa, ax = paper_clients()
    report = workflow.run_research("chiplet interconnect", router=router, openalex=oa, arxiv=ax, max_papers=10,
                                   patent_agent=PatentAgent(router, client(), now=lambda: NOW), now=lambda: NOW)
    assert "patent" in report.agents_run and report.agents_not_run == ["market", "x"]
    inv = next(c for c in rclient.calls if "PATENT findings" in c["messages"][-1]["content"])
    assert "[P1] (verified_fact" in inv["messages"][-1]["content"] and "Patent Acceleration" in inv["messages"][-1]["content"]
    md = render_markdown(report)
    assert "## Evidence: patents" in md and "Patent Acceleration 2024->2025" in md and "espacenet" in md

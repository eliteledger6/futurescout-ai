"""X client and X agent tests. All accounts, posts and model replies are SYNTHETIC (FIXTURE/MOCK);
the X API is faked with httpx.MockTransport, so nothing is billed."""

from datetime import datetime, timezone

import httpx
import pytest

from app.agents.x import XAgent, load_watchlist
from app.agents.x.agent import WatchedAccount
from app.graph import workflow
from app.report import render_markdown
from app.schemas.common import ContentType, Label, make_source_id
from app.sources.base import RateLimiter, SourceError
from app.sources.x import XClient, build_watchlist_query, parse_posts, post_url
from tests import test_market_agent as m
from tests.helpers import Scripted
from tests.test_workflow import clients as paper_clients
from tests.test_workflow import replies as workflow_replies

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
TOKEN = "FIXTURE-X-TOKEN-should-never-appear"
WATCH = [WatchedAccount(handle="fixturemem", id="1", group="company", name="Fixture Memory Corp"),
         WatchedAccount(handle="fixturepress", id="2", group="press", name="Fixture Press")]
SEARCH = {
    "data": [
        {"id": "101", "author_id": "1", "created_at": "2026-11-06T10:00:00Z",
         "text": "FIXTURE: Fixture Memory Corp begins sampling 16-high stacked memory to customers."},
        {"id": "102", "author_id": "2", "created_at": "2026-11-07T09:00:00Z",
         "text": "FIXTURE press: stacked memory supply tight, sources say."},
    ],
    "includes": {"users": [{"id": "1", "username": "fixturemem", "name": "Fixture Memory Corp"},
                           {"id": "2", "username": "fixturepress", "name": "Fixture Press"}]},
}
POST1 = make_source_id(post_url("fixturemem", "101"))
POST2 = make_source_id(post_url("fixturepress", "102"))


def x_client(handler=None, seen=None):
    def default(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        if request.url.path.endswith("/users/by"):
            return httpx.Response(200, json={"data": [{"id": "1", "username": "fixturemem", "name": "Fixture Memory Corp",
                                                       "verified_type": "business", "public_metrics": {"followers_count": 10}}],
                                             "errors": [{"value": "ghost", "detail": "not found"}]})
        return httpx.Response(200, json=SEARCH)

    http = httpx.Client(transport=httpx.MockTransport(handler or default), headers={"Authorization": f"Bearer {TOKEN}"})
    return XClient(TOKEN, http=http, limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW)


def test_lookup_reports_found_and_missing_and_counts_billed_users():
    c = x_client()
    found, missing = c.lookup_users(["@fixturemem", "ghost"])
    assert [u.username for u in found] == ["fixturemem"] and found[0].verified_type == "business"
    assert missing == ["ghost"] and c.usage.users_read == 1 and c.usage.cost_usd == 0.01


def test_invalid_handles_are_rejected_before_any_request():
    seen = []
    with pytest.raises(SourceError, match="not valid X usernames"):
        x_client(seen=seen).lookup_users(["fine_name", "no spaces allowed", "waytoolonghandle123"])
    assert seen == []


def test_posts_become_social_posts_with_real_urls():
    recs = parse_posts(SEARCH, NOW)
    assert [r.url for r in recs] == ["https://x.com/fixturemem/status/101", "https://x.com/fixturepress/status/102"]
    assert all(r.content_type == ContentType.SOCIAL_POST for r in recs)
    assert recs[0].authors == ["@fixturemem"] and recs[0].published_at == "2026-11-06"


def test_query_only_searches_the_watchlist_and_respects_length():
    from app.sources.x import account_chunks, watchlist_queries

    q = build_watchlist_query(["stacked memory", "HBM"], ["a", "b"])
    assert q == '("stacked memory" OR HBM) (from:a OR from:b) -is:retweet -is:reply'
    # 37 real-length handles do not fit in one ~500-char query (X returned 400 live): they are chunked, none dropped
    handles = [f"account_name_{i:02d}" for i in range(37)]
    chunks = watchlist_queries(["high bandwidth memory", "HBM"], handles)
    assert len(chunks) >= 2 and all(len(c) <= 500 for c in chunks)
    assert sum(c.count("from:") for c in chunks) == 37
    assert all(c.startswith('("high bandwidth memory" OR HBM) (from:') for c in chunks)
    assert account_chunks(["a"], "")[0] == "(from:a) -is:retweet -is:reply"
    with pytest.raises(SourceError, match="no accounts approved"):
        build_watchlist_query(["x"], [])


def test_search_watchlist_merges_chunks_without_duplicates():
    seen = []
    c = x_client(seen=seen)
    handles = [f"account_name_{i:02d}" for i in range(37)]
    posts = c.search_watchlist(["stacked memory"], handles, max_posts=30)
    assert len(seen) >= 2                                   # one request per chunk
    assert [p.url for p in posts] == ["https://x.com/fixturepress/status/102", "https://x.com/fixturemem/status/101"]  # same fixture posts, deduped, newest first


def test_errors_never_contain_the_token():
    c = x_client(lambda r: httpx.Response(401))
    with pytest.raises(SourceError) as info:
        c.search_recent("anything")
    assert "bearer token" in str(info.value) and TOKEN not in str(info.value)


def test_search_caps_posts_and_counts_cost():
    seen = []
    c = x_client(seen=seen)
    c.search_recent("q", max_posts=500)
    assert seen[0].url.params["max_results"] == "100"
    c.search_recent("q", max_posts=3)
    assert seen[1].url.params["max_results"] == "10"   # X minimum
    assert c.usage.posts_read == 4 and c.usage.cost_usd == 0.02


X_REPLY = {"findings": [
    {"claim": "Fixture Memory Corp says it is sampling 16-high stacked memory.", "label": "verified_fact",
     "confidence": "high", "source_ids": [POST1], "companies": ["Fixture Memory Corp"],
     "supporting_excerpt": "Fixture Memory Corp begins sampling 16-high stacked memory to customers"},
    {"claim": "Stacked memory supply will stay tight next year.", "label": "forecast", "confidence": "medium",
     "source_ids": [POST2], "companies": ["Invented Rival"]},
    {"claim": "Two accounts emphasise stacked memory this week.", "label": "ai_interpretation", "confidence": "low",
     "source_ids": [POST1, POST2]},
], "limitations": ["7-day window"]}


def test_agent_enforces_social_signal_rules():
    router, _ = m.router_for(Scripted({"XReport": X_REPLY}))
    res = XAgent(router, x_client(), watchlist=WATCH, now=lambda: NOW).run("stacked memory")
    x1, x2, x3 = res.findings
    assert [f.fid for f in res.findings] == ["X1", "X2", "X3"] and res.status == "ok"
    assert x1.label == Label.UNVERIFIED_CLAIM and "social posts cannot verify" in x1.guard_note.replace("news headlines and ", "")
    assert x2.label == Label.UNVERIFIED_CLAIM and x2.companies == [] and "Invented Rival" in x2.guard_note
    assert x3.label == Label.AI_INTERPRETATION
    assert res.accounts == ["fixturemem", "fixturepress"] and "from:fixturemem" in res.query
    assert res.x_usage["posts_read"] == 2 and res.x_usage["cost_usd"] == 0.01


def test_no_watchlist_or_no_token_means_no_search_and_no_model_call():
    script = Scripted({"XReport": X_REPLY})
    router, _ = m.router_for(script)
    seen = []
    assert XAgent(router, x_client(seen=seen), watchlist=[], now=lambda: NOW).run("stacked memory").status == "no_data"
    assert XAgent(router, None, watchlist=WATCH, now=lambda: NOW).run("stacked memory").status == "no_data"
    assert seen == [] and script.calls["XReport"] == 0


def test_x_failure_is_recorded_and_not_hidden():
    router, _ = m.router_for(Scripted({"XReport": X_REPLY}))
    res = XAgent(router, x_client(lambda r: httpx.Response(402)), watchlist=WATCH, now=lambda: NOW).run("stacked memory")
    assert res.status == "partial" and "credit" in res.errors[0].message and res.findings == []


def test_real_watchlist_file_has_only_lookup_confirmed_entries():
    approved = load_watchlist()
    from app.agents.x import watchlist as wl
    rows = wl.load()["approved"]
    owner = [r for r in rows if r.get("approved_by", "owner") == "owner"]
    assert sum(1 for r in owner if r.get("group") != "owner-added") == 37   # the original 37 looked-up accounts
    assert sum(1 for r in owner if r.get("group") == "owner-added") == 79   # owner approved the re-checked 79 (2026-11-09)
    assert all(r.get("approved_by") == "agent" for r in rows if r not in owner)
    assert all(a.id.isdigit() for a in approved)                  # every id came from an X lookup or search
    assert len({a.handle.lower() for a in approved}) == len(approved)   # no duplicates
    assert {"TSMC", "SEMIconnects", "OntoInnovation", "KulickeandSoffa"}.isdisjoint({a.handle for a in approved})  # not found on X: never added
    # the combined query for all approved accounts must fit X's limit
    from app.sources.x import build_watchlist_query
    assert len(build_watchlist_query(["high bandwidth memory", "HBM"], [a.handle for a in approved])) <= 4000


def test_workflow_runs_x_in_parallel_and_reports_its_cost():
    script = Scripted(workflow_replies(XReport={"findings": [X_REPLY["findings"][2]], "limitations": []}))
    router, client = m.router_for(script)
    oa, ax = paper_clients()
    xa = XAgent(router, x_client(), watchlist=WATCH, now=lambda: NOW)
    report = workflow.run_research("chiplet interconnect", router=router, openalex=oa, arxiv=ax, max_papers=10,
                                   x_agent=xa, now=lambda: NOW)
    assert "x" in report.agents_run and report.agents_not_run == ["patent", "market"]
    assert script.calls["XReport"] == 1
    x_row = next(u for u in report.usage if u["agent"] == "x (data)")
    assert x_row["cost_usd"] == 0.01 and report.total_cost_usd >= 0.01
    inv_prompt = next(c for c in client.calls if "X findings (posts by approved" in c["messages"][-1]["content"])
    assert "[X1]" in inv_prompt["messages"][-1]["content"]
    md = render_markdown(report)
    assert "## Social signals from X" in md and "@fixturemem" in md and "x (data)" in md

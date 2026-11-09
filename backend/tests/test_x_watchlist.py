"""X account discovery and watchlist management tests. Posts, users and the watchlist file are
SYNTHETIC (FIXTURE); the X API is faked, so nothing is billed."""

from datetime import date, datetime, timezone

import httpx
import yaml

from app.agents.x import XAgent
from app.agents.x import watchlist as wl
from app.agents.x.agent import WatchedAccount
from app.schemas.xsignals import XResult
from app.sources.base import RateLimiter
from app.sources.x import XClient, build_topic_query

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
DISCOVERY = {
    "data": [
        {"id": "1", "author_id": "u1", "created_at": "2026-11-06T10:00:00Z", "text": "FIXTURE stacked memory news", "public_metrics": {"like_count": 50, "retweet_count": 10}},
        {"id": "2", "author_id": "u1", "created_at": "2026-11-05T10:00:00Z", "text": "FIXTURE more stacked memory", "public_metrics": {"like_count": 5}},
        {"id": "3", "author_id": "u2", "created_at": "2026-11-05T10:00:00Z", "text": "FIXTURE 100x stacked memory stock alert", "public_metrics": {}},
        {"id": "4", "author_id": "u3", "created_at": "2026-11-04T10:00:00Z", "text": "FIXTURE post by an approved account"},
    ],
    "includes": {"users": [
        {"id": "u1", "username": "FixtureAnalyst", "name": "Fixture Analyst Co", "description": "Semiconductor research firm", "verified_type": "business", "public_metrics": {"followers_count": 50000}},
        {"id": "u2", "username": "pumpfixture", "name": "Pump Fixture", "description": "Daily stock alerts and signals", "verified_type": None, "public_metrics": {"followers_count": 200}},
        {"id": "u3", "username": "fixturemem", "name": "Fixture Memory Corp", "description": "approved already", "verified_type": "business", "public_metrics": {"followers_count": 1000}},
    ]},
}


def client(seen=None):
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        return httpx.Response(200, json=DISCOVERY)
    return XClient("FIXTURE-token", http=httpx.Client(transport=httpx.MockTransport(handler)), limiter=RateLimiter(0),
                   sleep=lambda s: None, now=lambda: NOW)


def test_discovery_ranks_real_authors_flags_promo_accounts_and_skips_approved():
    seen = []
    out = client(seen).discover_accounts(["stacked memory", "HBM"], exclude={"fixturemem"})
    assert seen[0].url.params["query"] == build_topic_query(["stacked memory", "HBM"]) == '("stacked memory" OR HBM) lang:en -is:retweet -is:reply'
    assert "from:" not in seen[0].url.params["query"]          # discovery looks at all of X
    assert [s.handle for s in out] == ["FixtureAnalyst", "pumpfixture"]
    best = out[0]
    assert best.posts_on_topic == 2 and best.engagement == 65 and best.flags == [] and best.score > out[1].score
    assert best.sample_post_urls[0] == "https://x.com/FixtureAnalyst/status/1"
    assert any("trading-tip" in f for f in out[1].flags) and any("followers" in f for f in out[1].flags)
    assert out[1].score < 0   # flags push tip accounts to the bottom


def fixture_watchlist(tmp_path, auto=False):
    path = tmp_path / "x_watchlist.yaml"
    path.write_text(yaml.safe_dump({
        "auto_manage": auto, "auto_add_min_score": 6.0, "auto_remove_after_days": 90,
        "approved": [{"handle": "fixturemem", "id": "u3", "group": "company", "name": "Fixture Memory Corp"},
                     {"handle": "oldagentpick", "id": "u9", "group": "agent", "name": "Old Agent Pick", "approved_by": "agent",
                      "added_on": "2026-01-01", "last_on_topic": "2026-02-01"}],
        "candidates": [], "suggested": []}), encoding="utf-8")
    return path


def test_suggestions_are_recorded_but_nothing_changes_while_auto_manage_is_off(tmp_path):
    path = fixture_watchlist(tmp_path, auto=False)
    agent = XAgent(None, client(), watchlist=[WatchedAccount(handle="fixturemem", id="u3")], watchlist_path=path, now=lambda: NOW)
    res = XResult(topic="t", status="no_data")
    agent.discover("stacked memory", ["stacked memory"], res)
    data = wl.load(path)
    assert [s["handle"] for s in data["suggested"]] == ["FixtureAnalyst", "pumpfixture"]
    assert data["suggested"][0]["topics"] == ["stacked memory"] and data["suggested"][0]["evidence"]
    assert [a["handle"] for a in data["approved"]] == ["fixturemem", "oldagentpick"]   # untouched
    assert res.watchlist_changes == [] and res.suggested_accounts[0]["new"] is True
    assert "FIXTURE-token" not in path.read_text(encoding="utf-8")


def test_auto_manage_adds_clean_high_scores_and_removes_only_silent_agent_picks(tmp_path):
    path = fixture_watchlist(tmp_path, auto=True)
    agent = XAgent(None, client(), watchlist=[WatchedAccount(handle="fixturemem", id="u3")], watchlist_path=path, now=lambda: NOW)
    res = XResult(topic="t", status="no_data")
    agent.discover("stacked memory", ["stacked memory"], res)
    data = wl.load(path)
    handles = [a["handle"] for a in data["approved"]]
    assert "FixtureAnalyst" in handles and "pumpfixture" not in handles       # flagged account never auto-added
    assert "oldagentpick" not in handles                                      # agent pick silent since Feb: removed
    assert "fixturemem" in handles                                            # owner-approved: never removed
    added = next(a for a in data["approved"] if a["handle"] == "FixtureAnalyst")
    assert added["approved_by"] == "agent" and added["added_on"] == "2026-11-08"
    assert len(res.watchlist_changes) == 2 and len(data["changes"]) == 2
    assert [s["handle"] for s in data["suggested"]] == ["pumpfixture"]        # still waiting for a human


def test_real_watchlist_file_loads_with_defaults():
    data = wl.load()
    # owner decision 2026-11-09: the agent manages the list itself, verified accounts only, stricter score
    assert data["auto_manage"] is True and data["require_verified"] is True and data["auto_add_min_score"] >= 8.0
    assert sum(1 for a in data["approved"] if a.get("approved_by", "owner") == "owner") == 37

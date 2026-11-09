"""The X read list grows on its own (owner 2026-11-09), within rules: verified only, senior roles and @mentions by
watched accounts count, new topics trigger an account search, and a daily X budget caps the spend.
All accounts, posts and profiles here are FIXTURES; the X client is faked. The agent never follows anyone on X."""

from datetime import date, datetime, timezone

import yaml

from app.agents.x import watchlist as wl
from app.config import Settings
from app.radar import TopicConfig
from app.schemas.common import ContentType, SourceRecord
from app.sources.x import AccountSuggestion, XUsage, XUser, exec_role, mentioned_handles, suggestion_from_user, suggestion_score
from app.watch import Watcher, WatchState

NOW = datetime(2026, 11, 9, 12, tzinfo=timezone.utc)


def post(author, text, n):
    return SourceRecord(url=f"https://x.com/{author}/status/{n}", source_name="X", content_type=ContentType.SOCIAL_POST,
                        title=text[:40], authors=[f"@{author}"], abstract=text, retrieved_at=NOW, is_mock=True)


def test_exec_roles_are_found_in_bios_and_lift_the_score():
    assert exec_role("CEO @FixtureChips. Ex-Intel.") == "CEO"
    assert exec_role("Vice President, AI Infrastructure") == "Vice President"
    assert exec_role("Co-founder of a robotics startup") == "Co-founder"
    assert exec_role("I write about chips") is None and exec_role("ceoish fan page") is None
    base = dict(handle="a", id="1", name="A", description="", verified_type="blue", followers=50_000, posts_on_topic=1,
                engagement=0, sample_post_urls=[])
    assert suggestion_score(AccountSuggestion(**base, role="CTO")) == suggestion_score(AccountSuggestion(**base)) + 2.0


def test_mentions_only_count_watched_authors_and_skip_self_and_known():
    posts = [post("watcheda", "Great talk by @FixtureCEO and @watchedb on HBM", 1),
             post("watchedb", "Agree with @fixtureceo, also @watcheda", 2),
             post("stranger", "@FixtureCEO hello", 3),
             post("watcheda", "me again @watcheda", 4)]
    assert mentioned_handles(posts, {"watcheda", "watchedb"}) == {"fixtureceo": {"watcheda", "watchedb"}}


def watchlist_file(tmp_path, **extra):
    data = {"auto_manage": True, "auto_add_min_score": 6.0, "auto_remove_after_days": 90, "max_accounts": 200,
            "require_verified": True, "endorse_min_watchers": 2,
            "approved": [{"handle": "watcheda", "id": "1", "approved_by": "owner"}, {"handle": "watchedb", "id": "2", "approved_by": "owner"}],
            "suggested": [], "changes": [], **extra}
    p = tmp_path / "x_watchlist.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p


def test_auto_add_requires_verified_and_counts_endorsements(tmp_path):
    p = watchlist_file(tmp_path)
    data = wl.load(p)
    unverified = suggestion_from_user(XUser("9", "loudguy", "Loud Guy", "CEO of something big", False, None, 90_000, None), reason="x")
    verified = suggestion_from_user(XUser("8", "fixtureceo", "Fixture CEO", "CEO at Fixture Chips", True, "blue", 40_000, None), reason="x")
    assert verified.role == "CEO" and verified.score == round(0.5 + 4.602 + 2.0, 2)        # blue badge + reach + role
    wl.record_suggestions(data, [unverified, verified], "mentioned by watched accounts", today=date(2026, 11, 9))
    wl.record_endorsements(data, {"fixtureceo": {"watcheda", "watchedb"}, "loudguy": {"watcheda", "watchedb"}}, today=date(2026, 11, 9))
    changes = wl.auto_manage(data, today=date(2026, 11, 9))
    handles = [a["handle"] for a in data["approved"]]
    assert "fixtureceo" in handles and "loudguy" not in handles                                 # no verification: never added
    assert "mentioned by @watcheda, @watchedb" in changes[0] and "CEO" in changes[0]
    added = next(a for a in data["approved"] if a["handle"] == "fixtureceo")
    assert added["approved_by"] == "agent"                                                     # removable by the agent later


def test_endorsements_expire_and_only_unknown_handles_need_a_lookup(tmp_path):
    data = wl.load(watchlist_file(tmp_path))
    need = wl.record_endorsements(data, {"newperson": {"watcheda", "watchedb"}, "onlyonce": {"watcheda"}}, today=date(2026, 9, 1))
    assert need == ["newperson"]                                                               # one watcher is not enough
    assert wl.endorsement_bonus(data, "NewPerson") == 4.0
    wl.record_endorsements(data, {}, today=date(2026, 11, 9))                                  # 69 days later
    assert "newperson" not in data["endorsements"]


class FakeX:
    def __init__(self, posts):
        self.posts, self.usage = posts, XUsage()
        self.lookups, self.searches = [], []

    def recent_from_accounts(self, usernames, *, max_posts=30, since_id=None):
        self.usage.posts_read += len(self.posts)
        return self.posts

    def lookup_users(self, usernames):
        self.lookups.append(list(usernames))
        self.usage.users_read += len(usernames)
        return [XUser("8", "fixtureceo", "Fixture CEO", "CEO at Fixture Chips", True, "blue", 40_000, None)], []

    def discover_accounts(self, keywords, *, exclude, max_posts=50):
        self.searches.append(keywords)
        self.usage.posts_read += 50
        s = AccountSuggestion("labvp", "7", "Lab VP", "VP Research, Fixture Labs", "business", 20_000, 3, 10,
                              ["https://x.com/labvp/status/1"], role="VP")
        s.score = suggestion_score(s)                      # the real client scores before returning
        return [s]


def make_watcher(tmp_path, x, **settings):
    topics = tmp_path / "topics.yaml"
    topics.write_text(yaml.safe_dump({"topics": [{"name": "hbm", "terms": ["hbm"]}]}), encoding="utf-8")
    s = Settings(_env_file=None, watch_paper_discovery_days=0, **settings)
    return Watcher(s, x_client=x, accounts=["watcheda", "watchedb"], router=None, openalex=None, patents_cached=None,
                   state_path=tmp_path / "state.json", topics_file=topics, watchlist_path=watchlist_file(tmp_path), now=lambda: NOW)


def test_scan_reads_grows_from_mentions_and_tracks_spend(tmp_path, monkeypatch):
    x = FakeX([post("watcheda", "Keynote by @FixtureCEO today", 1), post("watchedb", "Thanks @FixtureCEO", 2)])
    w = make_watcher(tmp_path, x, watch_x_daily_budget_usd=3.0)
    state = WatchState()
    w.scan(state)
    assert x.lookups == [["fixtureceo"]]
    assert "fixtureceo" in [a["handle"] for a in wl.load(w.watchlist_path)["approved"]]
    assert w.accounts == ["watcheda", "watchedb"]                                              # reloaded next cycle
    assert state.x_spent_today(NOW) == round(2 * 0.005 + 1 * 0.01, 4)
    assert any(e["kind"] == "accounts" and "added @fixtureceo" in e["detail"] for e in state.events)


def test_budget_stops_reading_and_new_topics_trigger_capped_account_searches(tmp_path):
    x = FakeX([])
    w = make_watcher(tmp_path, x, watch_x_daily_budget_usd=0.2, watch_x_discovery_topics_per_day=1)
    state = WatchState()
    state.add_x_spend(NOW, 0.25)
    assert w.scan(state) is None and "budget" in state.events[-1]["detail"] and x.usage.posts_read == 0
    state = WatchState()
    w.discover_accounts_for(state, [{"topic": "glass substrate", "terms": ["glass substrate"]}, {"topic": "3d dram", "terms": ["3d dram"]}])
    assert x.searches == [["glass substrate"]]                                                 # 1 per day
    assert "labvp" in [a["handle"] for a in wl.load(w.watchlist_path)["approved"]]
    assert any("postponed" in e["detail"] for e in state.events)

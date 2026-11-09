"""Watch-mode tests. X posts, radar counts and research runs are all FAKED; nothing is billed."""

from datetime import datetime, timedelta, timezone

import httpx
import yaml

from app.config import Settings
from app.radar import TopicConfig
from app.schemas.common import ContentType, SourceRecord
from app.sources.base import RateLimiter
from app.sources.x import XClient, build_accounts_query
from app.watch import Watcher, count_mentions, load_state

NOW = datetime(2026, 11, 9, 8, 0, tzinfo=timezone.utc)


def post(pid, handle, text):
    return SourceRecord(url=f"https://x.com/{handle}/status/{pid}", source_name="X API", content_type=ContentType.SOCIAL_POST,
                        title=text[:60], abstract=text, authors=[f"@{handle}"], text_depth="full_text")


TOPICS = [TopicConfig(name="high bandwidth memory", terms=["high bandwidth memory", "HBM"]),
          TopicConfig(name="co-packaged optics", terms=["co-packaged optics", "CPO"])]


def test_count_mentions_matches_terms_whole_word_and_hyphen_blind():
    posts = [post("1", "a", "FIXTURE: our HBM4 samples ship"), post("2", "b", "FIXTURE co packaged optics demo at the show"),
             post("3", "c", "FIXTURE chbm is not a word about HBM? no: it says CHBM only")]
    m = count_mentions(posts, TOPICS)
    # post 1: "HBM4" is not the whole word HBM (no match); post 2: hyphen-blind match; post 3: whole word "HBM?" matches
    assert m == {"co-packaged optics": 1, "high bandwidth memory": 1}
    assert count_mentions([post("4", "a", "FIXTURE HBM demand is strong")], TOPICS) == {"high bandwidth memory": 1}


class FakeCounter:
    SOURCE = "fixture"

    def __init__(self, table):
        self.table, self.searches_used = table, 0

    def count_by_year(self, key, start):
        self.searches_used += 1
        name = key if isinstance(key, str) else key[0]
        return self.table.get(name, {2022: 10, 2023: 12, 2024: 14, 2025: 15, 2026: 3})


HOT = {2022: 20, 2023: 40, 2024: 80, 2025: 160, 2026: 30}


def x_client(payload):
    http = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, json=payload)), headers={"Authorization": "Bearer FIXTURE"})
    return XClient("FIXTURE", http=http, limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW)


POSTS = {"data": [{"id": "900", "author_id": "u", "created_at": "2026-11-09T07:00:00Z", "text": "FIXTURE: HBM supply remains tight"},
                  {"id": "901", "author_id": "u", "created_at": "2026-11-09T07:10:00Z", "text": "FIXTURE: more on HBM pricing"},
                  {"id": "902", "author_id": "u", "created_at": "2026-11-09T07:20:00Z", "text": "FIXTURE: HBM again"}],
         "includes": {"users": [{"id": "u", "username": "fixturemem", "name": "Fixture Memory Corp"}]}}


def make_watcher(tmp_path, *, runs, ages=None, research=True, settings=None):
    topics_file = tmp_path / "topics.yaml"
    topics_file.write_text(yaml.safe_dump({"topics": [{"name": t.name, "terms": t.terms} for t in TOPICS]}), encoding="utf-8")
    s = settings or Settings(_env_file=None, watch_max_runs_per_day=1)

    def run(topic):
        runs.append(topic)
        return f"run-{len(runs)}"
    return Watcher(s, x_client=x_client(POSTS), accounts=["fixturemem"], router=None,
                   openalex=FakeCounter({"co-packaged optics": HOT, "high bandwidth memory": HOT}),
                   patents_cached=FakeCounter({"co-packaged optics": HOT, "high bandwidth memory": HOT}),
                   patents_live_factory=None, run_research=run if research else None, report_ages=lambda: ages or {},
                   state_path=tmp_path / "state.json", topics_file=topics_file, now=lambda: NOW)


def test_cycle_scans_detects_triggers_once_per_day_and_logs_everything(tmp_path, monkeypatch):
    monkeypatch.setattr("app.watch.save_radar", lambda radar: None)   # do not touch the real radar file
    runs = []
    w = make_watcher(tmp_path, runs=runs)
    state = w.cycle()
    kinds = [e["kind"] for e in state.events]
    assert "scan" in kinds and "radar" in kinds and "trigger" in kinds and "run" in kinds
    assert state.last_post_id == "902" and state.mention_history[-1]["mentions"] == {"high bandwidth memory": 3}
    # both topics are hot (+100%) but the daily cap is 1: HBM wins (3 mentions), CPO is skipped with a reason
    assert runs == ["high bandwidth memory"]
    assert any(e["kind"] == "skip" and "daily cap" in e["detail"] and e["topic"] == "co-packaged optics" for e in state.events)
    assert state.runs_started[0]["run_id"] == "run-1"
    # second cycle the same day: cap reached, nothing new runs; the since_id is reused
    state2 = make_watcher(tmp_path, runs=runs).cycle()
    assert runs == ["high bandwidth memory"] and state2.runs_today(NOW) == 1
    assert load_state(tmp_path / "state.json").last_post_id == "902"


def test_fresh_report_blocks_a_rerun(tmp_path, monkeypatch):
    monkeypatch.setattr("app.watch.save_radar", lambda radar: None)
    runs = []
    ages = {"high bandwidth memory": NOW - timedelta(days=1), "co-packaged optics": NOW - timedelta(days=30)}
    make_watcher(tmp_path, runs=runs, ages=ages).cycle()
    assert runs == ["co-packaged optics"]   # HBM has a 1-day-old report: skipped; CPO's is 30 days old: researched


def test_no_research_mode_only_observes(tmp_path, monkeypatch):
    monkeypatch.setattr("app.watch.save_radar", lambda radar: None)
    runs = []
    state = make_watcher(tmp_path, runs=runs, research=False).cycle()
    assert runs == [] and any(e["kind"] == "trigger" for e in state.events) and state.runs_started[0]["run_id"] is None


def test_accounts_query_has_no_topic_filter():
    q = build_accounts_query(["a", "b"])
    assert q == "(from:a OR from:b) -is:retweet -is:reply"

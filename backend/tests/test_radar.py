

def test_a_copy_without_runs_serves_the_snapshot_radar_before_the_sample(tmp_path, monkeypatch):
    import json
    from app import radar as rd
    real = json.loads((rd.BACKEND_DIR / "samples" / "radar.json").read_text(encoding="utf-8"))
    snap, sample = dict(real, generated_at="2026-11-09T06:53:54Z"), dict(real, generated_at="2026-11-09T05:43:19Z")
    (tmp_path / "snap.json").write_text(json.dumps(snap), encoding="utf-8")
    (tmp_path / "sample.json").write_text(json.dumps(sample), encoding="utf-8")
    monkeypatch.setattr(rd, "RADAR_FILE", tmp_path / "runs_radar.json")           # no runs/ on this copy
    monkeypatch.setattr(rd, "SNAPSHOT_RADAR_FILE", tmp_path / "snap.json")
    monkeypatch.setattr(rd, "SAMPLE_RADAR_FILE", tmp_path / "sample.json")
    assert rd.load_radar(rd.RADAR_FILE).generated_at.isoformat().startswith("2026-11-09T06:53")   # the snapshot wins
    (tmp_path / "snap.json").unlink()
    assert rd.load_radar(rd.RADAR_FILE).generated_at.isoformat().startswith("2026-11-09T05:43")   # then the sample


def test_a_topic_the_first_patent_source_cannot_count_is_counted_by_the_second():
    from datetime import datetime, timezone
    from app.radar import TopicConfig, compute_radar
    from app.sources.base import SourceError

    class Paused:
        SOURCE = "Google Patents (SerpApi)"
        def count_by_year(self, terms, start):
            if terms == ["cached topic"]:
                return {2022: 30, 2023: 40, 2024: 50, 2025: 100, 2026: 60}
            raise SourceError("serpapi", "patent search is paused to save the SerpApi quota")
        def count_between(self, terms, a, b):
            return 10

    class Epo:
        SOURCE = "EPO OPS"
        def count_by_year(self, terms, start):
            return {2022: 20, 2023: 25, 2024: 30, 2025: 60, 2026: 40}
        def count_between(self, terms, a, b):
            return 5

    topics = [TopicConfig(name="cached topic", terms=["cached topic"], sector="semiconductors"),
              TopicConfig(name="new topic", terms=["new topic"], sector="semiconductors")]
    now = lambda: datetime(2026, 11, 11, tzinfo=timezone.utc)  # noqa: E731
    r = compute_radar(topics, openalex=None, patents=Paused(), patents_fallback=Epo(), now=now)
    by = {t.topic: t for t in r.topics}
    assert by["cached topic"].patent_source == "Google Patents (SerpApi)" and by["cached topic"].patent_counts[2025] == 100
    assert by["new topic"].patent_source == "EPO OPS" and by["new topic"].patent_counts[2025] == 60 and not by["new topic"].errors
    alone = compute_radar(topics, openalex=None, patents=Paused(), now=now)
    t = {x.topic: x for x in alone.topics}["new topic"]
    assert t.patent_source is None and any("paused" in e for e in t.errors)             # no second source: stated, not guessed


def test_a_run_that_cannot_count_patents_keeps_the_earlier_numbers_and_a_blocked_source_is_left_alone():
    from datetime import datetime, timezone
    from app.radar import TopicConfig, carry_over_patents, compute_radar
    from app.sources.base import SourceError
    now = lambda: datetime(2026, 11, 11, tzinfo=timezone.utc)  # noqa: E731
    topics = [TopicConfig(name=n, terms=[n], sector="semiconductors") for n in ("a", "b", "c")]

    class Good:
        SOURCE = "EPO OPS"
        def count_by_year(self, terms, start): return {2022: 20, 2023: 25, 2024: 30, 2025: 60, 2026: 40}
        def count_between(self, terms, a, b): return 5
    old = compute_radar(topics, openalex=None, patents=Good(), now=lambda: datetime(2026, 11, 9, tzinfo=timezone.utc))

    calls = []

    class Blocked:
        SOURCE = "EPO OPS"
        def count_by_year(self, terms, start):
            calls.append(terms[0])
            raise SourceError("EPO OPS", "EPO refused the request (fair use / quota or bad token)", status=403)
        def count_between(self, terms, a, b): return 0

    class Paused:
        SOURCE = "Google Patents (SerpApi)"
        def count_by_year(self, terms, start): raise SourceError("serpapi", "patent search is paused")
        def count_between(self, terms, a, b): return 0
    new = compute_radar(topics, openalex=None, patents=Paused(), patents_fallback=Blocked(), now=now)
    assert calls == ["a"]                                               # refused once: not asked again in this run
    assert all(not t.patent_counts for t in new.topics)
    assert carry_over_patents(new, old) == 3
    t = new.topics[0]
    assert t.patent_counts[2025] == 60 and t.patent_source == "EPO OPS" and t.patent_counted_at == "2026-11-09" and not t.errors


def test_epo_client_slows_down_to_the_rate_epo_allows():
    from app.sources.base import RateLimiter
    from app.sources.epo import EpoOpsClient
    c = EpoOpsClient("k", "s", limiter=RateLimiter(2.0))
    c._follow_throttle("idle (images=green:200, inpadoc=green:60, other=green:1000, retrieval=green:200, search=green:30)")
    assert c._limiter.min_interval == 2.6                               # 30 a minute allowed: one every 2.6 s
    c._follow_throttle("overloaded (search=red:5, other=green:1000)")
    assert c._limiter.min_interval == 15.6                              # loaded: 5 a minute
    c._follow_throttle("overloaded (search=black:0)")
    assert c._limiter.min_interval == 15.6                              # blocked: keep the slow pace (the call itself fails)
    c._follow_throttle("idle (search=green:60)")
    assert c._limiter.min_interval == 2.0                               # never faster than our own base pace

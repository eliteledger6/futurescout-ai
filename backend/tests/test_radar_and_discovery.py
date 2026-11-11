"""Radar and SEC full-text discovery tests. All counts/hits are SYNTHETIC (FIXTURE); networks are faked."""

from datetime import date, datetime, timezone

import httpx
import pytest

from app.radar import Radar, TopicConfig, compute_radar, heat_of, load_radar, load_topics, rank_topics, save_radar
from app.schemas.science import AccelerationMetric
from app.sources.base import RateLimiter, SourceError
from app.sources.edgar_fulltext import EdgarFullTextClient, parse_display_name, parse_hits

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)


class FakeCounter:
    """Stands in for OpenAlex / SerpApi count_by_year."""
    SOURCE = "fixture counts"

    def __init__(self, table, fail=False):
        self.table, self.fail, self.searches_used = table, fail, 0

    def count_by_year(self, *args, **kw):
        if self.fail:
            raise SourceError(self.SOURCE, "fixture outage")
        key = args[0] if isinstance(args[0], str) else args[0][0]
        self.searches_used += 5
        return self.table[key]


PAPERS = {"hot topic": {2022: 10, 2023: 20, 2024: 40, 2025: 80, 2026: 30}, "cold topic": {2022: 50, 2023: 50, 2024: 50, 2025: 45, 2026: 10}}
PATENTS = {"hot topic": {2022: 20, 2023: 30, 2024: 40, 2025: 60, 2026: 10}, "cold topic": {2022: 90, 2023: 90, 2024: 90, 2025: 90, 2026: 20}}


def test_heat_ranks_hot_above_cold_and_tolerates_failures():
    topics = [TopicConfig(name="cold topic", terms=["cold topic"]), TopicConfig(name="hot topic", terms=["hot topic"])]
    radar = compute_radar(topics, openalex=FakeCounter(PAPERS), patents=FakeCounter(PATENTS), now=lambda: NOW)
    hot, cold = radar.topics
    assert hot.topic == "hot topic" and hot.rank == 1 and hot.heat == 75.0   # papers +100%, patents +50%
    assert cold.heat == -5.0 and cold.rank == 2 and radar.searches_used == 10
    assert "not whether it is a good investment" in radar.basis
    broken = compute_radar(topics, openalex=FakeCounter(PAPERS), patents=FakeCounter(PATENTS, fail=True), now=lambda: NOW)
    # patents down: heat falls back to paper growth alone, visibly marked, so topics can still be ranked
    assert all(t.heat_basis == "papers 2025" and t.errors[0].startswith("patents: ") and "fixture outage" in t.errors[0] for t in broken.topics)
    assert [t.topic for t in broken.topics] == ["hot topic", "cold topic"] and broken.topics[0].heat == 100.0 and broken.topics[0].rank == 1
    assert hot.heat_basis == "papers 2025 + patents 2025"


def test_small_base_topics_are_shown_but_not_ranked():
    papers = {"tiny": {2022: 1, 2023: 2, 2024: 7, 2025: 30, 2026: 5}, "big": {2022: 100, 2023: 110, 2024: 120, 2025: 150, 2026: 40}}
    patents = {"tiny": {2022: 30, 2023: 31, 2024: 31, 2025: 35, 2026: 9}, "big": {2022: 90, 2023: 95, 2024: 100, 2025: 120, 2026: 30}}
    radar = compute_radar([TopicConfig(name="tiny", terms=["tiny"]), TopicConfig(name="big", terms=["big"])],
                          openalex=FakeCounter(papers), patents=FakeCounter(patents), now=lambda: NOW)
    big, tiny = radar.topics                      # ranked topic first, small-base topic last
    assert big.rank == 1 and tiny.rank is None and tiny.small_base and tiny.heat is not None
    assert "not ranked" in radar.basis


def test_heat_needs_both_signals():
    a = AccelerationMetric(last_full_year=2025, last_full_year_count=2, previous_year=2024, previous_year_count=1, yoy_growth_pct=100.0)
    assert heat_of(a, None) == 100.0 and heat_of(a, a) == 100.0 and heat_of(None, None) is None


def test_radar_round_trips_through_file(tmp_path):
    radar = compute_radar([TopicConfig(name="hot topic", terms=["hot topic"])], openalex=FakeCounter(PAPERS), patents=FakeCounter(PATENTS), now=lambda: NOW)
    p = save_radar(radar, tmp_path / "radar.json")
    assert load_radar(p).topics[0].heat == 75.0 and load_radar(tmp_path / "none.json") is None


def test_real_topics_file_is_valid():
    topics = load_topics()
    assert len(topics) >= 6 and all(t.terms for t in topics)


HITS = {"hits": {"total": {"value": 3}, "hits": [
    {"_id": "0000319201-26-000027:klac-20260630.htm", "_source": {"display_names": ["KLA CORP  (KLAC)  (CIK 0000319201)"], "ciks": ["0000319201"], "file_date": "2026-08-06", "root_forms": ["10-K"]}},
    {"_id": "0000319201-26-000034:klac-20260930.htm", "_source": {"display_names": ["KLA CORP  (KLAC)  (CIK 0000319201)"], "ciks": ["0000319201"], "file_date": "2026-10-29", "root_forms": ["10-Q"]}},
    {"_id": "0001628280-26-010744:uctt-20251226.htm", "_source": {"display_names": ["Ultra Clean Holdings, Inc.  (UCTT)  (CIK 0001275014)"], "ciks": ["0001275014"], "file_date": "2026-02-23", "root_forms": ["10-K"]}},
    {"_id": "0009999999-26-000001:priv.htm", "_source": {"display_names": ["Fixture Private Filer LLC  (CIK 0009999999)"], "ciks": ["0009999999"], "file_date": "2026-03-01", "root_forms": ["10-K"]}},
]}}


def test_parse_hits_groups_by_company_and_reads_tickers():
    assert parse_display_name("KLA CORP  (KLAC)  (CIK 0000319201)") == ("Kla Corp", "KLAC", 319201)
    assert parse_display_name("Fixture Private Filer LLC  (CIK 0009999999)") == ("Fixture Private Filer LLC", None, 9999999)
    total, filers = parse_hits(HITS)
    assert total == 3 and [f.name for f in filers] == ["Kla Corp", "Fixture Private Filer LLC", "Ultra Clean Holdings, Inc."]
    kla = filers[0]
    assert kla.mentions == 2 and kla.ticker == "KLAC" and kla.latest_filing == "2026-10-29" and kla.latest_form == "10-Q"
    assert kla.documents[0] == ("0000319201-26-000034", "klac-20260930.htm")   # newest filing first, not search order
    with pytest.raises(SourceError, match="unexpected shape"):
        parse_hits({"nope": 1})


def client(seen=None):
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        return httpx.Response(200, json=HITS)
    return EdgarFullTextClient("Fixture Tester fixture@example.invalid", http=httpx.Client(transport=httpx.MockTransport(handler)),
                               limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW)


def test_find_filers_and_counts_send_quoted_phrase_and_date_window():
    seen = []
    total, filers = client(seen).find_filers("high bandwidth memory", months=15)
    assert total == 3 and len(filers) == 3
    p = seen[0].url.params
    assert p["q"] == '"high bandwidth memory"' and p["forms"] == "10-K,10-Q,20-F" and p["startdt"] == "2025-08-01" and p["enddt"] == "2026-11-08"
    counts = client().count_filers_by_year("high bandwidth memory", 2024)
    assert counts == {2024: 3, 2025: 3, 2026: 3}
    with pytest.raises(SourceError, match="contact email"):
        EdgarFullTextClient("no-email")

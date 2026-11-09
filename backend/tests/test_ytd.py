"""Year-to-date momentum: the current, unfinished year is compared with the SAME dates last year, so a topic that is
fading (or exploding) right now is visible before next January. Counts are FIXTURES; OpenAlex is faked."""

from datetime import date, datetime, timezone

import httpx

from app.agents.science.metrics import LAG_DAYS, compute_ytd, ytd_from_client, ytd_window
from app.radar import TopicConfig, compute_radar
from app.sources.openalex import OpenAlexClient

NOW = datetime(2026, 11, 9, tzinfo=timezone.utc)


def test_window_leaves_out_the_indexing_lag_from_both_years():
    s1, e1, s0, e0 = ytd_window(date(2026, 11, 9))
    assert (s1, s0) == (date(2026, 1, 1), date(2025, 1, 1))
    assert e1 == date(2026, 10, 10) and e0 == date(2025, 10, 10) and (date(2026, 11, 9) - e1).days == LAG_DAYS
    assert ytd_window(date(2026, 1, 20)) is None                 # cutoff would fall in last year: nothing to compare
    assert ytd_window(date(2028, 3, 30))[3] == date(2027, 2, 28)  # 29 Feb has no twin last year


def test_trend_labels_and_the_small_base_rule():
    assert compute_ytd(100, 1000, date(2026, 10, 10)).trend == "cooling"     # the owner's example: collapsing
    assert compute_ytd(100, 1000, date(2026, 10, 10)).growth_pct == -90.0
    assert compute_ytd(1500, 1000, date(2026, 10, 10)).trend == "rising"
    assert compute_ytd(1050, 1000, date(2026, 10, 10)).trend == "flat"
    small = compute_ytd(30, 5, date(2026, 10, 10))
    assert small.growth_pct == 500.0 and small.trend is None                # 5 papers last year: no label


def test_openalex_count_between_sends_the_date_window_and_reads_meta_count():
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.url.params["filter"])
        return httpx.Response(200, json={"meta": {"count": 123}, "results": []})
    oa = OpenAlexClient("k", http=httpx.Client(transport=httpx.MockTransport(handler)), sleep=lambda s: None)
    y = ytd_from_client(oa, "solid-state battery", date(2026, 11, 9))
    assert y.count == 123 and y.previous_count == 123 and y.trend == "flat" and y.cutoff == "10-10"
    assert 'title_and_abstract.search:"solid-state battery"' in seen[0]
    assert "from_publication_date:2026-01-01,to_publication_date:2026-10-10" in seen[0]
    assert "from_publication_date:2025-01-01,to_publication_date:2025-10-10" in seen[1]


class Counter:
    """count_by_year + count_between from fixture tables."""

    def __init__(self, years, ytd):
        self.years, self.ytd = years, ytd

    def count_by_year(self, phrase, start):
        return self.years[phrase]

    def count_between(self, phrase, start, end):
        return self.ytd[phrase][start.year]


def test_radar_heat_drops_for_a_topic_that_is_fading_this_year():
    years = {"fading": {2022: 100, 2023: 200, 2024: 500, 2025: 1000, 2026: 100},
             "steady": {2022: 100, 2023: 200, 2024: 500, 2025: 1000, 2026: 900}}
    ytd = {"fading": {2026: 100, 2025: 900}, "steady": {2026: 1100, 2025: 900}}
    radar = compute_radar([TopicConfig(name="fading", terms=["fading"]), TopicConfig(name="steady", terms=["steady"])],
                          openalex=Counter(years, ytd), patents=None, now=lambda: NOW)
    steady, fading = radar.topics                                 # steady now ranks first
    assert steady.topic == "steady" and steady.rank == 1 and steady.trend == "rising"
    assert fading.trend == "cooling" and fading.paper_ytd.growth_pct == -88.9
    assert fading.heat == round((100.0 + -88.9) / 2, 1)          # both had +100% in 2025; 2026 tells them apart
    assert fading.heat_basis == "papers 2025 + papers YTD" and "cooling" in radar.basis

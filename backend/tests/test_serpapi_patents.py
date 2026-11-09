"""SerpApi Google Patents client tests. Responses are SYNTHETIC (FIXTURE), shaped like the sample
in SerpApi's docs (read 2026-11-08); no request leaves the machine and no search quota is used."""

from datetime import datetime, timezone

import httpx
import pytest

from app.agents.patent import PatentAgent
from app.schemas.common import ContentType, Label
from app.sources.base import RateLimiter, SourceError
from app.sources.serpapi_patents import SerpApiPatentsClient, build_query, parse_results
from tests import test_market_agent as m
from tests.helpers import Scripted

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
KEY = "FIXTURE-serpapi-key-never-shown"
PAYLOAD = {
    "search_information": {"total_results": 812, "total_pages": 9, "page_number": 1},
    "organic_results": [
        {"position": 1, "patent_id": "patent/US20260012345A1/en", "patent_link": "https://patents.google.com/patent/US20260012345A1/en",
         "title": "Stacked memory   device with thermal vias", "snippet": "FIXTURE: A stacked memory device includes a base die and thermal vias.",
         "priority_date": "2025-01-10", "filing_date": "2025-06-01", "publication_date": "2026-01-15",
         "assignee": "Fixture Memory Co", "inventor": "A. Fixture", "publication_number": "US20260012345A1", "language": "en"},
        {"position": 2, "patent_id": "patent/KR102999999B1/en", "patent_link": "https://patents.google.com/patent/KR102999999B1/en",
         "title": "Memory module", "snippet": "", "publication_date": "2025-11-02", "grant_date": "2025-11-02",
         "assignee": "Other Fixture Ltd", "publication_number": "KR102999999B1"},
        {"position": 3, "title": "A scholar result without a patent link", "snippet": "skipped"},
    ],
}


def client(tmp_path=None, status=200, seen=None, payload=None):
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        if status != 200:
            return httpx.Response(status)
        if "before" in request.url.params:
            year = int(request.url.params["before"].split(":")[1][:4])
            return httpx.Response(200, json={"search_information": {"total_results": {2022: 40, 2023: 60, 2024: 90, 2025: 150, 2026: 70}.get(year, 0)}})
        return httpx.Response(200, json=payload or PAYLOAD)

    return SerpApiPatentsClient(KEY, http=httpx.Client(transport=httpx.MockTransport(handler)), limiter=RateLimiter(0),
                                cache_dir=tmp_path, sleep=lambda s: None, now=lambda: NOW)


def test_query_syntax():
    assert build_query(["high bandwidth memory", "HBM"]) == (
        'TI=("high bandwidth memory") OR AB=("high bandwidth memory") OR TI=(HBM) OR AB=(HBM)')
    assert build_query(["compute-in-memory"]) == 'TI=("compute in memory") OR AB=("compute in memory")'  # hyphens -> spaces
    with pytest.raises(SourceError):
        build_query([" "])


def test_parse_keeps_real_links_and_snippets_only():
    total, recs = parse_results(PAYLOAD, NOW)
    assert total == 812 and len(recs) == 2   # scholar row without patent_link skipped
    r = recs[0]
    assert r.url == "https://patents.google.com/patent/US20260012345A1/en" and r.content_type == ContentType.PATENT
    assert r.title == "Stacked memory device with thermal vias [US20260012345A1]" and r.published_at == "2026-01-15"
    assert r.text_depth == "excerpt_only" and r.authors == ["Fixture Memory Co"] and r.publication_type == "patent application"
    assert recs[1].text_depth == "metadata_only" and recs[1].publication_type == "patent grant"
    assert parse_results({"error": "Google Patents hasn't returned any results for this query."}, NOW) == (0, [])
    with pytest.raises(SourceError, match="Invalid API key"):
        parse_results({"error": "Invalid API key."}, NOW)


def test_counts_cost_one_search_per_year_and_cache_makes_repeats_free(tmp_path):
    seen = []
    c = client(tmp_path, seen=seen)
    counts = c.count_by_year(["stacked memory"], 2022)
    assert counts == {2022: 40, 2023: 60, 2024: 90, 2025: 150, 2026: 70}
    assert c.searches_used == 5 and seen[0].url.params["num"] == "10"
    again = client(tmp_path, seen=seen)
    assert again.count_by_year(["stacked memory"], 2022) == counts
    assert again.searches_used == 0 and again.cache_hits == 5 and len(seen) == 5   # no new requests
    assert all(KEY not in p.name and KEY not in p.read_text() for p in tmp_path.iterdir())


def test_cache_only_mode_spends_nothing(tmp_path):
    seen = []
    client(tmp_path, seen=seen).count_by_year(["stacked memory"], 2024)      # fills the cache (3 searches)
    paused = SerpApiPatentsClient(KEY, http=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(500))),
                                  limiter=RateLimiter(0), cache_dir=tmp_path, cache_only=True, sleep=lambda s: None,
                                  clock=lambda: 10**12, now=lambda: NOW)    # clock far in the future: TTL ignored
    assert paused.count_by_year(["stacked memory"], 2024) == {2024: 90, 2025: 150, 2026: 70} and paused.searches_used == 0
    with pytest.raises(SourceError, match="paused"):
        paused.search(["never cached topic"])
    assert len(seen) == 3   # no request left the machine in cache-only mode


def test_errors_never_contain_the_key(tmp_path):
    with pytest.raises(SourceError) as info:
        client(tmp_path, status=401).search(["stacked memory"])
    assert "SERPAPI_API_KEY" in str(info.value) and KEY not in str(info.value)


def test_patent_agent_runs_on_serpapi_within_six_searches(tmp_path):
    reply = {"findings": [{"claim": "A Fixture Memory Co application describes thermal vias in stacked memory.",
                           "label": "verified_fact", "confidence": "low", "source_ids": [parse_results(PAYLOAD, NOW)[1][0].id],
                           "supporting_excerpt": "A stacked memory device includes a base die and thermal vias"}],
             "limitations": ["snippets only"]}
    router, _ = m.router_for(Scripted({"PatentReport": reply}))
    c = client(tmp_path)
    res = PatentAgent(router, c, now=lambda: NOW).run("stacked memory")
    assert res.status == "ok" and res.findings[0].label == Label.VERIFIED_FACT
    assert res.acceleration.yoy_growth_pct == 66.7          # 90 -> 150 (2024 -> 2025)
    assert res.source_usage["searches_used"] == 6 and c.searches_used <= 6   # 5 years + 1 search
    assert "Google Patents (SerpApi)" in res.coverage_note

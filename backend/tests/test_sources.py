from datetime import datetime, timezone

import httpx
import pytest

from app.agents.science.metrics import compute_acceleration
from app.sources.arxiv import ArxivClient, parse_feed
from app.sources.base import RateLimiter, SourceError
from app.sources.openalex import OpenAlexClient, reconstruct_abstract
from tests.helpers import load_json, load_text

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)


def openalex(handler, key="SECRET-KEY-123"):
    http = httpx.Client(transport=httpx.MockTransport(handler))
    return OpenAlexClient(key, http=http, sleep=lambda s: None, now=lambda: NOW)


# ---------------- OpenAlex ----------------
def test_reconstruct_abstract_orders_words_by_position():
    assert reconstruct_abstract({"world": [1], "hello": [0]}) == "hello world"
    assert reconstruct_abstract(None) is None


def test_openalex_search_parses_records_and_sends_key_and_params():
    seen = {}

    def handler(request):
        seen.update(dict(request.url.params))
        return httpx.Response(200, json=load_json("openalex_works.json"))

    records = openalex(handler).search_works("chiplet", from_year=2024, per_page=10)
    assert seen["api_key"] == "SECRET-KEY-123"
    assert seen["search"] == "chiplet" and seen["filter"] == "from_publication_date:2024-01-01"
    assert seen["per-page"] == "10" and "abstract_inverted_index" in seen["select"]
    a, b, c = records
    assert a.url == "https://doi.org/10.0000/fixture.001" and a.doi == "10.0000/fixture.001"
    assert a.abstract.startswith("We report a synthetic") and a.text_depth == "abstract_only"
    assert a.venue == "Journal of Fixture Engineering" and a.authors == ["Fixture Author One", "Fixture Author Two"]
    assert b.url == "https://example.test/b" and b.content_type.value == "preprint"
    assert b.abstract is None and b.text_depth == "metadata_only"
    assert c.url == "https://openalex.org/W0000000003"
    assert all(r.retrieved_at == NOW and r.source_name == "OpenAlex" for r in records)
    assert len({r.id for r in records}) == 3


def test_openalex_count_by_year_filters_old_years():
    client = openalex(lambda req: httpx.Response(200, json=load_json("openalex_group_by.json")))
    assert client.count_by_year("chiplet", 2024) == {2024: 100, 2025: 150, 2026: 50}


def test_count_by_year_uses_exact_phrase_in_title_or_abstract_not_loose_search():
    seen = {}

    def handler(request):
        seen.update(dict(request.url.params))
        return httpx.Response(200, json=load_json("openalex_group_by.json"))

    openalex(handler).count_by_year('high, bandwidth: "memory"|x', 2020)
    assert "search" not in seen
    assert seen["group_by"] == "publication_year"
    # syntax characters (comma, colon, quotes, pipe) are stripped so they cannot break the filter
    assert seen["filter"] == 'title_and_abstract.search:"high bandwidth memory x",from_publication_date:2020-01-01'


def test_count_by_year_empty_phrase_makes_no_request():
    def handler(request):
        raise AssertionError("no request expected")

    assert openalex(handler).count_by_year('",|:', 2020) == {}


def test_openalex_409_gives_clear_error_without_leaking_key():
    client = openalex(lambda req: httpx.Response(409, text="SECRET-KEY-123 exhausted"))
    with pytest.raises(SourceError) as err:
        client.search_works("x")
    assert err.value.status == 409 and "credits" in err.value.message
    assert "SECRET-KEY-123" not in str(err.value)


def test_openalex_retries_429_then_succeeds():
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(429, headers={"retry-after": "1"}) if len(calls) < 3 else httpx.Response(200, json={"results": []})

    assert openalex(handler).search_works("x") == []
    assert len(calls) == 3


def test_openalex_network_failure_becomes_source_error_without_key():
    def handler(request):
        raise httpx.ConnectError("connection refused for ?api_key=SECRET-KEY-123")

    with pytest.raises(SourceError) as err:
        openalex(handler).search_works("x")
    assert err.value.retryable and "SECRET-KEY-123" not in str(err.value)


def test_openalex_invalid_json_is_source_error():
    with pytest.raises(SourceError, match="not valid JSON"):
        openalex(lambda req: httpx.Response(200, text="<html>")).search_works("x")


# ---------------- arXiv ----------------
def test_arxiv_parse_feed_normalises_fields():
    records = parse_feed(load_text("arxiv_feed.xml"), NOW)
    first, second = records
    assert first.url == "https://arxiv.org/abs/0000.00001v1"
    assert first.title == "FIXTURE ARXIV D: Synthetic memory stacking preprint"
    assert first.abstract.startswith("This synthetic abstract discusses stacking memory dies with")
    assert first.published_at == "2026-02-01" and first.venue == "arXiv preprint (cs.AR)"
    assert first.authors == ["Fixture Author Four", "Fixture Author Five"]
    assert first.content_type.value == "preprint" and first.text_depth == "abstract_only"
    assert second.venue == "Fixture Letters 1 (2025)"


def test_arxiv_error_feed_raises():
    with pytest.raises(SourceError, match="malformed query"):
        parse_feed(load_text("arxiv_error.xml"), NOW)


def test_arxiv_bad_xml_raises():
    with pytest.raises(SourceError, match="not valid XML"):
        parse_feed("<html>", NOW)


def test_arxiv_query_builder():
    assert ArxivClient.build_query("high bandwidth memory") == 'all:"high bandwidth memory"'
    assert ArxivClient.build_query("chiplet") == "all:chiplet"
    assert ArxivClient.build_query("ti:chiplet") == "ti:chiplet"
    assert ArxivClient.build_query("chiplet", ["cs.AR", "physics.optics"]) == "(all:chiplet) AND (cat:cs.AR OR cat:physics.optics)"


def test_arxiv_search_waits_on_rate_limiter_before_each_request():
    ticks = {"t": 0.0}
    sleeps = []
    limiter = RateLimiter(3.0, clock=lambda: ticks["t"], sleep=lambda s: (sleeps.append(s), ticks.__setitem__("t", ticks["t"] + s)))
    http = httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(200, text=load_text("arxiv_feed.xml"))))
    client = ArxivClient(http=http, limiter=limiter, sleep=lambda s: None, now=lambda: NOW)
    assert len(client.search("chiplet")) == 2
    client.search("chiplet")
    client.search("chiplet")
    assert sleeps == [3.0, 3.0]  # first call free, then 3 s between calls


def test_arxiv_from_year_filters_old_papers_and_requests_extra_results():
    seen = {}

    def handler(request):
        seen.update(dict(request.url.params))
        return httpx.Response(200, text=load_text("arxiv_feed.xml"))  # published 2026-02-01 and 2025-10-30

    client = ArxivClient(http=httpx.Client(transport=httpx.MockTransport(handler)),
                         limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW)
    assert [r.published_at for r in client.search("x", max_results=10, from_year=2026)] == ["2026-02-01"]
    assert int(seen["max_results"]) == 30  # asks for 3x so filtering still leaves enough
    assert len(client.search("x", max_results=10, from_year=2025)) == 2
    assert len(client.search("x", max_results=10, from_year=2027)) == 0
    client.search("x", max_results=10)
    assert int(seen["max_results"]) == 10  # no filter, no extra


def test_arxiv_http_error_is_source_error():
    http = httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(503)))
    client = ArxivClient(http=http, limiter=RateLimiter(0), sleep=lambda s: None)
    with pytest.raises(SourceError) as err:
        client.search("x")
    assert err.value.retryable and err.value.status == 503


# ---------------- metrics ----------------
def test_acceleration_uses_last_two_full_years():
    m = compute_acceleration({2024: 100, 2025: 150, 2026: 50}, current_year=2026)
    assert (m.last_full_year, m.previous_year, m.yoy_growth_pct) == (2025, 2024, 50.0)


def test_acceleration_basis_names_the_exact_phrase():
    m = compute_acceleration({2024: 100, 2025: 150}, 2026, phrase="high bandwidth memory")
    assert '"high bandwidth memory"' in m.basis and "title or abstract" in m.basis


def test_acceleration_missing_or_zero_base():
    assert compute_acceleration({2025: 10}, 2026) is None
    assert compute_acceleration({2024: 0, 2025: 10}, 2026).yoy_growth_pct is None

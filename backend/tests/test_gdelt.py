"""GDELT client tests. Data is SYNTHETIC (FIXTURE); the network is faked."""

from datetime import datetime, timezone

import httpx
import pytest

from app.sources.base import RateLimiter, SourceError
from app.sources.gdelt import GdeltClient, parse_articles, parse_seendate

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
PAYLOAD = {"articles": [
    {"url": "https://news.example.invalid/a", "title": "FIXTURE  Memory maker  raises capex", "seendate": "20261105T120000Z", "domain": "news.example.invalid", "language": "English"},
    {"url": "https://other.example.invalid/b", "title": "fixture memory maker raises capex", "seendate": "20261104T010000Z", "domain": "other.example.invalid"},
    {"url": "https://news.example.invalid/c", "title": "FIXTURE second story", "seendate": "bad", "domain": "news.example.invalid"},
    {"url": "not-a-url", "title": "dropped: bad url"},
    {"url": "https://news.example.invalid/d", "title": ""},
]}


def client(handler):
    return GdeltClient(http=httpx.Client(transport=httpx.MockTransport(handler)), limiter=RateLimiter(0),
                       sleep=lambda s: None, now=lambda: NOW)


def test_parse_drops_bad_rows_and_keeps_metadata_only():
    recs = parse_articles(PAYLOAD, NOW)
    assert [r.url for r in recs] == ["https://news.example.invalid/a", "https://other.example.invalid/b", "https://news.example.invalid/c"]
    assert recs[0].title == "FIXTURE Memory maker raises capex" and recs[0].published_at == "2026-11-05"
    assert recs[2].published_at is None
    assert all(r.text_depth == "metadata_only" and r.content_type.value == "news" and r.abstract is None for r in recs)


def test_parse_seendate():
    assert parse_seendate("20261105T120000Z") == "2026-11-05" and parse_seendate("") is None


def test_search_builds_query_dedupes_titles_and_respects_limit():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen.update(request.url.params)
        return httpx.Response(200, json=PAYLOAD)

    out = client(handler).search("high bandwidth memory", max_results=10)
    assert seen["query"] == '"high bandwidth memory" sourcelang:english' and seen["mode"] == "artlist"
    assert len(out) == 2  # duplicate headline removed
    assert len(client(handler).search("HBM", max_results=1)) == 1


def test_plain_text_rejection_becomes_clear_error():
    c = client(lambda r: httpx.Response(200, text="Your query was too short or too long."))
    with pytest.raises(SourceError, match="query rejected"):
        c.search("a")


def test_rate_limit_and_unexpected_shape():
    with pytest.raises(SourceError, match="rate limited"):
        client(lambda r: httpx.Response(429)).search("hbm memory")
    with pytest.raises(SourceError, match="unexpected shape"):
        parse_articles([1, 2], NOW)

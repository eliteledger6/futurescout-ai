"""Tests for the enrichment sources added 2026-11-08: SEC XBRL fundamentals, 8-K press-release
exhibits, retraction flags and X engagement. All data is SYNTHETIC (FIXTURE); networks are faked."""

from datetime import datetime, timezone

import httpx
import pytest

from app.graph.citation_guard import apply_citation_guard
from app.schemas.common import ContentType, FindingDraft, Label, SourceRecord
from app.sources.base import RateLimiter, SourceError
from app.sources.edgar import EdgarClient
from app.sources.sec_facts import SecFactsClient, parse_facts
from app.sources.x import parse_posts
from tests import test_market_agent as m

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)


def fy(year, val, form="10-K"):
    return {"fp": "FY", "fy": year, "form": form, "frame": f"CY{year}", "end": f"{year}-12-31", "val": val}


FACTS = {"entityName": "Fixture\xa0Memory Corp", "facts": {"us-gaap": {
    "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": [fy(2023, 400e6), fy(2024, 500e6), fy(2025, 800e6),
                                                                              {"fp": "Q1", "frame": "CY2025Q1", "val": 1}]}},
    "ResearchAndDevelopmentExpense": {"units": {"USD": [fy(2024, 50e6), fy(2025, 120e6)]}},
    "NetIncomeLoss": {"units": {"USD": [fy(2025, -30e6)]}},
}}}


def test_parse_facts_computes_size_growth_and_rnd_intensity():
    f = parse_facts(FACTS, 1234567, "fallback")
    assert f.name == "Fixture Memory Corp" and f.latest_year == 2025 and f.size_class == "small"   # 800M < 1B
    assert f.revenue_growth_pct == 60.0 and f.rnd_intensity_pct == 15.0 and f.net_income[2025] == -30e6
    assert "fiscal 2025 revenue USD 800M (small by revenue)" in f.summary() and "net income -USD 30M" in f.summary()
    ifrs = parse_facts({"entityName": "Foreign Fixture", "facts": {"ifrs-full": {"Revenue": {"units": {"TWD": [fy(2025, 50e9, "20-F")]}}}}}, 9, "x")
    assert ifrs.size_class is None and ifrs.currency == "TWD" and ifrs.revenue_growth_pct is None   # USD thresholds only
    assert "size class not assigned" in ifrs.summary()
    assert parse_facts({"entityName": "Empty", "facts": {}}, 9, "x").summary().endswith("no annual revenue reported in SEC XBRL data.")
    with pytest.raises(SourceError):
        parse_facts({"nope": 1}, 9, "x")


def test_facts_client_caches_and_never_sends_anything_but_a_user_agent(tmp_path):
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=FACTS)
    c = SecFactsClient("Fixture Tester fixture@example.invalid", http=httpx.Client(transport=httpx.MockTransport(handler)),
                       limiter=RateLimiter(0), cache_dir=tmp_path, sleep=lambda s: None)
    assert c.fundamentals(1234567, "x").size_class == "small"
    assert c.fundamentals(1234567, "x").size_class == "small" and len(seen) == 1   # second call served from cache
    assert seen[0].url.path.endswith("/CIK0001234567.json") and "authorization" not in seen[0].headers


INDEX = {"directory": {"item": [{"name": "0001234567-26-000012-index.html"}, {"name": "fixt-8k.htm"},
                                 {"name": "fixt_ex99-1.htm"}, {"name": "fixt_ex99-1img.jpg"}, {"name": "R1.htm"}]}}


def test_press_releases_come_from_ex99_exhibits_of_recent_8ks():
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url.endswith("company_tickers.json"):
            return httpx.Response(200, json=m.TICKERS)
        if "CIK0001234567.json" in url:
            return httpx.Response(200, json=m.SUBMISSIONS)   # contains one 8-K (accession ...26-000012)
        if url.endswith("/000123456726000012/index.json"):
            return httpx.Response(200, json=INDEX)
        if url.endswith("fixt_ex99-1.htm"):
            return httpx.Response(200, text="<html><body><p>FIXTURE PRESS RELEASE: Fixture Memory Corp today announced volume "
                                            "production of its stacked memory product for AI customers.</p></body></html>")
        return httpx.Response(404)
    c = EdgarClient(m.UA, http=httpx.Client(transport=httpx.MockTransport(handler)), limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW)
    [rel] = c.press_releases("FIXT", limit=2)
    assert rel.content_type == ContentType.PRESS_RELEASE and rel.url.endswith("/000123456726000012/fixt_ex99-1.htm")
    assert "8-K press release" in rel.title and rel.published_at == "2026-11-01"
    rel = c.add_excerpts(rel, ["stacked memory"])
    assert rel.text_depth == "excerpt_only" and "volume production" in rel.abstract


def test_retracted_paper_cannot_verify_a_fact():
    paper = SourceRecord(url="https://doi.org/10.0000/fixture.retracted", source_name="OpenAlex", content_type=ContentType.PAPER,
                         title="FIXTURE retracted paper", abstract="we report a synthetic breakthrough in stacked memory", is_retracted=True)
    draft = FindingDraft(claim="A breakthrough in stacked memory was reported.", label=Label.VERIFIED_FACT, confidence="high",
                         source_ids=[paper.id], supporting_excerpt="synthetic breakthrough in stacked memory")
    [f] = apply_citation_guard([draft], {paper.id: paper}).findings
    assert f.label == Label.UNVERIFIED_CLAIM and "RETRACTED" in f.guard_note


def test_x_engagement_is_recorded_from_public_metrics():
    payload = {"data": [{"id": "1", "author_id": "a", "created_at": "2026-11-06T10:00:00Z", "text": "FIXTURE post",
                         "public_metrics": {"like_count": 10, "retweet_count": 5, "reply_count": 2, "quote_count": 1}},
                        {"id": "2", "author_id": "a", "created_at": "2026-11-06T10:00:00Z", "text": "FIXTURE post two"}],
               "includes": {"users": [{"id": "a", "username": "fixturemem", "name": "Fixture Memory Corp"}]}}
    recs = parse_posts(payload, NOW)
    assert recs[0].cited_by_count == 18 and recs[1].cited_by_count is None

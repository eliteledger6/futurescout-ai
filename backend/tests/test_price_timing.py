"""Price & timing risk tests. Price series are SYNTHETIC (FIXTURE) and Alpha Vantage is faked; no
request leaves the machine. The response shape follows Alpha Vantage's documented daily format."""

from datetime import date, datetime, timedelta, timezone

import httpx
import pytest

from app.agents.risk.price_timing import compute_metrics, metrics_text, run_price_timing, tickers_from_market
from app.graph import workflow
from app.report import render_markdown
from app.schemas.common import Label
from app.schemas.market import CompanyCheck, MarketResult
from app.sources.base import RateLimiter, SourceError
from app.sources.prices import AlphaVantageClient, Bar, parse_daily
from tests import test_market_agent as m
from tests.helpers import Scripted
from tests.test_workflow import clients as paper_clients
from tests.test_workflow import replies as workflow_replies

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
KEY = "FIXTURE-av-key-never-shown"


def bars(closes, start=date(2026, 6, 1)):
    return [Bar(start + timedelta(days=i), c, c * 1.01, c * 0.99, 1000) for i, c in enumerate(closes)]


def payload(closes):
    series = {}
    for b in bars(closes):
        series[b.day.isoformat()] = {"1. open": str(b.close), "2. high": str(b.high), "3. low": str(b.low),
                                      "4. close": str(b.close), "5. volume": "1000"}
    return {"Meta Data": {"2. Symbol": "FIXT"}, "Time Series (Daily)": series}


RALLY = [100 * (1.01 ** i) for i in range(100)]           # +1% a day: strongly stretched
FLAT = [100 + (i % 3) for i in range(100)]                   # sideways
SLIDE = [200 * (0.995 ** i) for i in range(100)]             # steady decline


def test_metrics_and_rule_based_levels():
    up = compute_metrics("UP", "Up Co", bars(RALLY), "src_x")
    assert up.timing_risk == "elevated" and up.return_3m_pct > 40 and any("3 months" in r for r in up.reasons)
    assert compute_metrics("FL", "Flat Co", bars(FLAT), "src_y").timing_risk == "moderate"
    down = compute_metrics("DN", "Down Co", bars(SLIDE), "src_z")
    assert down.timing_risk == "subdued" and down.return_3m_pct < 0
    txt = metrics_text(up)
    assert txt.startswith("UP closed at") and "Timing risk (rule-based): elevated" in txt
    assert "buy" not in txt.lower() and "sell" not in txt.lower()


def test_parse_and_limit_replies():
    assert [b.close for b in parse_daily(payload([1, 2, 3]), "FIXT")] == [1.0, 2.0, 3.0]   # oldest first
    with pytest.raises(SourceError, match="limit or notice"):
        parse_daily({"Information": "standard API rate limit is 25 requests per day"}, "FIXT")
    with pytest.raises(SourceError, match="not found"):
        parse_daily({"Error Message": "Invalid API call"}, "ZZZZ")


def client(tmp_path, closes=RALLY, seen=None, status=200):
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        if status != 200:
            return httpx.Response(status)
        return httpx.Response(200, json=payload(closes))
    return AlphaVantageClient(KEY, http=httpx.Client(transport=httpx.MockTransport(handler)), limiter=RateLimiter(0),
                              cache_dir=tmp_path, sleep=lambda s: None)


def test_cache_protects_the_daily_quota_and_key_is_never_stored(tmp_path):
    seen = []
    client(tmp_path, seen=seen).daily("fixt")
    c2 = client(tmp_path, seen=seen)
    c2.daily("FIXT")
    assert len(seen) == 1 and c2.cache_hits == 1 and c2.requests == 0
    assert all(KEY not in p.read_text() for p in tmp_path.iterdir())
    assert KEY not in AlphaVantageClient.source_url("FIXT") and "symbol=FIXT" in AlphaVantageClient.source_url("fixt")
    with pytest.raises(SourceError, match="invalid ticker"):
        client(tmp_path).daily("not a ticker!")


MARKET = MarketResult(topic="t", status="ok", companies=[
    CompanyCheck(ticker="FIXT", name="Fixture Memory Corp", filings_checked=2, filings_with_mentions=2),
    CompanyCheck(ticker="NONE", name="No Mention Inc", filings_checked=2, filings_with_mentions=0)])


def test_only_companies_with_topic_mentions_are_priced():
    assert tickers_from_market(MARKET) == [("FIXT", "Fixture Memory Corp")]
    assert tickers_from_market(None) == []


def test_findings_never_become_forecasts_and_quotes_are_checked(tmp_path):
    c = client(tmp_path)
    src_id = run_price_timing("t", MARKET, c, None, now=lambda: NOW).sources[0].id
    reply = {"findings": [
        {"claim": "Fixture Memory Corp shares are stretched after a large run-up.", "label": "ai_interpretation",
         "confidence": "medium", "source_ids": [src_id], "companies": ["Fixture Memory Corp"]},
        {"claim": "The price will keep rising next month.", "label": "forecast", "confidence": "low", "source_ids": [src_id]},
        {"claim": "Timing risk is elevated by rule.", "label": "verified_fact", "confidence": "medium",
         "source_ids": [src_id], "supporting_excerpt": "Timing risk (rule-based): elevated"}],
        "limitations": ["100 trading days only"]}
    router, _ = m.router_for(Scripted({"TimingReport": reply}))
    res = run_price_timing("t", MARKET, c, router, now=lambda: NOW)
    t1, t2, t3 = res.findings
    assert [f.fid for f in res.findings] == ["T1", "T2", "T3"] and res.status == "ok"
    assert t2.label == Label.AI_INTERPRETATION and "forecasts are not allowed" in t2.guard_note
    assert t3.label == Label.VERIFIED_FACT
    assert res.metrics[0].timing_risk == "elevated" and "not a buy or sell signal" in res.coverage_note


def test_no_key_or_no_companies_means_nothing_is_fetched(tmp_path):
    assert run_price_timing("t", MARKET, None, None).limitations[0].startswith("Prices were not fetched")
    seen = []
    res = run_price_timing("t", MarketResult(topic="t", status="ok"), client(tmp_path, seen=seen), None)
    assert res.metrics == [] and seen == []


def test_workflow_adds_timing_to_the_risk_stage_and_report(tmp_path):
    script = Scripted(workflow_replies(
        MarketReport={"findings": [], "limitations": []},
        TimingReport={"findings": [{"claim": "Fixture Memory Corp looks stretched on 100-day data.", "label": "ai_interpretation",
                                    "confidence": "low", "source_ids": []}], "limitations": []}))
    router, rclient = m.router_for(script)
    oa, ax = paper_clients()
    market = m.MarketAgent(router, m.edgar(), None, companies=m.COMPANIES[:1], now=lambda: NOW)
    report = workflow.run_research("chiplet interconnect", router=router, openalex=oa, arxiv=ax, max_papers=10,
                                   market_agent=market, prices=client(tmp_path), now=lambda: NOW)
    assert report.timing is not None and report.timing.metrics[0].ticker == "FIXT"
    inv = next(c for c in rclient.calls if "PRICE & TIMING RISK" in c["messages"][-1]["content"])
    assert "timing risk elevated" in inv["messages"][-1]["content"]
    md = render_markdown(report)
    assert "## Price and timing risk" in md and "not a buy or sell signal" in md and "**elevated**" in md

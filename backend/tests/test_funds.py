"""Topic funds (SIMULATION): basket tiers, decision rules, paper trades, NEAR Intents dry-run route check. All faked."""

from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace as NS

import httpx
import pytest
from fastapi.testclient import TestClient

import app.fund as fund_mod
from app.fund import (PriceBook, build_basket, check_routes, decide, load_fund_config, mark_to_market, needs_decision,
                      new_fund, save_fund)
from app.fund.intents import OneClickClient
from app.sources.prices import Bar

NOW = datetime(2026, 11, 9, 12, tzinfo=timezone.utc)
CFG = load_fund_config()


def co(ticker, size, mentions=2):
    return NS(ticker=ticker, name=f"{ticker} Corp", filings_with_mentions=mentions, fundamentals={"size_class": size})


def scout(ticker, size, score=50.0, off=False):
    return NS(ticker=ticker, name=f"{ticker} Inc", sec_listed=True, off_sector=off, fundamentals={"size_class": size},
              patents=3, papers=1, filings=0, next_runner_score=score)


def report(risks=None):
    risks = risks or {}
    return NS(topic="Fixture tech", generated_at=NOW, sector="semiconductors",
              market=NS(companies=[co("BIG1", "large"), co("BIG2", "large"), co("MIDA", "mid"), co("NOMENTION", "large", 0),
                                   co("NOSIZE", None)]),
              scout=NS(candidates=[scout("SMOL", "small"), scout("BANK", "large", off=True), scout("MIDB", "mid", 20)]),
              timing=NS(metrics=[NS(ticker=t, timing_risk=r) for t, r in risks.items()]))


class FakeBook(PriceBook):
    def __init__(self, closes):
        super().__init__(None, cache_dir=NS())  # type: ignore[arg-type]
        self.closes = closes

    def bars(self, ticker):
        p = self.closes.get(ticker.upper())
        return [Bar(day=date(2026, 11, 6), close=p, high=p, low=p, volume=1)] if p else []


PRICES = {"BIG1": 100.0, "BIG2": 50.0, "MIDA": 20.0, "MIDB": 10.0, "SMOL": 5.0, "SPY": 600.0}


@pytest.fixture
def verdict(monkeypatch):
    state = {"band": "building", "score": 60.0}
    monkeypatch.setattr(fund_mod, "build_verdict", lambda r: {"available": True, **state})
    return state


def test_basket_tiers_filters_and_ranking():
    b = build_basket(report(), CFG)
    assert [(c.ticker, c.tier) for c in b] == [("BIG1", "low"), ("BIG2", "low"), ("MIDA", "medium"), ("MIDB", "medium"), ("SMOL", "high")]
    # no topic mention, no size class, off-sector scout: all left out


def test_building_band_invests_75pct_split_by_tier_with_fees(verdict):
    f = new_fund("Fixture tech", "semiconductors", CFG, NOW)
    d = decide(f, "run1", report(), FakeBook(PRICES), CFG, NOW, "first decision for this topic")
    assert d.band == "building" and d.target_invested_pct == 75.0
    assert d.tier_targets_usd == {"low": 4500.0, "medium": 2250.0, "high": 750.0}
    assert all(t.side == "buy" for t in d.trades) and len(d.trades) == 5
    invested = sum(t.usd for t in d.trades)
    assert invested == pytest.approx(7500, abs=0.5)
    assert f.cash_usd == pytest.approx(10000 - 7500 * 1.003, abs=0.5)        # 0.3% assumed cost per trade
    assert d.sha256 and len(d.sha256) == 64 and any("75%" in r for r in d.reasons)


def test_stretched_tier_is_staged_and_review_is_due_later(verdict):
    f = new_fund("Fixture tech", None, CFG, NOW)
    d = decide(f, "run1", report({"BIG1": "high", "BIG2": "high"}), FakeBook(PRICES), CFG, NOW, "first")
    assert d.staged_tiers == ["low"] and d.tier_targets_usd["low"] == 2250.0
    assert needs_decision(f, "run1", NOW + timedelta(days=1), CFG) is None
    assert "staged entry" in needs_decision(f, "run1", NOW + timedelta(days=8), CFG)
    assert needs_decision(f, "run2", NOW, CFG) == "a newer report is available"


def test_score_drop_halves_and_insufficient_sells_everything(verdict):
    f = new_fund("Fixture tech", None, CFG, NOW)
    book = FakeBook(PRICES)
    decide(f, "run1", report(), book, CFG, NOW, "first")
    verdict.update(score=50.0)                                   # -10 points, still "building"
    d2 = decide(f, "run2", report(), book, CFG, NOW, "newer report")
    assert d2.target_invested_pct == 37.5 and any("halved" in r for r in d2.reasons)
    assert {t.side for t in d2.trades} == {"sell"}
    verdict.update(band="insufficient", score=None)
    d3 = decide(f, "run3", report(), book, CFG, NOW, "newer report")
    assert d3.target_invested_pct == 0 and f.holdings == [] and all(t.side == "sell" for t in d3.trades)
    assert f.cash_usd < 10000                                   # fees were paid, no money appeared


def test_mark_to_market_and_benchmark(verdict, tmp_path):
    f = new_fund("Fixture tech", None, CFG, NOW)
    decide(f, "run1", report(), FakeBook(PRICES), CFG, NOW, "first")
    up = {k: v * 1.1 for k, v in PRICES.items()}
    mark_to_market(f, FakeBook(up), NOW)
    s = f.summary()
    assert s["value_usd"] > 10000 * 0.99 and s["holdings"] == 5
    assert f.history[-1].benchmark_value_usd == pytest.approx(11000, abs=1)
    assert (tmp_path / "fixture-tech.json") == save_fund(f, tmp_path)


def test_route_needs_symbol_and_price_match_and_dry_quote_parses():
    tokens = [{"symbol": "BIG1on", "assetId": "nep141:big1.on", "blockchain": "eth", "price": 101.0},
              {"symbol": "BIG2", "assetId": "nep141:meme", "blockchain": "sol", "price": 0.002}]
    sent = []

    def handler(req):
        if req.url.path == "/v0/tokens":
            return httpx.Response(200, json=tokens)
        sent.append(req.read())
        return httpx.Response(201, json={"quote": {"amountInUsd": "100.0", "amountOutUsd": "99.5", "amountOutFormatted": "0.98",
                                                   "timeEstimate": 10}, "correlationId": "c1"})
    client = OneClickClient("https://x.test", http=httpx.Client(transport=httpx.MockTransport(handler)), now=lambda: NOW, bridge_rpc=None)
    assert client.route_for("BIG1", 100.0, 15).available
    r2 = client.route_for("BIG2", 50.0, 15)
    assert not r2.available and "unrelated" in r2.note                  # same symbol, wrong price: not the stock
    assert not client.route_for("MIDA", 20.0, 15).available
    q = client.dry_quote("nep141:usdc", 6, "nep141:big1.on", 100.0, "intents.near")
    assert q.cost_pct == 0.5 and q.error is None
    assert b'"dry":true' in sent[0].replace(b" ", b"")                  # only ever dry quotes


def test_check_routes_quotes_only_tradable_holdings(verdict):
    f = new_fund("Fixture tech", None, CFG, NOW)
    decide(f, "run1", report(), FakeBook(PRICES), CFG, NOW, "first")
    tokens = [{"symbol": "BIG1on", "assetId": "nep141:big1.on", "blockchain": "eth", "price": 100.0}]
    handler = lambda req: httpx.Response(200, json=tokens) if req.url.path == "/v0/tokens" else httpx.Response(  # noqa: E731
        201, json={"quote": {"amountInUsd": "1", "amountOutUsd": "1"}})
    stats = check_routes(f, OneClickClient("https://x.test", http=httpx.Client(transport=httpx.MockTransport(handler))), CFG)
    assert stats == {"checked": 5, "available": 1, "quoted": 1, "errors": []}


def test_funds_api_lists_and_details(verdict, tmp_path):
    from app.api.main import create_app
    from app.config import Settings
    f = new_fund("Fixture tech", None, CFG, NOW)
    decide(f, "run1", report(), FakeBook(PRICES), CFG, NOW, "first")
    save_fund(f, tmp_path)
    app = create_app(Settings(_env_file=None), store=NS(list=lambda limit=50: [], get=lambda i: None), funds_dir=tmp_path,
                     portfolio_path=tmp_path / "pf.json", ledger=NS())
    c = TestClient(app)
    lst = c.get("/api/funds").json()
    assert lst["label"] == "simulation" and lst["funds"][0]["slug"] == "fixture-tech"
    det = c.get("/api/funds/fixture-tech").json()
    assert det["summary"]["holdings"] == 5 and det["decisions"][0]["band"] == "building"
    assert c.get("/api/funds/..%2Fsecret").status_code == 404


def test_unpriced_companies_wait_and_trigger_a_price_review(verdict):
    f = new_fund("Fixture tech", None, CFG, NOW)
    d = decide(f, "run1", report(), FakeBook({k: v for k, v in PRICES.items() if k != "SMOL"}), CFG, NOW, "first")
    assert d.waiting_for_price == ["SMOL"] and any("SMOL" in r for r in d.reasons)
    assert needs_decision(f, "run1", NOW + timedelta(hours=2), CFG) is None
    assert "price review" in needs_decision(f, "run1", NOW + timedelta(days=1), CFG)
    d2 = decide(f, "run1", report(), FakeBook(PRICES), CFG, NOW + timedelta(days=1), "price review")
    assert d2.waiting_for_price == [] and any(t.ticker == "SMOL" and t.side == "buy" for t in d2.trades)


def test_bridge_listed_stock_token_needs_a_matching_quoted_price():
    """Ondo-style tokens are only in the bridge list (no prices): the price implied by a dry quote must match the stock."""
    bridge = {"result": {"tokens": [
        {"asset_name": "MIDAon", "intents_token_id": "nep141:bnb-0xmida.omdep.near", "defuse_asset_identifier": "eth:56:0xmida"},
        {"asset_name": "SMOLon", "intents_token_id": "nep141:bnb-0xsmol.omdep.near", "defuse_asset_identifier": "eth:56:0xsmol"}]}}
    bodies = []

    def handler(req):
        if req.url.path == "/v0/tokens":
            return httpx.Response(200, json=[])
        if req.url.host == "bridge.test":
            return httpx.Response(200, json=bridge)
        body = req.read().decode()
        bodies.append(body)
        out = "5.0" if "0xmida" in body else "0.001"          # $100 -> 5 MIDAon ($20, matches) / 0.001 SMOLon ($100,000, unrelated)
        return httpx.Response(201, json={"quote": {"amountInUsd": "100.0", "amountOutUsd": "99.0", "amountOutFormatted": out}})
    client = OneClickClient("https://x.test", http=httpx.Client(transport=httpx.MockTransport(handler)), now=lambda: NOW,
                            bridge_rpc="https://bridge.test/rpc")
    assert not client.route_for("MIDA", 20.0, 15).available          # no pay asset configured: cannot verify the price, so not claimed
    client.pay = ("nep141:usdc", 6, "intents.near")
    ok = client.route_for("MIDA", 20.0, 15)
    assert ok.available and ok.symbol == "MIDAon" and ok.blockchain == "BNB Chain" and ok.token_price_usd == 20.0
    bad = client.route_for("SMOL", 5.0, 15)
    assert not bad.available and "unrelated" in bad.note
    assert not client.route_for("BIG2", 50.0, 15).available          # in neither list
    assert bodies and all('"dry":true' in b.replace(" ", "") for b in bodies)   # only ever dry quotes


def test_confidence_below_70_shrinks_the_position(verdict):
    verdict.update(band="strong", score=76.0, confidence_pct=56.0)
    f = new_fund("Fixture tech", None, CFG, NOW)
    d = decide(f, "run1", report(), FakeBook(PRICES), CFG, NOW, "first")
    assert d.target_invested_pct == 80.0 and d.confidence_pct == 56.0          # strong = 100% x 56/70
    assert any("below the 70%" in r for r in d.reasons)
    verdict.update(confidence_pct=75.0)
    f2 = new_fund("Fixture tech", None, CFG, NOW)
    assert decide(f2, "run1", report(), FakeBook(PRICES), CFG, NOW, "first").target_invested_pct == 100.0

"""Paper portfolio (SIMULATION) and testnet balance tests. Prices, reports and the NEAR balance are all
FIXTURES / fakes; nothing leaves the machine."""

from datetime import date, datetime, timedelta, timezone

import httpx
from fastapi.testclient import TestClient

from app.api import create_app
from app.api.store import FileStore
from app.chain.near_record import NearRecordError
from app.config import Settings
from app.portfolio import Portfolio, add_positions_from_report, load_portfolio, price_position, save_portfolio, update_prices
from app.schemas.research import ResearchReport
from app.schemas.scout import CompanySignal, ScoutResult
from app.sources.base import RateLimiter
from app.sources.prices import AlphaVantageClient, Bar
from app.chain.near_record import read_balance
from tests.test_price_timing import payload

NOW = datetime(2026, 11, 8, 12, tzinfo=timezone.utc)


def report(run_id="r1", day=NOW, tickers=("GLSS", "APLD", "FIXT", "XTRA")) -> ResearchReport:
    cands = [CompanySignal(name=f"{t} Fixture Co", ticker=t, cik=i + 1, sec_listed=True, next_runner_score=70 - i) for i, t in enumerate(tickers)]
    return ResearchReport(topic="glass core substrate", generated_at=day, total_cost_usd=0.2,
                          scout=ScoutResult(topic="glass core substrate", status="ok", candidates=cands))


def bars(closes, start=date(2026, 10, 1)):
    return [Bar(start + timedelta(days=i), c, c, c, 1000) for i, c in enumerate(closes)]


def test_positions_come_from_scout_candidates_capped_per_report_and_never_duplicated():
    pf = Portfolio(notional_usd=10_000, positions_per_report=3)
    assert add_positions_from_report(pf, "r1", report()) == 3
    assert [p.ticker for p in pf.positions] == ["GLSS", "APLD", "FIXT"] and all(p.status == "pending" for p in pf.positions)
    assert pf.positions[0].report_date == "2026-11-08" and pf.positions[0].notional_usd == 10_000
    assert add_positions_from_report(pf, "r1", report()) == 0                       # same report again: nothing
    assert add_positions_from_report(pf, "r2", report("r2")) == 3                   # another report may hold the same tickers
    assert add_positions_from_report(pf, "r3", ResearchReport(topic="x", generated_at=NOW)) == 0   # no scout: nothing


def test_pricing_uses_first_close_on_or_after_the_report_date():
    pf = Portfolio(notional_usd=10_000, positions_per_report=3)
    add_positions_from_report(pf, "r1", report(day=datetime(2026, 10, 5, tzinfo=timezone.utc), tickers=("GLSS",)))
    p = pf.positions[0]
    price_position(p, bars([100, 101, 102, 103, 104, 110, 120, 125]), "https://fixture")   # 2026-10-01..10-08
    assert p.status == "open" and p.entry_date == "2026-10-05" and p.entry_close == 104 and round(p.shares, 4) == round(10_000 / 104, 4)
    assert p.last_date == "2026-10-08" and p.last_close == 125 and p.return_pct == round((125 / 104 - 1) * 100, 2)
    assert p.value_usd == round(10_000 / 104 * 125, 2)
    # a report dated after the last bar stays pending, honestly
    late = Portfolio(notional_usd=1, positions_per_report=1)
    add_positions_from_report(late, "r9", report(day=datetime(2026, 12, 1, tzinfo=timezone.utc), tickers=("GLSS",)))
    price_position(late.positions[0], bars([1, 2]), "u")
    assert late.positions[0].status == "pending" and "no close on or after 2026-12-01" in late.positions[0].note
    assert pf.summary()["return_pct"] == round((125 / 104 - 1) * 100, 2) and pf.summary()["open"] == 1


def av_client(series: dict[str, list[float]], limit_after: int | None = None):
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        sym = request.url.params["symbol"]
        calls.append(sym)
        assert "apikey" in request.url.params and request.url.params["apikey"] == "FIXTURE-key"
        if limit_after is not None and len(calls) > limit_after:
            return httpx.Response(200, json={"Information": "fixture rate limit"})
        if sym not in series:
            return httpx.Response(200, json={"Error Message": "Invalid API call"})
        return httpx.Response(200, json=payload(series[sym]))
    c = AlphaVantageClient("FIXTURE-key", http=httpx.Client(transport=httpx.MockTransport(handler)), limiter=RateLimiter(0),
                           cache_dir=None, sleep=lambda s: None)
    return c, calls


def test_update_prices_respects_the_request_budget_and_tracks_a_benchmark(tmp_path):
    pf = Portfolio(notional_usd=10_000, positions_per_report=3)
    add_positions_from_report(pf, "r1", report(day=datetime(2026, 6, 10, tzinfo=timezone.utc), tickers=("GLSS", "APLD", "NOPE")))
    client, calls = av_client({"GLSS": [100.0] * 50 + [120.0] * 50, "APLD": [50.0] * 100, "SOXX": [200.0] * 50 + [210.0] * 50})
    out = update_prices(pf, client, max_requests=10, benchmark="SOXX")
    by = {p.ticker: p for p in pf.positions}
    assert by["GLSS"].status == "open" and by["GLSS"].return_pct == 20.0 and by["APLD"].return_pct == 0.0
    assert by["NOPE"].status == "error" and "not found" in by["NOPE"].note
    assert pf.benchmark.ticker == "SOXX" and pf.benchmark.return_pct == 5.0 and pf.benchmark.entry_date == by["GLSS"].entry_date
    assert out["priced"] == 2 and out["requests"] == 4 and calls == ["GLSS", "APLD", "NOPE", "SOXX"]
    s = pf.summary()
    assert s["invested_usd"] == 20_000 and s["value_usd"] == 22_000 and s["return_pct"] == 10.0 and s["best"] == "GLSS"
    # budget: only one request allowed -> the rest are skipped with a note, nothing crashes
    pf2 = Portfolio(notional_usd=1, positions_per_report=3)
    add_positions_from_report(pf2, "r1", report(day=datetime(2026, 6, 10, tzinfo=timezone.utc), tickers=("GLSS", "APLD")))
    client2, _ = av_client({"GLSS": [1.0] * 100, "APLD": [1.0] * 100})
    out2 = update_prices(pf2, client2, max_requests=1, benchmark="")
    assert out2["requests"] == 1 and any("budget" in e for e in out2["errors"])
    # round trip to disk keeps everything
    save_portfolio(pf, tmp_path / "p.json")
    again = load_portfolio(tmp_path / "p.json", notional=1, per_report=1)
    assert again.positions[0].return_pct == 20.0 and again.benchmark.return_pct == 5.0 and again.kind == "simulation"


def test_read_balance_is_a_plain_view_and_refuses_mainnet():
    def handler(request: httpx.Request) -> httpx.Response:
        body = request.read().decode()
        assert '"view_account"' in body and '"seller.testnet"' in body
        return httpx.Response(200, json={"result": {"amount": str(25 * 10**23), "locked": "0", "storage_usage": 500}})
    http = httpx.Client(transport=httpx.MockTransport(handler))
    assert read_balance(http, "https://rpc.testnet.near.org", "seller.testnet") == {"available_near": 2.5, "locked_near": 0.0, "storage_bytes": 500}
    try:
        read_balance(http, "https://rpc.mainnet.near.org", "seller.near")
    except NearRecordError:
        pass
    else:
        raise AssertionError("mainnet must be refused")


def test_api_portfolio_route_and_no_report_selling_routes(tmp_path):
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "report_fixture1.json").write_text(report(day=NOW).model_dump_json(), encoding="utf-8")
    app = create_app(Settings(_env_file=None, near_ai_api_key="k", near_testnet_account_id="seller.testnet"), store=FileStore(runs),
                     portfolio_path=tmp_path / "portfolio.json")
    client = TestClient(app)
    pf = client.get("/api/portfolio").json()
    assert pf["label"] == "simulation" and pf["summary"]["positions"] == 3 and pf["summary"]["pending"] == 3
    assert pf["positions"][0]["ticker"] == "GLSS" and pf["prices_configured"] is False and "No money moves" in pf["disclaimer"]
    assert (tmp_path / "portfolio.json").is_file()
    for gone in ("/api/treasury", "/api/market"):                       # report selling was removed on 2026-11-10
        assert client.get(gone).status_code == 404

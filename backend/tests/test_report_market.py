"""Report market: fresh reports are sold to trading bots for 24 h (402 until paid), checked on chain, then free."""
from datetime import datetime, timedelta, timezone

import pytest

from app.fund.economy import EconomyConfig, near_to_yocto
from app.fund.report_market import MarketState, buy, is_locked, unlock_at

NOW = datetime(2026, 11, 10, 12, tzinfo=timezone.utc)
CFG = EconomyConfig(market_open=True, seller_account="report-agent.near", embargo_hours=24)


def tx(signer="bot.near", receiver="report-agent.near", amount=4.0, h="TX1"):
    return {"result": {"status": {"SuccessValue": ""}, "transaction": {"hash": h, "signer_id": signer, "receiver_id": receiver,
            "actions": [{"Transfer": {"deposit": str(near_to_yocto(amount))}}]}}}


def test_a_report_is_locked_for_24h_then_free():
    assert is_locked(NOW - timedelta(hours=2), CFG, NOW) and unlock_at(NOW, CFG) == NOW + timedelta(hours=24)
    assert not is_locked(NOW - timedelta(hours=25), CFG, NOW)
    assert not is_locked(NOW, EconomyConfig(seller_account="r.near"), NOW)          # market closed by default: nothing locked


def test_payment_is_checked_on_chain_and_redeemed_once(tmp_path):
    st = MarketState()
    sale = buy(state=st, path=tmp_path / "s.json", run_id="r1", buyer="Bot.near", tx_hash="TX1", price_near=4.0, cfg=CFG,
               read=lambda h, who: tx(), now=NOW)
    assert sale.amount_near == 4.0 and sale.token and st.by_token(sale.token).run_id == "r1"
    again = buy(state=st, path=tmp_path / "s.json", run_id="r1", buyer="bot.near", tx_hash="TX1", price_near=4.0, cfg=CFG,
                read=lambda h, who: tx(), now=NOW)
    assert again.token == sale.token and len(st.sales) == 1                         # same purchase asked twice: same access
    with pytest.raises(ValueError, match="already used"):
        buy(state=st, path=tmp_path / "s.json", run_id="r2", buyer="bot.near", tx_hash="TX1", price_near=4.0, cfg=CFG,
            read=lambda h, who: tx(), now=NOW)
    for bad, match in ((tx(receiver="evil.near", h="TX2"), "not the report agent"), (tx(amount=1.0, h="TX2"), "too small"),
                       (tx(signer="other.near", h="TX2"), "not by the buyer")):
        with pytest.raises(ValueError, match=match):
            buy(state=st, path=tmp_path / "s.json", run_id="r2", buyer="bot.near", tx_hash="TX2", price_near=4.0, cfg=CFG,
                read=lambda h, who, b=bad: b, now=NOW)
    with pytest.raises(ValueError, match="closed"):
        buy(state=st, path=tmp_path / "s.json", run_id="r2", buyer="bot.near", tx_hash="TX3", price_near=4.0,
            cfg=EconomyConfig(seller_account="r.near"), read=lambda h, who: tx(), now=NOW)


def test_api_locks_a_fresh_report_with_buying_instructions(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    import app.api.main as api_main
    from app.api.store import FileStore
    from app.config import Settings
    from tests.test_portfolio_treasury import report
    fc = api_main.load_fund_config()
    fc.economy = CFG
    monkeypatch.setattr(api_main, "load_fund_config", lambda: fc)
    runs = tmp_path / "runs"
    runs.mkdir()
    fresh = report(day=datetime.now(timezone.utc))
    (runs / "report_fresh1.json").write_text(fresh.model_dump_json(), encoding="utf-8")
    client = TestClient(api_main.create_app(Settings(_env_file=None, near_ai_api_key="k"), store=FileStore(runs),
                                            trading_dir=tmp_path / "trading"))
    row = client.get("/api/runs").json()[0]
    assert row["locked"] is True and row["unlock_at"]
    r = client.get("/api/runs/report_fresh1")
    assert r.status_code == 402 and r.json()["detail"]["pay_to"] == "report-agent.near" and r.json()["detail"]["how_to_buy"]
    m = client.get("/api/market").json()
    scored = client.get("/api/runs").json()[0]["score"] is not None
    assert m["open"] and m["pay_to"] == "report-agent.near" and m["how_to_buy"]
    assert [r["run_id"] for r in m["reports"]] == (["report_fresh1"] if scored else [])   # only scored reports are on sale
    assert client.get("/api/runs/report_fresh1?access=wrong").status_code == 402


def test_owner_can_keep_a_report_always_free():
    cfg = EconomyConfig(market_open=True, seller_account="r.near", always_free=["demo1"])
    assert not is_locked(NOW, cfg, NOW, "demo1") and is_locked(NOW, cfg, NOW, "other")


def test_paid_only_reports_never_unlock_without_payment():
    cfg = EconomyConfig(market_open=True, seller_account="r.near", embargo_hours=None, always_free=["demo1"])
    assert unlock_at(NOW, cfg) is None
    assert is_locked(NOW - timedelta(days=365), cfg, NOW, "old")              # a year later: still locked
    assert not is_locked(NOW, cfg, NOW, "demo1")                              # the owner's demo report stays free


def test_shipped_config_keeps_reports_paid_only():
    from app.fund import load_fund_config
    ec = load_fund_config().economy
    assert ec.market_open and ec.embargo_hours is None                       # owner 2026-11-10: never free without payment


def test_new_reports_are_unlocked_for_the_demo_and_marked_so():
    from app.fund.report_market import demo_free
    cfg = EconomyConfig(market_open=True, seller_account="r.near", embargo_hours=None, always_free=["demo1"],
                        demo_free_from=NOW - timedelta(hours=1))
    assert not is_locked(NOW, cfg, NOW, "new") and demo_free(NOW, cfg, "new")                       # written after the date: open, marked
    assert is_locked(NOW - timedelta(days=2), cfg, NOW, "old") and not demo_free(NOW - timedelta(days=2), cfg, "old")   # older: still paid
    assert demo_free(NOW - timedelta(days=2), cfg, "demo1")                                         # listed: open, marked
    assert not demo_free(NOW, EconomyConfig(seller_account="r.near", demo_free_from=NOW), "x")      # market closed: nothing to mark


def test_api_sells_a_report_for_a_payment_checked_on_chain(tmp_path, monkeypatch):
    """The whole purchase route (it answered 500 for every request from 2026-11-10 to 2026-11-11: an argument had
    slipped into a comment, and only the function underneath was tested)."""
    from fastapi.testclient import TestClient
    import app.api.main as api_main
    import app.fund.economy as economy
    from app.api.store import FileStore
    from app.config import Settings
    from app.fund.live import OneClickLive
    from tests.test_portfolio_treasury import report
    fc = api_main.load_fund_config()
    fc.economy = CFG
    monkeypatch.setattr(api_main, "load_fund_config", lambda: fc)
    monkeypatch.setattr(OneClickLive, "price_usd", lambda self, asset: 2.5)
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "report_fresh1.json").write_text(report(day=datetime.now(timezone.utc)).model_dump_json(), encoding="utf-8")
    client = TestClient(api_main.create_app(Settings(_env_file=None, near_ai_api_key="k"), store=FileStore(runs),
                                            trading_dir=tmp_path / "trading"))
    price = client.get("/api/runs").json()[0]["price_near"]
    assert price and price > 0

    def chain(amount_near, signer="bot.near", to="report-agent.near"):
        return lambda http, rpc, h, who: {"result": {"status": {"SuccessValue": ""}, "transaction": {
            "hash": h, "signer_id": signer, "receiver_id": to, "actions": [{"Transfer": {"deposit": str(int(amount_near * 1e24))}}]}}}

    body = {"run_id": "report_fresh1", "tx_hash": "TXPAID", "buyer": "bot.near"}
    monkeypatch.setattr(economy, "read_tx", chain(price / 2))
    assert client.post("/api/market/buy", json=body).status_code == 402                      # paid too little
    monkeypatch.setattr(economy, "read_tx", chain(price, to="someone-else.near"))
    assert client.post("/api/market/buy", json=body).status_code == 402                      # paid somebody else
    monkeypatch.setattr(economy, "read_tx", chain(price))
    r = client.post("/api/market/buy", json=body)
    assert r.status_code == 200 and r.json()["report"]["topic"] and r.json()["access_token"]
    token = r.json()["access_token"]
    assert client.get(f"/api/runs/report_fresh1?access={token}").status_code == 200          # the token opens the report
    assert client.get("/api/runs/report_fresh1").status_code == 402                          # still locked for everyone else
    assert client.post("/api/market/buy", json={**body, "buyer": "other.near"}).status_code == 402   # the payment cannot be used twice

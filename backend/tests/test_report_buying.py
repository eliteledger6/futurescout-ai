"""The trading agent buys only reports it could act on now (owner 2026-11-11). Network, prices and the store are faked;
nothing is paid (execute=False)."""
import importlib.util
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from app.fund import load_fund_config
from tests.test_db import fixture_report


def load_ft():
    spec = importlib.util.spec_from_file_location("ft_rb", Path(__file__).resolve().parents[1] / "scripts" / "fund_trade.py")
    ft = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ft)
    return ft


def test_only_reports_with_a_tradable_strong_or_building_stock_are_bought(tmp_path, monkeypatch, capsys):
    ft = load_ft()
    import app.api.main as api_main
    rep = fixture_report()
    store = SimpleNamespace(get=lambda rid: (rep, None))
    monkeypatch.setattr(api_main, "_default_store", lambda s: store)
    monkeypatch.setattr(ft, "ECONOMY", tmp_path / "economy.json")
    monkeypatch.setattr(ft, "make_executor", lambda *a, **k: SimpleNamespace(kill_switch=lambda: False))
    monkeypatch.setattr(ft, "near_price", lambda ex: 3.6)
    monkeypatch.setattr(ft, "live_fund_value", lambda *a, **k: 100.0)
    toks = [{"topic": "chiplet", "run_id": "r1"}, {"topic": "6G", "run_id": "r2"}, {"topic": "hbm", "run_id": "r3"}]
    C = lambda t, band, q, score: SimpleNamespace(topic=t, verdict_band=band, quotable=q, score=score, confidence_pct=40.0, ticker=t[:4].upper())
    cands = [C("chiplet", "strong", True, 70), C("6G", "early", True, 60), C("hbm", "strong", False, 80)]
    s = SimpleNamespace(fund_mainnet_credentials=lambda: None, fund_mainnet_account_id="", oneclick_api_key=None)
    ft.economy_buy_reports(s, load_fund_config(), toks, cands, datetime(2026, 11, 11, tzinfo=timezone.utc), execute=False, only_actionable=True)
    out = capsys.readouterr().out
    assert "report '6G': not bought (rated 'early'" in out
    assert "report 'hbm': not bought (NEAR Intents cannot quote its stocks right now" in out
    assert "report 'chiplet':" in out and "chiplet': not bought (" not in out          # priced and considered

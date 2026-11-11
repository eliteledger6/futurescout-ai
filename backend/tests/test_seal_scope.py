"""Owner 2026-11-11: only reports are sealed on NEAR by default; fund decisions and trade records only when switched on."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

from app.config import Settings


def load_ft():
    spec = importlib.util.spec_from_file_location("ft_seal", Path(__file__).resolve().parents[1] / "scripts" / "fund_trade.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_fund_decisions_and_trades_are_not_sealed_unless_switched_on():
    s = Settings(_env_file=None)
    assert s.seal_fund_decisions is False and s.seal_trades is False


def test_trade_record_is_sealed_only_when_switched_on(monkeypatch):
    ft = load_ft()
    import app.chain.near_record as nr
    calls = []

    class Recorder:
        def record_fund_decision(self, key, payload):
            calls.append(key)
            return SimpleNamespace(as_dict=lambda: {"network": "mainnet", "tx_hash": "abc"})

    monkeypatch.setattr(nr, "make_recorder", lambda s: Recorder())
    p = SimpleNamespace(id="p1", sha256="f" * 64, status="done", symbol="INTCon", usd=10, mode="live", chain=None)
    ft.seal(SimpleNamespace(seal_trades=False), p)
    assert calls == [] and p.chain is None                       # default: nothing signed, nothing spent
    ft.seal(SimpleNamespace(seal_trades=True), p)
    assert calls == ["trade_p1"] and p.chain["network"] == "mainnet"


def test_funds_script_seals_decisions_only_when_switched_on():
    src = (Path(__file__).resolve().parents[1] / "scripts" / "funds.py").read_text(encoding="utf-8")
    assert "make_recorder(s) if (args.seal_missing or (s.seal_fund_decisions and not args.no_seal)) else None" in src

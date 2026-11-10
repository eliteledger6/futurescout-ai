"""Trading strategy: triggers are pure code; the agent's answer is checked against the fixed rules. All fixtures."""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace as NS

from app.agents.trader.agent import Candidate
from app.fund.strategy import StrategyConfig, StrategyDecision, assess, detect_triggers

NOW = datetime(2026, 11, 10, 9, tzinfo=timezone.utc)
CFG = StrategyConfig()
TOKENS = [{"ticker": "MRVL", "topic": "hbm", "run_id": "run_a", "band": "strong", "score": 72.0, "confidence_pct": 46.8},
          {"ticker": "GOOGL", "topic": "AI agents", "run_id": "run_b", "band": "strong", "score": 73.3, "confidence_pct": 38.7}]


def test_triggers_fire_once_per_event_and_review_is_periodic():
    closes = {"MRVL": ("2026-11-09", 154.6, 141.2), "GOOGL": ("2026-11-09", 284.0, 286.0)}      # +9.5% / -0.7%
    t = detect_triggers(tokens=TOKENS, seen_runs={}, closes=closes, seen_closes={}, last_check=None, now=NOW, cfg=CFG, held={"GOOGL"})
    kinds = [(x.kind, x.ticker) for x in t]
    assert ("new_report", "MRVL") in kinds and ("new_report", "GOOGL") in kinds and ("review", "") in kinds
    assert not any(k in ("price_drop", "price_jump") for k, _ in kinds)                       # 9.5% is below the 10% jump threshold
    drop = {"MRVL": ("2026-11-09", 130.0, 141.2)}                                               # -7.9%
    t2 = detect_triggers(tokens=TOKENS, seen_runs={"hbm": "run_a", "AI agents": "run_b"}, closes=drop, seen_closes={}, last_check=NOW - timedelta(hours=1),
                         now=NOW, cfg=CFG, held=set())
    assert [(x.kind, x.ticker) for x in t2] == [("price_drop", "MRVL")] and "(allowed)" in t2[0].detail
    t3 = detect_triggers(tokens=TOKENS, seen_runs={"hbm": "run_a", "AI agents": "run_b"}, closes=drop, seen_closes={"MRVL": "2026-11-09"},
                         last_check=NOW - timedelta(hours=1), now=NOW, cfg=CFG, held=set())
    assert t3 == []                                                                              # the same close does not wake it twice
    t4 = detect_triggers(tokens=TOKENS, seen_runs={"hbm": "run_a", "AI agents": "run_b"}, closes={}, seen_closes={}, last_check=NOW - timedelta(hours=25),
                         now=NOW, cfg=CFG, held=set())
    assert [x.kind for x in t4] == ["review"]


class FakeRouter:
    def __init__(self, d):
        self.d = d
        self.seen = None

    def complete(self, agent, messages, response_model=None):
        self.seen = messages[1]["content"]
        assert agent == "trader" and response_model is StrategyDecision
        return NS(parsed=StrategyDecision(**self.d), llm_alias="claude_opus_5_5")

    def usage_summary(self):
        return [{"agent": "trader", "cost_usd": 0.02}]


def cands():
    return [Candidate(ticker="MRVL", symbol="MRVLon", asset_id="a", topic="hbm", verdict_band="strong", score=72, confidence_pct=46.8, quotable=True, quote_cost_pct=0.6),
            Candidate(ticker="GOOGL", symbol="GOOGLon", asset_id="b", topic="AI agents", verdict_band="strong", score=73.3, confidence_pct=38.7, quotable=True, quote_cost_pct=0.8),
            Candidate(ticker="INTC", symbol="INTCon", asset_id="c", topic="chiplet", verdict_band="early", score=50, confidence_pct=50, quotable=True, quote_cost_pct=0.7)]


def run(d, *, fixed=None, budget=10000.0, holdings=None, adds=None, triggers=None):
    r = FakeRouter(d)
    out = assess(r, triggers=triggers or [NS(kind="review", ticker="", topic="", detail="routine review")], candidates=cands(), holdings=holdings or [],
                 context={"hbm": {"verdict": "strong"}}, budget_usd=budget, fixed_usd=fixed, cfg=CFG, adds_so_far=adds or {})
    return out, r


def test_rules_are_enforced_by_code_not_trusted_to_the_model():
    buy = {"action": "buy", "ticker": "mrvl", "usd": 4000, "what_changed": "w", "rationale": "r", "confidence": "high"}
    d, c, model, cost, notes = run(buy)[0]
    assert d.action == "buy" and c.ticker == "MRVL" and d.usd == 2500.0 and d.confidence == "medium" and cost == 0.02      # 25% share cap, confidence capped
    d, c, *_ , notes = run({**buy, "ticker": "GOOGL"})[0]
    assert d.action == "hold" and c is None and any("below 45%" in n for n in notes)                                                     # low-confidence report: no new buy
    d, c, *_, notes = run({**buy, "ticker": "INTC"})[0]
    assert d.action == "hold" and any("not strong or building" in n for n in notes)
    d, c, *_, notes = run({**buy, "ticker": "NVDA"})[0]
    assert d.action == "hold" and any("not a quotable candidate" in n for n in notes)
    d, c, *_, notes = run(buy, adds={"MRVL": 2}, triggers=[NS(kind="price_drop", ticker="MRVL", topic="", detail="-8%")])[0]
    assert d.action == "hold" and any("already added 2" in n for n in notes)                                                            # dip-buying is capped
    d, c, *_, notes = run({**buy, "usd": 7}, fixed=25.0)[0]
    assert d.action == "buy" and d.usd == 25.0 and any("fixed $25.00" in n for n in notes)                                              # live: size fixed by the caps
    (d, c, *_), r = run({"action": "hold", "what_changed": "the fall is not explained by the evidence", "rationale": "hold"})
    assert d.action == "hold" and "WHY YOU WOKE UP" in r.seen and "LATEST EVIDENCE PER TOPIC" in r.seen


def test_auto_approve_is_off_by_default_and_in_the_config():
    import yaml
    from pathlib import Path
    from app.fund.live import LiveConfig
    assert LiveConfig().auto_approve is False
    cfg = yaml.safe_load(Path(__file__).resolve().parents[1].joinpath("config", "funds.yaml").read_text(encoding="utf-8"))
    assert cfg["live"]["auto_approve"] is False            # the owner's switch; Claude never flips it

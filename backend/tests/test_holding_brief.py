"""Daily holding brief (owner 2026-11-12, "$0.50 a day"): X signals + a risk note per holding, owed until paid."""
import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app import report_queue
from app.fund import holding_brief as hb

NOW = datetime(2026, 11, 12, 9, 0, tzinfo=timezone.utc)
HOLDING = {"ticker": "INTC", "symbol": "INTCon", "topic": "high bandwidth memory", "quantity": 0.73919, "cost_usd": 43.83}
WATCH = {"price": 61.0, "cost_per_share": 59.2948, "gain_pct": 2.88}


class XAgent:
    def __init__(self, fail=False):
        self.fail, self.calls = fail, []

    def run(self, topic, keywords=None):
        self.calls.append((topic, keywords))
        if self.fail:
            raise RuntimeError("X is down")
        src = SimpleNamespace(id="x1", url="https://x.com/eetimes/status/1", authors=["eetimes"], published_at="2026-11-11")
        f = SimpleNamespace(claim="Intel says its packaging line is sold out through 2027.", label=SimpleNamespace(value="unverified_claim"), source_ids=["x1"])
        return SimpleNamespace(sources=[src], findings=[f], x_usage={"posts_read": 8, "cost_usd": 0.04}, errors=[], limitations=[])


class Router:
    def __init__(self, note=None, fail=False):
        self.note, self.fail, self.usage, self.calls = note, fail, [], []

    def complete(self, agent, messages, response_model=None):
        self.calls.append((agent, messages))
        if self.fail:
            raise RuntimeError("model down")
        self.usage.append(SimpleNamespace(cost_usd=0.0012))
        return SimpleNamespace(parsed=self.note)


def brief(router, x):
    return hb.make_brief(router=router, x_agent=x, holding=HOLDING, watch=WATCH, risks=["Thermal limits at 16 layers."], company="Intel Corp",
                         now=NOW, price_usd=0.5, near_usd=3.6)


def test_a_brief_uses_the_x_agent_and_the_risk_agent_and_is_priced_at_fifty_cents():
    note = hb.BriefNote(summary="INTC trades at $61.00, 2.9% above cost.  Posts say packaging is sold out.", what_changed="nothing new in the posts",
                        risks=["a", "b", "c", "d"], urgency="low")
    r, x = Router(note), XAgent()
    b = brief(r, x)
    assert x.calls == [("high bandwidth memory", ["Intel Corp", "INTC"])]
    assert r.calls[0][0] == "risk_brief"                                           # the Risk agent in brief mode, on the small model
    sent = json.loads(r.calls[0][1][1]["content"])
    assert sent["price_now"] == 61.0 and sent["gain_pct_since_bought"] == 2.88 and sent["risks_named_in_its_latest_report"] == ["Thermal limits at 16 layers."]
    assert sent["recent_posts"][0]["label"] == "unverified_claim"                  # a post is never a verified fact
    assert b.status == "owed" and b.price_usd == 0.5 and b.price_near == 0.1389    # $0.50 at $3.60 a NEAR
    assert b.cost_usd == 0.0412 and b.posts_read == 8                              # X reads + the model call
    assert b.signals[0].url == "https://x.com/eetimes/status/1" and b.signals[0].account == "eetimes"
    assert b.note.summary == "INTC trades at $61.00, 2.9% above cost. Posts say packaging is sold out." and len(b.note.risks) == 3


def test_a_brief_survives_a_dead_source_or_model_and_says_so():
    b = brief(Router(fail=True), XAgent(fail=True))
    assert b.note is None and b.signals == [] and b.status == "owed"
    assert any("X signals agent failed" in e for e in b.errors) and any("Risk agent (brief) failed" in e for e in b.errors)


def test_due_once_a_day_owed_list_and_what_the_trading_agent_reads(tmp_path):
    st = hb.BriefState()
    assert hb.due(st, "INTC", NOW, 24)
    b = brief(Router(hb.BriefNote(summary="s", what_changed="an export ban is reported", risks=["r"], urgency="high")), XAgent())
    st.briefs.append(b)
    assert not hb.due(st, "INTC", NOW + timedelta(hours=23), 24) and hb.due(st, "INTC", NOW + timedelta(hours=24), 24)
    assert [x.id for x in st.owed()] == [b.id]
    hb.save_state(st, tmp_path / "briefs" / "state.json")
    again = hb.load_state(tmp_path / "briefs" / "state.json")
    assert again.last_for("INTC").note.urgency == "high" and again.last_for("NVDA") is None
    seen = hb.for_agent(again, ["INTC", "NVDA"], NOW + timedelta(hours=5))
    assert len(seen) == 1 and seen[0]["urgency"] == "high" and seen[0]["price_then"] == 61.0 and "not verified facts" in seen[0]["note"]
    assert hb.for_agent(again, ["INTC"], NOW + timedelta(hours=72)) == []            # an old brief is not shown as news
    b.status = "paid"
    assert st.owed() == []


def test_a_brief_payment_is_income_but_does_not_pay_for_a_new_report(tmp_path):
    f = tmp_path / "economy.json"
    f.write_text(json.dumps({"purchases": [{"run_id": "r1", "status": "paid"}, {"run_id": "briefs_20261112T090000", "status": "paid"},
                                           {"run_id": "r2", "status": "failed"}]}), encoding="utf-8")
    assert report_queue.sales_count(f) == 1


def test_shipped_settings_match_the_owners_decision():
    from app.fund import load_fund_config
    from app.models.config import load_model_config
    ec = load_fund_config().economy
    assert ec.brief_usd == 0.5 and ec.brief_hours == 24 and ec.brief_max_posts <= 10 and ec.brief_max_owed == 3
    mc = load_model_config()
    assert "risk_brief" in str(mc.agents if hasattr(mc, "agents") else mc)


def test_a_brief_reads_few_accounts_so_it_needs_one_search():
    acc = lambda h, g, n="": SimpleNamespace(handle=h, group=g, name=n)  # noqa: E731
    wl = [acc("eetimes", "press"), acc("intel", "company", "Intel"), acc("nvidia", "company", "NVIDIA"), acc("someone", "owner-added"),
          acc("SemiAnalysis_", "analyst"), acc("IntelFoundry", "owner-added", "Intel Foundry")] + [acc(f"p{i}", "press") for i in range(20)]
    got = [a.handle for a in hb.brief_accounts(wl, "Intel Corp")]
    assert got[:2] == ["intel", "IntelFoundry"] and "nvidia" not in got and "someone" not in got      # its own accounts first, then press and analysts
    assert "eetimes" in got and "SemiAnalysis_" in got and len(got) == 14
    assert [a.handle for a in hb.brief_accounts(wl, "")][:1] == ["eetimes"]


def test_the_owner_can_ask_for_a_brief_now():
    """`fund_trade.py brief` writes a brief on every holding regardless of the daily schedule (the owner runs it)."""
    from pathlib import Path
    src = (Path(__file__).resolve().parents[1] / "scripts" / "fund_trade.py").read_text(encoding="utf-8")
    assert 'due = list(held) if force else [h for h in held if hb.due(bst, h["ticker"], now, ec.brief_hours)]' in src
    assert 'rc = cmd_briefs(s, cfg, execute=True, force=True)' in src and '"balance", "brief"]' in src

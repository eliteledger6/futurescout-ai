"""Reports the agent writes by itself: the radar's top topics stay fresh, and every report sold funds one more.
Agent Market fees join the 70% staked / 30% kept split."""
import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app import market_income, report_queue as rq
from app.agent_market import MarketConfig
from app.fund.economy import EconomyConfig, EconomyState, Purchase, YOCTO, stake_amount_yocto

NOW = datetime(2026, 11, 12, 9, 0, tzinfo=timezone.utc)
CFG = MarketConfig(auto_top_n=5, auto_fresh_days=7, auto_runs_per_day=2)
NAMES = ["AI agents", "retrieval-augmented generation", "mixture of experts", "supervised fine-tuning",
         "post-quantum cryptography", "quantum error correction", "high bandwidth memory"]


def radar(names=NAMES, unranked=("glass core substrate",)):
    rows = [SimpleNamespace(topic=n, rank=i + 1) for i, n in enumerate(names)]
    return SimpleNamespace(topics=rows + [SimpleNamespace(topic=n, rank=None) for n in unranked])


def report(topic, days_ago, score=70.0):
    return {"id": topic, "topic": topic, "score": score, "generated_at": (NOW - timedelta(days=days_ago)).isoformat()}


def pick(rows, state=None, sales=0, cfg=CFG, **kw):
    state = state or rq.QueueState(sales_used=0)
    return rq.next_report(radar=radar(), rows=rows, state=state, sales=sales, cfg=cfg, now=NOW, **kw), state


def test_top_five_topics_always_get_a_fresh_report_in_rank_order():
    rows = [report("AI agents", 2), report("retrieval-augmented generation", 9), report("mixture of experts", 1)]
    assert pick(rows)[0] == ("retrieval-augmented generation", "top 5")           # its report is 9 days old
    rows[1] = report("retrieval-augmented generation", 0)
    assert pick(rows)[0] == ("supervised fine-tuning", "top 5")                   # next top-5 topic without one
    fresh = [report(n, 1) for n in NAMES[:5]]
    assert pick(fresh)[0] is None                                                 # top 5 covered and nothing sold: nothing to write


def test_a_sale_funds_the_next_topic_below_the_top_five_once(tmp_path):
    fresh = [report(n, 1) for n in NAMES[:5]]
    got, state = pick(fresh, sales=1)
    assert got == ("quantum error correction", "sale")
    rq.record(state, tmp_path / "q.json", topic=got[0], reason=got[1], run_id="r1", note="report written", now=NOW)
    assert state.sales_used == 1
    fresh.insert(0, report("quantum error correction", 0))
    assert pick(fresh, state=state, sales=1)[0] is None                           # that sale is used up
    assert pick(fresh, state=state, sales=2)[0] == ("high bandwidth memory", "sale")
    assert rq.load_state(tmp_path / "q.json").runs[0].topic == "quantum error correction"


def test_daily_cap_earlier_sales_failures_and_the_off_switch(tmp_path):
    state = rq.QueueState(sales_used=0, runs=[rq.AutoRun(at=NOW, topic="a", reason="top 5", run_id="1"),
                                               rq.AutoRun(at=NOW - timedelta(hours=1), topic="b", reason="sale", run_id="2")])
    assert pick([], state=state, sales=9)[0] is None                              # two written today already
    first = rq.QueueState()                                                       # first start: sales made before do not fund reports
    assert pick([report(n, 1) for n in NAMES[:5]], state=first, sales=6)[0] is None and first.sales_used == 6
    failed = rq.QueueState(sales_used=0)
    rq.record(failed, tmp_path / "q.json", topic="AI agents", reason="top 5", run_id=None, note="model down", now=NOW - timedelta(hours=2))
    assert rq.failed_topics(failed, NOW) == ("AI agents",)
    assert pick([], state=failed, failed_recently=rq.failed_topics(failed, NOW))[0] == ("retrieval-augmented generation", "top 5")
    assert failed.sales_used == 0                                                 # a failed run does not use up a sale
    assert pick([], cfg=MarketConfig(auto_runs_per_day=0))[0] is None             # switched off
    assert rq.next_report(radar=None, rows=[], state=rq.QueueState(sales_used=0), sales=3, cfg=CFG, now=NOW) is None   # no radar yet


def test_sales_are_counted_from_the_fullest_economy_record(tmp_path):
    mine, snap = tmp_path / "mine.json", tmp_path / "snap.json"
    mine.write_text(json.dumps({"purchases": [{"status": "paid"}]}), encoding="utf-8")
    snap.write_text(json.dumps({"purchases": [{"status": "paid"}, {"status": "failed"}, {"status": "paid"}]}), encoding="utf-8")
    assert rq.sales_count(mine, snap, tmp_path / "missing.json") == 2


def hire(aid, status="accepted", amount="3", token="USD"):
    return {"assignment": {"assignmentId": aid, "status": status, "escrowAmount": amount, "escrowToken": token,
                           "finalizedAt": "2026-11-12T08:00:00Z"}, "job": {}}


def test_agent_market_fees_are_recorded_once_and_test_hires_are_not_income(tmp_path):
    path, asked = tmp_path / "agent_market" / "income.json", []

    def price():
        asked.append(1)
        return 2.5

    rows = [hire("paid-1"), hire("test-1", amount="0"), hire("open-1", status="in_progress"), hire("odd-1", token="NEAR")]
    assert market_income.collect(rows, path, price, NOW, log=lambda m: None) == 1
    inc = market_income.load(path)
    assert [(f.assignment_id, f.usd, f.near) for f in inc.fees] == [("paid-1", 3.0, 1.2)] and inc.usd() == 3.0
    assert market_income.collect(rows + [hire("paid-2")], path, price, NOW, log=lambda m: None) == 1      # paid-1 is not counted twice
    assert market_income.load(path).near() == 2.4
    n = len(asked)
    assert market_income.collect(rows, path, price, NOW, log=lambda m: None) == 0 and len(asked) == n      # nothing new: no price request
    assert market_income.best(tmp_path / "none.json", path).usd() == 6.0


def test_agent_market_fees_join_the_seventy_thirty_split():
    cfg = EconomyConfig(staking_contract="stake.dao", stake_share=0.7, min_stake_near=1.0, stake_reserve_near=0.3)
    state = EconomyState(purchases=[Purchase(id="p", run_id="r", topic="t", price_near=1.0, buyer="b", seller="s", status="paid", at=NOW)])
    wallet = int(5 * YOCTO)
    assert stake_amount_yocto(wallet, cfg, state) is None                                    # 0.7 NEAR owed: under the 1 NEAR minimum
    got = stake_amount_yocto(wallet, cfg, state, extra_received_near=1.2)                    # plus a $3 hire = 1.2 NEAR received
    assert got is not None and abs(got / YOCTO - 1.54) < 1e-6                                # 70% of 2.2 NEAR
    assert stake_amount_yocto(int(0.8 * YOCTO), cfg, state, extra_received_near=1.2) is None  # the fee is not in the wallet yet

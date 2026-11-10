"""Agent economy: report pricing, the trading agent's report budget, exactly-once payment checked on chain, 80/20 staking."""

from datetime import datetime, timezone

import pytest

from app.fund.economy import (YOCTO, EconomyConfig, EconomyState, buy_report, near_to_yocto, parse_transfer, price_report,
                              purchase_blocks, report_budget_near, stake, stake_amount_yocto)

NOW = datetime(2026, 11, 10, 12, tzinfo=timezone.utc)
CFG = EconomyConfig(enabled=True, seller_account="report-agent.near", staking_contract="pool.poolv1.near")
BUYER = "trader.near"


def price(**kw):
    args = dict(run_id="run1", topic="hbm", cost_usd=0.40, score=80.0, confidence_pct=50.0, near_usd=3.6, cfg=CFG, now=NOW)
    args.update(kw)
    return price_report(**args)


def test_price_follows_cost_and_quality_within_the_owners_limits():
    p = price()
    assert p.price_near == pytest.approx(0.267, abs=0.001) and "x3 markup" in p.basis              # 0.40 x 3 x 0.8 = $0.96
    assert price(score=20, confidence_pct=10).price_usd >= 0.40                                     # never below what it cost
    assert price(cost_usd=50.0).price_near == CFG.max_price_near                                     # owner: at most 2 NEAR
    assert price(cost_usd=0.0001).price_near == CFG.min_price_near


def test_budget_is_10pct_of_the_fund_minus_reports_already_bought():
    st = EconomyState()
    assert report_budget_near(fund_value_usd=60.0, near_usd=3.0, state=st, cfg=CFG) == pytest.approx(2.0)
    st.purchases.append(buy_like(price_near=0.5, status="paid"))
    assert report_budget_near(fund_value_usd=60.0, near_usd=3.0, state=st, cfg=CFG) == pytest.approx(1.5)


def buy_like(price_near=0.3, status="paid", run_id="old"):
    from app.fund.economy import Purchase
    return Purchase(id="x", run_id=run_id, topic="t", price_near=price_near, buyer=BUYER, seller=CFG.seller_account, status=status, at=NOW)


def test_every_guard_blocks_a_purchase():
    p = price()
    ok = dict(state=EconomyState(), price=p, budget_near=1.0, wallet_near=1.0, cfg=CFG, trading_enabled=True, kill_switch=False)
    assert purchase_blocks(**ok) == []
    cases = [
        (dict(cfg=EconomyConfig(seller_account="r.near")), "switched off"),                # owner switch, off by default
        (dict(trading_enabled=False), "trading_enabled"),
        (dict(kill_switch=True), "kill switch"),
        (dict(budget_near=0.1), "report budget left"),
        (dict(wallet_near=0.3), "fee reserve"),
        (dict(state=EconomyState(purchases=[buy_like(run_id="run1", status="sending")])), "already bought"),
    ]
    for kw, match in cases:
        assert any(match in b for b in purchase_blocks(**{**ok, **kw})), match
    assert EconomyConfig().enabled is False and EconomyConfig().max_price_near == 2.0


def tx(signer=BUYER, receiver="report-agent.near", deposit=None, status=None):
    return {"result": {"status": status or {"SuccessValue": ""}, "transaction": {"hash": "H1", "signer_id": signer, "receiver_id": receiver,
            "actions": [{"Transfer": {"deposit": str(deposit if deposit is not None else near_to_yocto(0.267))}}]}}}


def test_payment_is_sent_once_and_confirmed_on_chain(tmp_path):
    st, sent = EconomyState(), []
    p = buy_report(state=st, path=tmp_path / "e.json", price=price(), buyer=BUYER, cfg=CFG,
                   send=lambda to, y: sent.append((to, y)) or "H1", read=lambda h, who: tx(), now=NOW)
    assert p.status == "paid" and sent == [("report-agent.near", near_to_yocto(0.267))] and st.bought("run1")
    assert (tmp_path / "e.json").is_file()
    for bad, match in ((tx(receiver="evil.near"), "not the report agent"), (tx(signer="x.near"), "not by the buyer"),
                       (tx(deposit=1), "too small"), (tx(status={"Failure": {}}), "did not succeed")):
        with pytest.raises(RuntimeError, match=match):
            parse_transfer(bad, tx_hash="H1", buyer=BUYER, seller="report-agent.near", min_yocto=near_to_yocto(0.267))


def test_an_unclear_send_is_recorded_and_never_retried(tmp_path):
    st = EconomyState()

    def boom(to, y):
        raise RuntimeError("connection reset")
    p = buy_report(state=st, path=tmp_path / "e.json", price=price(), buyer=BUYER, cfg=CFG, send=boom, read=lambda h, w: tx(), now=NOW)
    assert p.status == "sending" and "check the account" in p.note
    assert st.bought("run1") is not None                                   # counts as bought: no second payment
    assert any("already bought" in b for b in purchase_blocks(state=st, price=price(), budget_near=5, wallet_near=5, cfg=CFG,
                                                              trading_enabled=True, kill_switch=False))


def test_report_agent_stakes_80pct_and_keeps_20pct(tmp_path):
    bal = 5 * YOCTO
    assert stake_amount_yocto(bal, CFG) == 4 * YOCTO
    assert stake_amount_yocto(YOCTO, CFG) is None                          # 0.8 NEAR is under the 1 NEAR minimum
    assert stake_amount_yocto(bal, EconomyConfig(stake_share=0.8)) is None # no staking contract: off
    calls = []
    ev = stake(state=EconomyState(), path=tmp_path / "e.json", account="report-agent.near", balance_yocto=bal, cfg=CFG,
               call=lambda c, m, a, g, d: calls.append((c, m, d)) or "T1", now=NOW)
    assert ev.status == "staked" and calls == [("pool.poolv1.near", "deposit_and_stake", 4 * YOCTO)] and ev.amount_near == 4.0

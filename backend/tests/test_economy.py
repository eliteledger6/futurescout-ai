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
    assert p.price_near == pytest.approx(4.6) and "3-5 NEAR band" in p.basis                         # quality 0.8 -> 3 + 2 x 0.8
    assert price(score=0, confidence_pct=0).price_near == CFG.min_price_near == 3.0                  # owner: 3 to 5 NEAR
    assert price(score=100, confidence_pct=100).price_near == CFG.max_price_near == 5.0
    assert price(score=0, confidence_pct=0, cost_usd=14.4).price_near == pytest.approx(5.0)         # never below cost x 3 (capped)


def test_dollar_price_follows_what_the_report_cost_to_make():
    cfg = EconomyConfig(enabled=True, seller_account="r.near", min_price_usd=2.0, max_price_usd=3.0, margin_usd=1.5)
    cheap = price(cost_usd=0.10, cfg=cfg)                                   # 0.10 + seal 0.05 + 1.50 = 1.65 -> $2 minimum
    assert cheap.price_usd == pytest.approx(2.0, abs=0.01) and cheap.price_near == pytest.approx(0.556, abs=0.001)
    mid = price(cost_usd=0.45, cfg=cfg, patent_searches=8)                  # 0.45 + 0.20 + 0.05 + 1.50 = 2.20
    assert mid.price_usd == pytest.approx(2.2, abs=0.01) and "8 patent searches" in mid.basis
    dear = price(cost_usd=1.40, cfg=cfg, patent_searches=6)                # 3.10 -> $3 maximum
    assert dear.price_usd == pytest.approx(3.0, abs=0.01)
    assert price(cost_usd=0.45, cfg=cfg, near_usd=1.8).price_near == pytest.approx(1.111, abs=0.001)   # NEAR halves: twice the NEAR


def test_shipped_config_prices_reports_at_2_to_3_dollars():
    from app.fund import load_fund_config
    ec = load_fund_config().economy
    assert (ec.min_price_usd, ec.max_price_usd) == (2.0, 3.0) and ec.max_price_near >= 3.0 / 3.0


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
    ok = dict(state=EconomyState(), price=p, budget_near=10.0, wallet_near=10.0, cfg=CFG, trading_enabled=True, kill_switch=False)
    assert purchase_blocks(**ok) == []
    cases = [
        (dict(cfg=EconomyConfig(seller_account="r.near")), "switched off"),                # owner switch, off by default
        (dict(trading_enabled=False), "trading_enabled"),
        (dict(kill_switch=True), "kill switch"),
        (dict(budget_near=0.1), "report budget left"),
        (dict(wallet_near=4.6), "fee reserve"),
        (dict(state=EconomyState(purchases=[buy_like(run_id="run1", status="sending")])), "already bought"),
    ]
    for kw, match in cases:
        assert any(match in b for b in purchase_blocks(**{**ok, **kw})), match
    assert EconomyConfig().enabled is False and EconomyConfig().max_price_near == 5.0


def tx(signer=BUYER, receiver="report-agent.near", deposit=None, status=None):
    return {"result": {"status": status or {"SuccessValue": ""}, "transaction": {"hash": "H1", "signer_id": signer, "receiver_id": receiver,
            "actions": [{"Transfer": {"deposit": str(deposit if deposit is not None else near_to_yocto(4.6))}}]}}}


def test_payment_is_sent_once_and_confirmed_on_chain(tmp_path):
    st, sent = EconomyState(), []
    p = buy_report(state=st, path=tmp_path / "e.json", price=price(), buyer=BUYER, cfg=CFG,
                   send=lambda to, y: sent.append((to, y)) or "H1", read=lambda h, who: tx(), now=NOW)
    assert p.status == "paid" and sent == [("report-agent.near", near_to_yocto(4.6))] and st.bought("run1")
    assert (tmp_path / "e.json").is_file()
    for bad, match in ((tx(receiver="evil.near"), "not the report agent"), (tx(signer="x.near"), "not by the buyer"),
                       (tx(deposit=1), "too small"), (tx(status={"Failure": {}}), "did not succeed")):
        with pytest.raises(RuntimeError, match=match):
            parse_transfer(bad, tx_hash="H1", buyer=BUYER, seller="report-agent.near", min_yocto=near_to_yocto(4.6))


def test_an_unclear_send_is_recorded_and_never_retried(tmp_path):
    st = EconomyState()

    def boom(to, y):
        raise RuntimeError("connection reset")
    p = buy_report(state=st, path=tmp_path / "e.json", price=price(), buyer=BUYER, cfg=CFG, send=boom, read=lambda h, w: tx(), now=NOW)
    assert p.status == "sending" and "check the account" in p.note
    assert st.bought("run1") is not None                                   # counts as bought: no second payment
    assert any("already bought" in b for b in purchase_blocks(state=st, price=price(), budget_near=5, wallet_near=5, cfg=CFG,
                                                              trading_enabled=True, kill_switch=False))


def paid(st, near, rid="r"):
    from app.fund.economy import Purchase
    st.purchases.append(Purchase(id=rid, run_id=rid, topic="t", price_near=near, buyer=BUYER, seller="report-agent.near",
                                 status="paid", at=NOW))
    return st


def test_report_agent_stakes_70pct_of_each_payment_never_the_rest_of_its_wallet(tmp_path):
    st = paid(EconomyState(), 10.0)
    assert stake_amount_yocto(100 * YOCTO, CFG, st) == 7 * YOCTO             # 70% of the 10 NEAR paid, not of the 100 in the wallet
    assert stake_amount_yocto(100 * YOCTO, CFG, EconomyState()) is None      # no payment yet: the owner's own NEAR is never staked
    assert stake_amount_yocto(100 * YOCTO, EconomyConfig(stake_share=0.7), st) is None   # no staking contract: off
    small = EconomyConfig(staking_contract="pool.poolv1.near", min_stake_near=0.25, stake_reserve_near=0.3)
    one = paid(EconomyState(), 0.6)                                          # one $2 report
    assert stake_amount_yocto(5 * YOCTO, small, one) == 42 * YOCTO // 100   # 0.42 NEAR staked
    assert stake_amount_yocto(YOCTO // 2, small, one) is None                # 0.5 NEAR wallet - 0.3 reserve = 0.2: under the minimum
    calls = []
    ev = stake(state=st, path=tmp_path / "e.json", account="report-agent.near", balance_yocto=100 * YOCTO, cfg=CFG,
               call=lambda c, m, a, g, d: calls.append((c, m, d)) or "T1", now=NOW)
    assert ev.status == "staked" and calls == [("pool.poolv1.near", "deposit_and_stake", 7 * YOCTO)] and st.kept_near == 3.0
    assert stake_amount_yocto(100 * YOCTO, CFG, st) is None                  # already staked: nothing twice
    paid(st, 10.0, "r2")                                                     # the next payment: 70% of it, the pot grows to 6
    stake(state=st, path=tmp_path / "e.json", account="report-agent.near", balance_yocto=100 * YOCTO, cfg=CFG,
          call=lambda c, m, a, g, d: calls.append((c, m, d)) or "T2", now=NOW)
    assert calls[-1][2] == 7 * YOCTO and st.kept_near == 6.0


def test_stake_uses_near_ai_product_args_and_reads_the_farm_position(tmp_path):
    import base64
    import json as _json
    from app.fund.economy import staked_amount
    cfg = EconomyConfig(enabled=True, seller_account="r.near", staking_contract="stake.dao", stake_method="stake", stake_gas_tgas=300,
                        stake_args={"product_id": "prod_X", "price_id": "price_Y"})
    calls = []
    stake(state=paid(EconomyState(), 2.0), path=tmp_path / "e.json", account="r.near", balance_yocto=5 * YOCTO, cfg=cfg,
          call=lambda c, m, a, g, d: calls.append((c, m, a, g, d)) or "T", now=NOW)
    assert calls == [("stake.dao", "stake", {"product_id": "prod_X", "price_id": "price_Y"}, 300 * 10 ** 12, 14 * YOCTO // 10)]

    class Http:
        def post(self, url, json, timeout):  # noqa: A002
            args = _json.loads(base64.b64decode(json["params"]["args_base64"]))
            assert json["params"]["method_name"] == "get_farm_position" and args == {"account_id": "r.near", "product_id": "prod_X"}
            body = _json.dumps({"staked_near_amount": str(5 * YOCTO), "status": "Active"}).encode()
            return type("R", (), {"json": lambda self: {"result": {"result": list(body)}}})()
    assert staked_amount(Http(), cfg, "r.near") == 5 * YOCTO


# ---------------------------------------------------------------- paying from the near.com (private) balance
def test_payment_from_the_private_balance_is_checked_signed_once_and_seen_arriving(tmp_path):
    import base64 as b64
    import json as _json
    from app.fund.economy_pay import WNEAR, pay_from_private
    from app.fund.intents_signed import versioned_nonce
    units = near_to_yocto(4.6)
    DEP = "dep" + "1" * 61

    def order(receiver=DEP, amount=units, asset="imt:" + "7" * 64 + ":" + WNEAR):
        msg = {"deadline": "2026-11-13T09:00:00.000Z", "signer_id": BUYER,
               "intents": [{"intent": "transfer", "receiver_id": receiver, "tokens": {asset: str(amount)}}]}
        nonce = b64.b64encode(versioned_nonce("252812b3", datetime(2026, 11, 13, 9, tzinfo=timezone.utc), rand=bytes(15))).decode()
        return {"standard": "nep413", "payload": {"message": _json.dumps(msg), "nonce": nonce, "recipient": "intents.far"}}

    class Api:
        def __init__(self, have=10 * YOCTO, out=None, o=None):
            self.have, self.out, self.o, self.quotes = have, out, o, []
        def login(self, a, k, salt): return {"accessToken": "tok"}
        def balances(self, tok): return [{"tokenId": "imt:" + "7" * 64 + ":" + WNEAR, "available": str(self.have)}]
        def quote(self, **kw):
            self.quotes.append(kw)
            return {"amountIn": str(units), "minAmountOut": str(self.out if self.out is not None else units * 99 // 100),
                    "amountOutFormatted": "4.6", "depositAddress": DEP}
        def unsigned_order(self, dep, acc): return self.o or order()

    def run(api, arrive=True):
        total, sent = {"v": YOCTO}, []
        def submit(o, k):
            sent.append(o)
            if arrive:
                total["v"] += units
            return "INTENT1"
        st = EconomyState()
        p = pay_from_private(state=st, path=tmp_path / "e.json", price=price(), account=BUYER, private_key="ed25519:" + "1" * 40, cfg=CFG,
                             api=api, salt_reader=lambda: "252812b3", submit=submit, allowed_recipients=["intents.near", "intents.far"],
                             read_seller_total=lambda: total["v"], now=lambda: NOW, sleep=lambda s: None, poll_seconds=0)
        return p, sent, st

    api = Api()
    p, sent, st = run(api)
    assert p.status == "paid" and len(sent) == 1 and "near.com balance" in p.note and st.bought("run1")
    assert api.quotes[0]["recipient"] == "report-agent.near" and api.quotes[0]["recipient_type"] == "DESTINATION_CHAIN"
    p, sent, _ = run(Api(), arrive=False)
    assert p.status == "sending" and "nothing arrived" in p.note and len(sent) == 1      # never re-sent
    for api, match in ((Api(have=YOCTO), "holds 1.000 NEAR"), (Api(out=units // 2), "less than 98%"),
                       (Api(o=order(receiver="evil.near")), "deposit address"), (Api(o=order(amount=units * 2)), "not exactly")):
        with pytest.raises(RuntimeError, match=match):
            run(api)

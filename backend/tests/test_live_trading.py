"""Stage 3 live-trading module: every limit and the single-send guarantee, with a fake chain and a fake 1Click."""

import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace as NS

import httpx
import pytest

from app.agents.trader import agent as trader
from app.fund.live import (Executor, LiveConfig, OneClickLive, Proposal, TradingState, check_limits, check_quote, load_state,
                           read_balances, save_state)

NOW = datetime(2026, 11, 10, 9, tzinfo=timezone.utc)
ACCOUNT = "fund-test.near"


def proposal(usd=5.0, mode="live", status="proposed", close=50.0) -> Proposal:
    p = Proposal(id="abc1234567", created_at=NOW, mode=mode, topic="chiplet", ticker="INTC", symbol="INTCon",
                 asset_id="nep141:bnb-0xintc.omdep.near", usd=usd, ref_close=close, ref_close_date="2026-11-09")
    p.status = status
    return p


def quote_payload(usd=5.0, out_tokens="0.0995", out_usd=None, deposit="depo1234"):
    return {"quote": {"amountIn": str(int(usd * 1e6)), "amountInFormatted": str(usd), "amountInUsd": str(usd),
                      "amountOut": "1", "amountOutFormatted": out_tokens, "amountOutUsd": str(out_usd if out_usd is not None else usd * 0.992),
                      "minAmountOut": "1", "timeEstimate": 10, "depositAddress": deposit, "deadline": "2026-11-10T10:00:00Z"},
            "correlationId": "c-1"}


class FakeChain:
    """Fake NEAR RPC (views) + fake signer (calls)."""

    def __init__(self, usdc_units=5_000_000, registered=True, fail_transfer=False, near_yocto=5 * 10 ** 23):
        self.usdc_units, self.registered, self.fail_transfer, self.near_yocto = usdc_units, registered, fail_transfer, near_yocto
        self.calls = []
        self.account_id = ACCOUNT

    def rpc(self, req: httpx.Request) -> httpx.Response:
        body = json.loads(req.read())
        method = body["params"].get("method_name")
        if body["params"]["request_type"] == "view_account":
            return httpx.Response(200, json={"result": {"amount": str(self.near_yocto)}})
        val = {"ft_balance_of": str(self.usdc_units), "storage_balance_of": {"total": "1"} if self.registered else None,
               "mt_batch_balance_of": ["100000000000000000"]}[method]
        return httpx.Response(200, json={"result": {"result": list(json.dumps(val).encode())}})

    def transfer(self, receiver, amount_yocto):
        self.calls.append(("transfer", {"receiver": receiver, "amount": amount_yocto}, amount_yocto))
        if self.fail_transfer:
            raise RuntimeError("network dropped")
        return "tx-transfer"

    def call(self, contract, method, args, gas, deposit):
        self.calls.append((method, args, deposit))
        if method == "ft_transfer" and self.fail_transfer:
            raise RuntimeError("network dropped")
        return f"tx-{method}"


def make(tmp_path, chain, *, cfg=None, quote=None, statuses=("PENDING_DEPOSIT", "PROCESSING", "SUCCESS"), kill=False):
    cfg = cfg or LiveConfig(trading_enabled=True, poll_seconds=0.0, pay_with="usdc")
    seen = {"quotes": [], "status": 0}

    def oneclick(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/v0/tokens":
            return httpx.Response(200, json=[{"assetId": "nep141:wrap.near", "price": 4.0}])
        if req.url.path == "/v0/quote":
            body = json.loads(req.read())
            seen["quotes"].append(body)
            reply = quote or quote_payload()
            if quote is None:
                reply["quote"]["amountIn"] = body["amount"]          # a real quote echoes the amount it was asked for
            return httpx.Response(201, json=reply)
        if req.url.path == "/v0/status":
            st = statuses[min(seen["status"], len(statuses) - 1)]
            seen["status"] += 1
            return httpx.Response(200, json={"status": st, "swapDetails": {"amountOutFormatted": "0.0995", "amountOutUsd": "4.96"}})
        return httpx.Response(200, json={})
    oc = OneClickLive("https://oc.test", http=httpx.Client(transport=httpx.MockTransport(oneclick)))
    state_path = tmp_path / "trading" / "state.json"
    ex = Executor(cfg, state_path, oc, pay_asset="nep141:wrap.near" if cfg.pay_with == "near" else "nep141:usdc", signer=chain, http=httpx.Client(transport=httpx.MockTransport(chain.rpc)),
                  now=lambda: NOW, sleep=lambda s: None)
    if kill:
        ex.kill_file.parent.mkdir(parents=True, exist_ok=True)
        ex.kill_file.write_text("stop")
    return ex, seen, state_path


def test_limits_block_everything_that_should_be_blocked():
    cfg = LiveConfig(trading_enabled=True)
    st = TradingState()
    assert check_limits(st, proposal(5), cfg, kill_switch=False, now=NOW) == []
    assert "kill switch" in check_limits(st, proposal(5), cfg, kill_switch=True, now=NOW)[0]
    assert "trading_enabled" in check_limits(st, proposal(5), LiveConfig(), kill_switch=False, now=NOW)[0]
    assert "per-trade cap" in " ".join(check_limits(st, proposal(5.01), cfg, kill_switch=False, now=NOW))
    assert "below the minimum" in check_limits(st, proposal(0.5), cfg, kill_switch=False, now=NOW)[0]
    done = proposal(3, status="success")
    done.mark("executing", now=NOW)
    done.status = "success"
    st.proposals.append(done)
    msgs = " ".join(check_limits(st, proposal(3), cfg, kill_switch=False, now=NOW))
    assert "daily cap" in msgs and "total cap" in msgs
    sell = proposal(1)
    sell.side = "sell"
    assert "sells_enabled is false" in " ".join(check_limits(TradingState(), sell, cfg, kill_switch=False, now=NOW))   # selling: owner switch, off by default


def test_quote_checks_price_band_cost_and_amount():
    cfg = LiveConfig()
    q = quote_payload()["quote"]
    assert check_quote(q, proposal(5, close=50.0), cfg, NOW) == []                 # 5 / 0.0995 = $50.25
    assert "away from the stock" in " ".join(check_quote(q, proposal(5, close=60.0), cfg, NOW))
    from app.fund.live import price_band
    assert price_band(cfg, "2026-11-09", NOW) == 3.0 and price_band(cfg, "2026-11-07", NOW) == 6.0     # Friday close on a Monday... 3 days
    assert price_band(cfg, "2026-10-01", NOW) == 8.0 and price_band(cfg, None, NOW) == 8.0
    stale = proposal(5, close=48.0)                                                # 4.7% away
    assert check_quote(q, stale, cfg, NOW) != []
    stale.ref_close_date = "2026-11-07"
    assert check_quote(q, stale, cfg, NOW) == []
    assert "cost" in " ".join(check_quote(quote_payload(out_usd=4.80)["quote"], proposal(5), cfg))
    assert "not the approved" in " ".join(check_quote(quote_payload(usd=9.0)["quote"], proposal(5), cfg))
    assert check_quote({}, proposal(5), cfg) == ["quote is missing amounts"]
    assert "no reference close" in " ".join(check_quote(q, proposal(5, close=None), cfg))


def test_happy_path_sends_once_and_records_everything(tmp_path):
    chain = FakeChain()
    ex, seen, path = make(tmp_path, chain)
    st, p = TradingState(), proposal(status="approved")
    st.proposals.append(p)
    ex.execute(st, p)
    assert p.status == "success" and p.deposit_tx == "tx-ft_transfer" and p.sha256
    assert [c[0] for c in chain.calls] == ["ft_transfer"]
    assert chain.calls[0][1] == {"receiver_id": "depo1234", "amount": "5000000"} and chain.calls[0][2] == 1
    body = seen["quotes"][0]
    assert body["dry"] is False and body["recipient"] == ACCOUNT and body["refundTo"] == ACCOUNT and body["recipientType"] == "INTENTS"
    assert [e.status for e in p.history][:2] == ["executing", "deposited"]
    assert load_state(path).get(p.id).status == "success"
    # a finished or already-sent proposal can never be sent again
    with pytest.raises(RuntimeError, match="never sent twice"):
        ex.execute(st, p)
    assert len(chain.calls) == 1


def test_unregistered_deposit_address_is_registered_first(tmp_path):
    chain = FakeChain(registered=False)
    ex, _, _ = make(tmp_path, chain)
    st, p = TradingState(), proposal(status="approved")
    ex.execute(st, p)
    assert [c[0] for c in chain.calls] == ["storage_deposit", "ft_transfer"]


def test_nothing_is_sent_when_a_check_fails(tmp_path):
    for kwargs, match in (({"kill": True}, "kill switch"), ({"cfg": LiveConfig(trading_enabled=False, pay_with="usdc")}, "trading_enabled"),
                          ({"quote": quote_payload(out_tokens="0.05")}, "away from the stock"),
                          ({"quote": quote_payload(deposit=None)}, "no deposit address")):
        chain = FakeChain()
        ex, _, _ = make(tmp_path / match.replace(" ", "_"), chain, **kwargs)     # own folder: the STOP file must not leak
        st, p = TradingState(), proposal(status="approved")
        with pytest.raises(RuntimeError, match=match):
            ex.execute(st, p)
        assert chain.calls == []
    chain = FakeChain(usdc_units=1_000_000)                              # not enough USDC
    ex, _, _ = make(tmp_path / "poor", chain)
    with pytest.raises(RuntimeError, match="less than"):
        ex.execute(TradingState(), proposal(status="approved"))
    assert chain.calls == []
    ex, _, _ = make(tmp_path / "rest", FakeChain())
    with pytest.raises(RuntimeError, match="not 'approved'"):            # owner approval is required
        ex.execute(TradingState(), proposal(status="proposed"))
    ex.signer = None
    with pytest.raises(RuntimeError, match="not set"):
        ex.execute(TradingState(), proposal(status="approved"))


def test_ambiguous_transfer_error_is_never_retried(tmp_path):
    chain = FakeChain(fail_transfer=True)
    ex, _, _ = make(tmp_path, chain)
    st, p = TradingState(), proposal(status="approved")
    st.proposals.append(p)
    with pytest.raises(RuntimeError, match="never approve again"):
        ex.execute(st, p)
    assert p.status == "deposited" and st.spent("live") == 5.0           # counts against the caps until resolved
    with pytest.raises(RuntimeError):
        ex.execute(st, p)
    assert [c[0] for c in chain.calls] == ["ft_transfer"]                # one attempt only


def test_refund_is_recorded_and_frees_the_budget(tmp_path):
    chain = FakeChain()
    ex, _, _ = make(tmp_path, chain, statuses=("PROCESSING", "REFUNDED"))
    st, p = TradingState(), proposal(status="approved")
    st.proposals.append(p)
    ex.execute(st, p)
    assert p.status == "refunded" and p.result["status"] == "REFUNDED" and st.spent("live") == 0.0


def test_shadow_fill_uses_a_dry_quote_and_no_signer(tmp_path):
    ex, seen, _ = make(tmp_path, FakeChain())
    ex.signer = None
    st, p = TradingState(), proposal(usd=5.0, mode="shadow")
    st.proposals.append(p)
    ex.shadow_fill(st, p)
    assert p.status == "shadow_filled" and seen["quotes"][0]["dry"] is True and "nothing was sent" in p.history[-1].note
    with pytest.raises(RuntimeError):
        ex.execute(st, p)                                                # a shadow proposal can never go live


def test_balances_are_read_without_a_key():
    chain = FakeChain()
    bal = read_balances(httpx.Client(transport=httpx.MockTransport(chain.rpc)), LiveConfig(), ACCOUNT,
                        [{"asset_id": "nep141:x", "symbol": "INTCon", "ticker": "INTC", "decimals": 18, "price": 56.0}])
    assert bal["near"] == 0.5 and bal["usdc"] == 5.0 and bal["holdings"] == [{"symbol": "INTCon", "ticker": "INTC", "quantity": 0.1, "value_usd": 5.6}]


def test_state_roundtrip(tmp_path):
    st = TradingState(proposals=[proposal()])
    save_state(st, tmp_path / "s.json")
    assert load_state(tmp_path / "s.json").get("abc1").ticker == "INTC"


# ---------------------------------------------------------------- trading agent (model output is checked by code)
class FakeRouter:
    def __init__(self, decision):
        self.decision, self.calls = decision, 0

    def complete(self, agent, messages, response_model=None):
        self.calls += 1
        assert agent == "trader" and "CANDIDATES" in messages[1]["content"]
        return NS(parsed=trader.TraderDecision(**self.decision), llm_alias="claude_opus_5_5")

    def usage_summary(self):
        return [{"agent": "trader", "cost_usd": 0.03}]


CANDS = [trader.Candidate(ticker="INTC", symbol="INTCon", asset_id="a1", topic="chiplet", quotable=True, quote_cost_pct=0.8),
         trader.Candidate(ticker="MSFT", symbol="MSFTon", asset_id="a2", topic="AI agents", quotable=False)]


def test_trader_buy_is_accepted_only_inside_the_rules():
    ok = trader.decide(FakeRouter({"action": "buy", "ticker": "intc", "usd": 5, "rationale": "r", "confidence": "high"}), CANDS, budget_usd=5, min_usd=1)
    assert ok.candidate.ticker == "INTC" and ok.decision.usd == 5.0 and ok.decision.confidence == "medium" and ok.cost_usd == 0.03
    sized = trader.decide(FakeRouter({"action": "buy", "ticker": "INTC", "usd": 2}), CANDS, budget_usd=5, min_usd=1)
    assert sized.decision.usd == 5.0 and "quote-tested size" in sized.notes[0]       # the size is fixed by code, not the model
    for bad in ({"action": "buy", "ticker": "MSFT", "usd": 5}, {"action": "buy", "ticker": "TSLA", "usd": 5},
                {"action": "buy", "ticker": "INTC", "usd": 50}, {"action": "buy", "ticker": "INTC", "usd": None}):
        res = trader.decide(FakeRouter(bad), CANDS, budget_usd=5, min_usd=1)
        assert res.decision.action == "hold" and res.candidate is None and "rejected by code" in res.decision.rationale
    hold = trader.decide(FakeRouter({"action": "hold", "rationale": "weak evidence"}), CANDS, budget_usd=5, min_usd=1)
    assert hold.decision.action == "hold" and hold.candidate is None


def test_trader_is_not_called_when_nothing_is_quotable():
    r = FakeRouter({"action": "buy", "ticker": "MSFT", "usd": 5})
    res = trader.decide(r, [CANDS[1]], budget_usd=5, min_usd=1)
    assert res.decision.action == "hold" and r.calls == 0


def test_trading_api_is_read_only_and_leaks_no_key(tmp_path):
    from fastapi.testclient import TestClient

    from app.api.main import create_app
    from app.config import Settings
    st = TradingState(proposals=[proposal(mode="shadow")])
    save_state(st, tmp_path / "trading" / "state.json")
    s = Settings(_env_file=None, fund_mainnet_private_key="ed25519:SECRETSECRETSECRET")      # key without an account: nothing is read
    app = create_app(s, store=NS(list=lambda limit=50: [], get=lambda i: None), funds_dir=tmp_path / "funds",
                     trading_dir=tmp_path / "trading", portfolio_path=tmp_path / "pf.json")
    c = TestClient(app)
    r = c.get("/api/trading")
    body = r.json()
    assert r.status_code == 200 and isinstance(body["trading_enabled"], bool) and body["key_configured"] is False and body["balances"] is None
    assert body["limits"]["max_total_usd"] > 0 and body["proposals"][0]["symbol"] == "INTCon"     # the switch and caps are the owner's live config
    assert "SECRET" not in r.text
    assert c.post("/api/trading").status_code == 405 and c.post("/api/trading/approve").status_code in (404, 405)


# ---------------------------------------------------------------- paying with NEAR (the owner's choice)
NEAR_CFG = dict(trading_enabled=True, poll_seconds=0.0, pay_with="near")


def test_near_payment_is_one_plain_transfer_sized_from_the_price(tmp_path):
    chain = FakeChain(near_yocto=5 * 10 ** 24)
    ex, seen, _ = make(tmp_path, chain, cfg=LiveConfig(**NEAR_CFG))
    st, p = TradingState(), proposal(status="approved")
    st.proposals.append(p)
    ex.execute(st, p)
    units = int(5.0 / 4.0 * 10 ** 24)                                     # $5 at $4 per NEAR = 1.25 NEAR
    assert p.status == "success" and p.deposit_tx == "tx-transfer"
    assert chain.calls == [("transfer", {"receiver": "depo1234", "amount": units}, units)]      # no storage call, no token call
    body = seen["quotes"][0]
    assert body["originAsset"] == "nep141:wrap.near" and body["amount"] == str(units) and body["dry"] is False
    assert "NEAR sent" in " ".join(e.note for e in p.history)


def test_near_payment_keeps_a_fee_reserve_and_never_retries(tmp_path):
    chain = FakeChain(near_yocto=int(1.27 * 10 ** 24))                    # needs 1.25 + 0.05 reserve
    ex, _, _ = make(tmp_path / "low", chain, cfg=LiveConfig(**NEAR_CFG))
    with pytest.raises(RuntimeError, match="kept for fees"):
        ex.execute(TradingState(), proposal(status="approved"))
    assert chain.calls == []
    chain = FakeChain(near_yocto=5 * 10 ** 24, fail_transfer=True)
    ex, _, _ = make(tmp_path / "drop", chain, cfg=LiveConfig(**NEAR_CFG))
    st, p = TradingState(), proposal(status="approved")
    with pytest.raises(RuntimeError, match="never approve again"):
        ex.execute(st, p)
    with pytest.raises(RuntimeError):
        ex.execute(st, p)
    assert len(chain.calls) == 1 and p.status == "deposited"


def test_shadow_quote_in_near_mode(tmp_path):
    ex, seen, _ = make(tmp_path, FakeChain(), cfg=LiveConfig(**NEAR_CFG))
    ex.signer = None
    st, p = TradingState(), proposal(mode="shadow")
    ex.shadow_fill(st, p)
    assert p.status == "shadow_filled" and seen["quotes"][0]["originAsset"] == "nep141:wrap.near" and seen["quotes"][0]["dry"] is True


# ---------------------------------------------------------------- shadow allocation (sizes are the agent's choice)
class PlanRouter:
    def __init__(self, plan):
        self.plan = plan

    def complete(self, agent, messages, response_model=None):
        assert "Pretend budget available: $10,000.00" in messages[1]["content"]
        return NS(parsed=trader.TraderPlan(**self.plan), llm_alias="claude_opus_5_5")

    def usage_summary(self):
        return [{"agent": "trader", "cost_usd": 0.04}]


def test_shadow_allocation_is_free_in_size_but_stays_in_list_and_budget():
    plan = {"orders": [{"ticker": "INTC", "usd": 2500, "reason": "a"}, {"ticker": "msft", "usd": 4000, "reason": "b"},
                       {"ticker": "TSLA", "usd": 900}, {"ticker": "INTC", "usd": 10}, {"ticker": "MSFT", "usd": -5}],
            "summary": "s", "confidence": "high"}
    res = trader.allocate(PlanRouter(plan), CANDS, budget_usd=10000)
    assert [(c.ticker, u) for c, u, _ in res.orders] == [("INTC", 2500.0), ("MSFT", 4000.0)] and res.plan.confidence == "medium"
    assert len(res.notes) == 3                                        # TSLA not a candidate, duplicate INTC, the duplicate MSFT
    over = trader.allocate(PlanRouter({"orders": [{"ticker": "INTC", "usd": 9000}, {"ticker": "MSFT", "usd": 6000}]}), CANDS, budget_usd=10000)
    assert [u for _, u, _ in over.orders] == [6000.0, 4000.0] and "scaled" in over.notes[0]
    assert trader.allocate(PlanRouter({}), [], budget_usd=10000).orders == []


def test_shadow_portfolio_adds_up_fills():
    from app.fund.live import shadow_portfolio
    st = TradingState()
    for usd, out in ((2500.0, "44.0"), (1500.0, "26.0")):
        p = proposal(usd=usd, mode="shadow")
        p.quote = {"amountOutFormatted": out}
        p.status = "shadow_filled"
        st.proposals.append(p)
    st.proposals.append(proposal(usd=999.0, mode="shadow", status="failed"))
    pf = shadow_portfolio(st, {"INTCon": 58.0}, 10000.0)
    assert pf["invested_usd"] == 4000.0 and pf["cash_usd"] == 6000.0
    pos = {k: v for k, v in pf["positions"][0].items() if k not in ("asset_id", "first_bought")}
    assert len(pf["positions"]) == 1 and pos == {"symbol": "INTCon", "ticker": "INTC", "topic": "chiplet", "quantity": 70.0, "cost_usd": 4000.0,
                                                 "orders": 2, "value_usd": 4060.0, "change_pct": 1.5}
    assert pf["value_usd"] == 10060.0


def test_private_route_orders_are_not_polled_through_the_public_status(tmp_path):
    from app.fund.live import Executor, LiveConfig, OneClickLive, Proposal, TradingState
    from datetime import datetime, timezone
    import httpx
    oc = OneClickLive("https://oc.test", http=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(404, json={"message": "not found"}))))
    ex = Executor(LiveConfig(poll_seconds=0.0), tmp_path / "state.json", oc, pay_asset="nep141:wrap.near", sleep=lambda s: None)
    p = Proposal(id="priv0000001", created_at=datetime(2026, 11, 10, tzinfo=timezone.utc), mode="live", topic="t", ticker="MRVL", symbol="MRVLon",
                 asset_id="nep141:mrvl", usd=25.0)
    p.status, p.deposit_address, p.quote = "deposited", "e9" * 32, {"route": "confidential"}
    import pytest
    with pytest.raises(RuntimeError, match="PRIVATE route"):
        ex.poll(TradingState(), p)
    assert p.status == "deposited"


def test_shadow_sale_moves_tokens_back_to_cash_at_average_cost():
    from datetime import timedelta
    from app.fund.live import shadow_portfolio
    st = TradingState()
    b = proposal(usd=4000.0, mode="shadow")
    b.quote, b.status = {"amountOutFormatted": "80.0"}, "shadow_filled"
    s = proposal(usd=2200.0, mode="shadow")
    s.side, s.created_at = "sell", b.created_at + timedelta(hours=30)
    s.quote, s.status = {"amountInFormatted": "40.0", "amountOutUsd": "2200.0"}, "shadow_filled"
    st.proposals += [b, s]
    pf = shadow_portfolio(st, {"INTCon": 55.0}, 10000.0)
    pos = pf["positions"][0]
    assert pos["quantity"] == 40.0 and pos["cost_usd"] == 2000.0                     # half sold: half the cost goes with it
    assert pf["cash_usd"] == 8200.0 and pf["realized_usd"] == 200.0 and pf["value_usd"] == 8200.0 + 40 * 55.0
    assert st.proceeds("shadow") == 2200.0 and st.spent("shadow") == 0.0            # shadow fills are not "spent" live money

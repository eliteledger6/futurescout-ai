"""Live trading test (stage 3) and shadow mode. Run by the OWNER, on this machine, by hand. See STAGE3_PLAN.md.

  python scripts\\fund_trade.py status                 limits, kill switch, account balances (read-only)
  python scripts\\fund_trade.py propose                the trading agent proposes ONE live buy (nothing is sent)
  python scripts\\fund_trade.py propose --shadow      shadow mode: the agent spreads the pretend budget (real quotes, nothing sent)
  python scripts\\fund_trade.py list                   proposals and their status
  python scripts\\fund_trade.py approve <id>           OWNER APPROVAL: executes that one live buy (asks you to confirm)
  python scripts\\fund_trade.py reject <id>
  python scripts\\fund_trade.py resume <id>            re-check a deposit that was sent but not finished (sends nothing)
  python scripts\\fund_trade.py stop | start           kill switch on / off

What can move money: ONLY `approve`, only when `live.trading_enabled: true` in config\\funds.yaml, the kill switch is
off, FUND_MAINNET_ACCOUNT_ID / FUND_MAINNET_PRIVATE_KEY are in .env, every limit passes and you type the confirmation.
It sends USDC from that dedicated account to a NEAR Intents deposit address; the tokens arrive in the same account
inside NEAR Intents. Everything else here is read-only or pretend money.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.agents.trader.agent import Candidate, allocate, decide  # noqa: E402
from app.chain import NearRecorder, NearRecordError  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.fund import load_fund_config, tradable_tokens as fund_tradable_tokens  # noqa: E402
from app.fund.intents_signed import SignedIntents  # noqa: E402
from app.fund.signed_exec import SignedExecutor, submit_signed_order  # noqa: E402
from app.fund.live import (Executor, MainnetSigner, OneClickLive, Proposal, check_limits, fingerprint, load_state,  # noqa: E402
                           new_id, read_balances, save_state, shadow_portfolio)
from app.models.config import load_model_config  # noqa: E402
from app.models.router import ModelRouter  # noqa: E402

FUNDS_DIR = service.RUNS_DIR / "funds"
STATE = service.RUNS_DIR / "trading" / "state.json"


def tradable_tokens() -> list[dict]:
    return fund_tradable_tokens(FUNDS_DIR)


def make_executor(s, cfg, *, with_signer: bool) -> Executor:  # noqa: ANN001
    key = s.oneclick_api_key.get_secret_value().strip() if s.oneclick_api_key else None
    signer = None
    creds = s.fund_mainnet_credentials()
    if with_signer and creds:
        signer = MainnetSigner(creds[0], creds[1], cfg.live.rpc)
    pay = cfg.live.near_asset_id if cfg.live.pay_with == "near" else cfg.intents.pay_asset
    return Executor(cfg.live, STATE, OneClickLive(cfg.intents.api, api_key=key or None), pay_asset=pay, signer=signer)


def cmd_status(s, cfg) -> int:  # noqa: ANN001
    state = load_state(STATE)
    ex = make_executor(s, cfg, with_signer=False)
    lv = cfg.live
    print(f"trading_enabled: {lv.trading_enabled}   kill switch: {'ON' if ex.kill_switch() else 'off'}")
    print(f"caps: ${lv.max_trade_usd:.2f} per trade, ${lv.max_day_usd:.2f} per day, ${lv.max_total_usd:.2f} in total; "
          f"spent live so far ${state.spent('live'):.2f}")
    creds = s.fund_mainnet_credentials()
    if not creds:
        print("account: not configured (FUND_MAINNET_ACCOUNT_ID / FUND_MAINNET_PRIVATE_KEY in .env)")
        return 0
    bal = read_balances(httpx.Client(timeout=30), lv, creds[0], tradable_tokens())
    print(f"account: {bal['account']}   NEAR {bal['near']}   USDC {bal['usdc']}   (trades are paid in {'NEAR' if lv.pay_with == 'near' else 'USDC'})")
    if lv.pay_with == "near" and bal["near"] is not None:
        try:
            px = ex.oneclick.price_usd(lv.near_asset_id)
            print(f"   NEAR is about ${px:.2f}: the balance is worth about ${bal['near'] * px:.2f}; a ${lv.max_trade_usd:.0f} trade needs about "
                  f"{lv.max_trade_usd / px + lv.near_reserve:.2f} NEAR including the fee reserve")
        except Exception:  # noqa: BLE001
            pass
    for h in bal["holdings"]:
        print(f"   holds {h['quantity']} {h['symbol']} (about ${h['value_usd']})")
    for e in bal["errors"]:
        print("   note:", e)
    return 0


def cmd_shadow(s, cfg, usd: float | None) -> int:  # noqa: ANN001
    """Shadow mode: the agent spreads the pretend budget as it sees fit; every order gets a real dry quote; nothing is sent."""
    state = load_state(STATE)
    lv = cfg.live
    ex = make_executor(s, cfg, with_signer=False)
    now = datetime.now(timezone.utc)
    toks = tradable_tokens()
    if not toks:
        print("no tradable token in the funds; run scripts\\funds.py first")
        return 1
    pf = shadow_portfolio(state, {t["symbol"]: t["price"] for t in toks if t.get("price")}, lv.shadow_budget_usd)
    budget = min(usd, pf["cash_usd"]) if usd else pf["cash_usd"]
    if budget < 1:
        print(f"the shadow budget is fully used (${pf['invested_usd']:,.2f} of ${lv.shadow_budget_usd:,.2f} placed)")
        return 0
    account = (s.fund_mainnet_account_id or "intents.near").strip() or "intents.near"
    cands = []
    for t in toks:
        c = Candidate(ticker=t["ticker"], symbol=t["symbol"], asset_id=t["asset_id"], topic=t["topic"], verdict_band=t["band"], score=t["score"], confidence_pct=t.get("confidence_pct"),
                      tier=t["tier"], why=t["why"], price_stretch=t["stretch"], last_close=t["last_close"], last_close_date=t["last_close_date"], quotable=True)
        try:
            q = ex.dry_quote(c.asset_id, min(1000.0, budget), account)
            c.quote_cost_pct = round((float(q["amountInUsd"]) - float(q["amountOutUsd"])) / float(q["amountInUsd"]) * 100, 2)
        except (RuntimeError, KeyError, ValueError, httpx.HTTPError) as exc:
            c.note = str(exc)[:120]
        cands.append(c)
    res = allocate(ModelRouter(load_model_config(), s), cands, budget_usd=budget, holdings=pf["positions"])
    for n in res.notes:
        print("  note:", n)
    print(f"\nSHADOW PLAN by {res.model} (${res.cost_usd:.3f}): {res.plan.summary}")
    if not res.orders:
        p = Proposal(id=new_id(), created_at=now, mode="shadow", side="hold", topic="", ticker="", symbol="", asset_id="", usd=0.0,
                     rationale=res.plan.summary, risks=res.plan.risks, confidence=res.plan.confidence, model=res.model, model_cost_usd=res.cost_usd)
        p.mark("hold", "the agent kept the shadow budget in cash", now)
        p.sha256 = fingerprint(p)
        state.proposals.append(p)
        save_state(state, STATE)
        return 0
    for i, (c, amount, reason) in enumerate(res.orders):
        p = Proposal(id=new_id(), created_at=now, mode="shadow", topic=c.topic, ticker=c.ticker, symbol=c.symbol, asset_id=c.asset_id, usd=amount,
                     rationale=reason or res.plan.summary, risks=res.plan.risks, confidence=res.plan.confidence, model=res.model,
                     model_cost_usd=res.cost_usd if i == 0 else 0.0, ref_close=c.last_close, ref_close_date=c.last_close_date)
        p.mark("proposed", f"shadow plan: ${amount:,.2f} of {c.symbol}", now)
        state.proposals.append(p)
        ex.shadow_fill(state, p, account=account)
        print(f"  {p.status:13} ${amount:9,.2f} {c.symbol:8} {p.history[-1].note[:110]}")
    pf = shadow_portfolio(load_state(STATE), {t["symbol"]: t["price"] for t in toks if t.get("price")}, lv.shadow_budget_usd)
    print(f"shadow portfolio: ${pf['invested_usd']:,.2f} placed, ${pf['cash_usd']:,.2f} cash, of ${pf['budget_usd']:,.2f}")
    return 0


def cmd_propose(s, cfg, shadow: bool, usd: float | None) -> int:  # noqa: ANN001
    if shadow:
        return cmd_shadow(s, cfg, usd)
    state = load_state(STATE)
    lv = cfg.live
    ex = make_executor(s, cfg, with_signer=False)
    now = datetime.now(timezone.utc)
    if shadow:
        used = state.spent("shadow") + sum(p.usd for p in state.proposals if p.mode == "shadow" and p.status == "shadow_filled")
        budget = min(usd or 100.0, lv.shadow_budget_usd - used)
    else:
        day = now.date().isoformat()
        budget = min(usd or lv.max_trade_usd, lv.max_trade_usd, lv.max_total_usd - state.spent("live"), lv.max_day_usd - state.spent("live", day))
    if budget < lv.min_trade_usd:
        print(f"no budget left for a {'shadow' if shadow else 'live'} proposal (${budget:.2f})")
        return 1
    toks = tradable_tokens()
    if not toks:
        print("no tradable token in the funds; run scripts\\funds.py first")
        return 1
    account = (s.fund_mainnet_account_id or "intents.near").strip() or "intents.near"
    cands = []
    for t in toks:
        c = Candidate(ticker=t["ticker"], symbol=t["symbol"], asset_id=t["asset_id"], topic=t["topic"], verdict_band=t["band"], score=t["score"], confidence_pct=t.get("confidence_pct"),
                      tier=t["tier"], why=t["why"], price_stretch=t["stretch"], last_close=t["last_close"], last_close_date=t["last_close_date"])
        try:
            q = ex.dry_quote(c.asset_id, budget, account)
            c.dry_quote, c.quotable = q, True
            c.quote_cost_pct = round((float(q["amountInUsd"]) - float(q["amountOutUsd"])) / float(q["amountInUsd"]) * 100, 2)
        except (RuntimeError, KeyError, ValueError, httpx.HTTPError) as exc:
            c.note = str(exc)[:120]
        cands.append(c)
        print(f"  candidate {c.ticker:6} ({c.topic[:28]}): " + (f"quotable at ${budget:.2f}, cost {c.quote_cost_pct}%" if c.quotable else f"NOT quotable at ${budget:.2f}: {c.note}"))
    router = ModelRouter(load_model_config(), s)
    res = decide(router, cands, budget_usd=budget, min_usd=lv.min_trade_usd)
    d = res.decision
    for n in res.notes:
        print("  note:", n)
    if d.action == "hold" or res.candidate is None:
        p = Proposal(id=new_id(), created_at=now, mode="shadow" if shadow else "live", side="hold", topic="", ticker="", symbol="", asset_id="",
                     usd=0.0, rationale=d.rationale, risks=d.risks, confidence=d.confidence, model=res.model, model_cost_usd=res.cost_usd)
        p.mark("hold", "the agent proposed to hold", now)
        p.sha256 = fingerprint(p)
        state.proposals.append(p)
        save_state(state, STATE)
        print(f"\nHOLD: {d.rationale}")
        return 0
    c = res.candidate
    p = Proposal(id=new_id(), created_at=now, mode="shadow" if shadow else "live", topic=c.topic, ticker=c.ticker, symbol=c.symbol, asset_id=c.asset_id,
                 usd=float(d.usd), rationale=d.rationale, risks=d.risks, confidence=d.confidence, model=res.model, model_cost_usd=res.cost_usd,
                 ref_close=c.last_close, ref_close_date=c.last_close_date, dry_quote=c.dry_quote)
    p.mark("proposed", f"trading agent ({res.model}) proposed to buy ${p.usd:.2f} of {p.symbol}", now)
    state.proposals.append(p)
    save_state(state, STATE)
    print(f"\nPROPOSAL {p.id}: buy ${p.usd:.2f} of {p.symbol} ({p.ticker}, topic: {p.topic})  [model {res.model}, ${res.cost_usd:.3f}]")
    print(f"  why: {d.rationale}")
    for r in d.risks:
        print(f"  risk: {r}")
    if shadow:
        ex.shadow_fill(state, p, account=account)
        print(f"  shadow result: {p.status}: {p.history[-1].note}")
    else:
        blocked = check_limits(state, p, lv, kill_switch=ex.kill_switch(), now=now)
        if blocked:
            print("  it cannot be executed yet: " + "; ".join(blocked))
        print(f"  to approve (this is the step that sends money):  python scripts\\fund_trade.py approve {p.id}")
    return 0


def seal(s, p: Proposal) -> None:  # noqa: ANN001
    creds = s.near_testnet_credentials()
    if not creds or not p.sha256:
        return
    try:
        p.chain = NearRecorder(*creds).record_fund_decision(f"trade_{p.id}", {"sha256": p.sha256, "status": p.status, "symbol": p.symbol,
                                                                              "usd": str(p.usd), "mode": p.mode}).as_dict()
        print("  record fingerprint sealed on NEAR testnet")
    except NearRecordError as exc:
        print(f"  (record not sealed: {str(exc)[:100]})")


def rpc_view_salt(cfg):  # noqa: ANN001,ANN201
    from app.fund.live import rpc_view
    return rpc_view(httpx.Client(timeout=30), cfg.live.rpc, cfg.live.intents_contract, "current_salt", {})


def cmd_approve(s, cfg, pid: str) -> int:  # noqa: ANN001
    state = load_state(STATE)
    p = state.get(pid)
    if p is None or p.mode != "live" or p.status != "proposed":
        print("no live proposal in status 'proposed' with that id")
        return 1
    signed_route = cfg.live.route == "confidential"
    creds = s.fund_mainnet_credentials()
    ex = make_executor(s, cfg, with_signer=not signed_route)
    now = datetime.now(timezone.utc)
    blocked = check_limits(state, p, cfg.live, kill_switch=ex.kill_switch(), now=now)
    if not creds:
        blocked.append("FUND_MAINNET_ACCOUNT_ID / FUND_MAINNET_PRIVATE_KEY are not set in .env")
    if signed_route:
        api_key = s.oneclick_api_key.get_secret_value().strip() if s.oneclick_api_key else None
        if not cfg.live.signed_route_enabled:
            blocked.append("the signed-order route is built but switched off (live.signed_route_enabled is false in config\\funds.yaml)")
        if not api_key:
            blocked.append("ONECLICK_API_KEY is not set in .env (the private route needs the partner API key)")
        if creds and not blocked:
            http = httpx.Client(timeout=40)
            ex = SignedExecutor(cfg.live, STATE, SignedIntents(cfg.intents.api, api_key=api_key), ex.oneclick, account=creds[0], private_key=creds[1],
                                salt_reader=lambda: str(rpc_view_salt(cfg)),
                                submitter=lambda order, key: submit_signed_order(http, cfg.intents.api, api_key, order, key))
    elif ex.signer is None:
        blocked.append("FUND_MAINNET_ACCOUNT_ID / FUND_MAINNET_PRIVATE_KEY are not set in .env")
    if blocked:
        print("cannot execute:\n  - " + "\n  - ".join(blocked))
        return 1
    coin = "NEAR" if cfg.live.pay_with == "near" else "USDC"
    source = "the PRIVATE balance (near.com route, signed order)" if signed_route else "the wallet"
    print(f"REAL MONEY. About to pay ${p.usd:.2f} of {coin} from {source} of {creds[0]} (NEAR mainnet) to buy {p.symbol}.")
    print(f"  agent's reason: {p.rationale}")
    typed = input(f"Type  APPROVE {p.id}  to go ahead (anything else cancels): ").strip()
    if typed != f"APPROVE {p.id}":
        print("cancelled; nothing was sent")
        return 1
    p.mark("approved", "approved by the owner at the keyboard", datetime.now(timezone.utc))
    save_state(state, STATE)
    try:
        ex.execute(state, p)
    except RuntimeError as exc:
        print(f"STOPPED: {exc}")
        return 1
    print(f"RESULT: {p.status}  {p.result or ''}")
    if p.deposit_tx:
        print("  deposit tx:", cfg.live.explorer_tx.format(tx=p.deposit_tx))
    seal(s, p)
    save_state(state, STATE)
    return 0 if p.status == "success" else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["status", "propose", "list", "approve", "reject", "resume", "confirm", "refunded", "stop", "start", "register-usdc"])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--shadow", action="store_true")
    ap.add_argument("--usd", type=float)
    args = ap.parse_args()
    s, cfg = get_settings(), load_fund_config()
    STATE.parent.mkdir(parents=True, exist_ok=True)
    stop = STATE.with_name("STOP")
    if args.command == "status":
        return cmd_status(s, cfg)
    if args.command == "propose":
        return cmd_propose(s, cfg, args.shadow, args.usd)
    if args.command == "list":
        for p in load_state(STATE).proposals[-30:]:
            print(f"{p.id}  {p.created_at:%m-%d %H:%M}  {p.mode:6} {p.status:13} {p.side:4} ${p.usd:7.2f} {p.symbol:8} {p.rationale[:70]}")
        return 0
    if args.command == "register-usdc":
        ex = make_executor(s, cfg, with_signer=True)
        if ex.signer is None:
            print("FUND_MAINNET_ACCOUNT_ID / FUND_MAINNET_PRIVATE_KEY are not set in .env")
            return 1
        from app.fund.live import rpc_view
        acc = ex.signer.account_id
        if rpc_view(httpx.Client(timeout=30), cfg.live.rpc, cfg.live.usdc_contract, "storage_balance_of", {"account_id": acc}):
            print(f"{acc} can already hold USDC; nothing to do")
            return 0
        if input(f"Register {acc} to hold USDC on NEAR mainnet? Costs 0.00125 NEAR. Type YES: ").strip() != "YES":
            print("cancelled")
            return 1
        try:
            tx = ex.signer.call(cfg.live.usdc_contract, "storage_deposit", {"account_id": acc, "registration_only": True}, 30 * 10 ** 12, 1_250_000_000_000_000_000_000)
        except RuntimeError as exc:
            print(f"failed: {exc}")
            return 1
        print("registered; the account can now receive USDC.", cfg.live.explorer_tx.format(tx=tx) if tx else "")
        return 0
    if args.command == "stop":
        stop.write_text("trading stopped by the owner\n", encoding="utf-8")
        print("kill switch ON: no live trade can run until 'start'")
        return 0
    if args.command == "start":
        stop.unlink(missing_ok=True)
        print("kill switch off")
        return 0
    if not args.id:
        print("this command needs a proposal id")
        return 1
    if args.command == "approve":
        return cmd_approve(s, cfg, args.id)
    state = load_state(STATE)
    p = state.get(args.id)
    if p is None:
        print("no such proposal")
        return 1
    if args.command == "reject":
        if p.status != "proposed":
            print(f"proposal is '{p.status}'; only a proposed one can be rejected")
            return 1
        p.mark("rejected", "rejected by the owner")
        p.sha256 = fingerprint(p)
        save_state(state, STATE)
        print("rejected")
        return 0
    if args.command in ("confirm", "refunded"):
        # The owner saw the outcome in near.com (private-route orders are invisible to the public status check).
        if p.status != "deposited":
            print(f"proposal is '{p.status}'; only a submitted ('deposited') order can be confirmed")
            return 1
        if args.command == "confirm":
            q = p.quote or {}
            p.result = {"status": "SUCCESS (seen by the owner in near.com; not read from the service)",
                        "amountInFormatted": q.get("amountInFormatted"), "amountOutFormatted": q.get("amountOutFormatted"),
                        "amountOutUsd": q.get("amountOutUsd"), "amounts_are": "the quote, not the fill"}
            p.mark("success", "owner confirmed in near.com that the stock arrived (private route; amounts are the quoted ones)")
        else:
            p.mark("refunded", "owner reported in near.com that the payment came back (private route)")
        p.sha256 = fingerprint(p)
        seal(s, p)
        save_state(state, STATE)
        print(f"recorded: {p.status}")
        return 0
    if args.command == "resume":
        ex = make_executor(s, cfg, with_signer=False)
        try:
            ex.poll(state, p)
        except RuntimeError as exc:
            print(str(exc))
            return 1
        print(f"RESULT: {p.status}  {p.result or ''}")
        seal(s, p)
        save_state(state, STATE)
    return 0


if __name__ == "__main__":
    sys.exit(main())

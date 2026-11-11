"""Live trading test (stage 3) and shadow mode. Run by the OWNER, on this machine, by hand. See STAGE3_PLAN.md.

  python scripts\\fund_trade.py status                 limits, kill switch, account balances (read-only)
  python scripts\\fund_trade.py propose                the trading agent proposes ONE live buy (nothing is sent)
  python scripts\\fund_trade.py propose --shadow      shadow mode: the agent spreads the pretend budget (real quotes, nothing sent)
  python scripts\\fund_trade.py list                   proposals and their status
  python scripts\\fund_trade.py approve <id>           OWNER APPROVAL: executes that one live buy (asks you to confirm)
  python scripts\\fund_trade.py reject <id>
  python scripts\\fund_trade.py resume <id>            re-check a deposit that was sent but not finished (sends nothing)
  python scripts\\fund_trade.py stop | start           kill switch on / off
  python scripts\\fund_trade.py check [--shadow] [--review]   strategy wake-up (--review: an extra full keep/sell/buy review now)
  python scripts\\fund_trade.py watch                  shadow + live checks every hour (live executes only with live.auto_approve)
  python scripts\\fund_trade.py holdings               what the live fund holds according to its records

Selling (owner's written yes 2026-11-10) is off until the owner sets `live.sells_enabled: true`; a sale pays the stock token
from the PRIVATE balance and gets NEAR back (signed route only). With `live.budget_mode: net` the total cap counts buys minus
sale proceeds, so money from a sale can be invested again.

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
from app.fund.strategy import RULES, Check, Trigger, assess, detect_triggers  # noqa: E402
from app.fund.live import TradingState  # noqa: E402,F401
from app.fund.live import (Executor, MainnetSigner, OneClickLive, Proposal, check_limits, fingerprint, load_state,  # noqa: E402
                           new_id, read_balances, save_state, shadow_portfolio)
from app.models.config import load_model_config  # noqa: E402
from app.models.router import ModelRouter  # noqa: E402

FUNDS_DIR = service.RUNS_DIR / "funds"
ECONOMY = service.RUNS_DIR / "economy" / "state.json"
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


def cmd_check(s, cfg, shadow: bool, loop: bool) -> int:  # noqa: ANN001
    """Strategy wake-up for ONE mode; with --loop, forever (one check every strategy.check_minutes)."""
    import time
    while True:
        rc = run_check(s, cfg, shadow)
        if not loop:
            return rc
        time.sleep(max(60, cfg.live.strategy.check_minutes * 60))


def cmd_watch(s, cfg, publish: bool = False) -> int:  # noqa: ANN001
    """The auto-trading loop (owner request 2026-11-10): every check_minutes, a shadow check (pretend money, fills itself) and a
    live check (real money: a PROPOSAL; executed only after the owner's typed approval, unless the owner has set live.auto_approve)."""
    import time
    print(f"auto-trading loop: shadow + live check every {cfg.live.strategy.check_minutes} min; live.auto_approve is "
          f"{'ON (owner setting): approved proposals are sent' if cfg.live.auto_approve else 'off: live proposals wait for the owner'}. "
          f"Publishing to the hosted site: {'on (after a trade, a report purchase or a stake)' if publish else 'off (--publish)'}. Ctrl+C stops.")
    from app.site_publish import publish as site_publish, trade_fingerprint
    shown = trade_fingerprint(service.RUNS_DIR)
    while True:
        for shadow in (True, False):
            try:
                run_check(s, cfg, shadow)
            except Exception as exc:  # noqa: BLE001  (one failed check must not kill the loop)
                print(f"  check failed ({'shadow' if shadow else 'live'}): {type(exc).__name__}: {str(exc)[:160]}")
        if cfg.economy.enabled and cfg.economy.staking_contract and s.report_agent_credentials():
            try:
                cmd_economy(s, cfg, "stake")
            except Exception as exc:  # noqa: BLE001
                print(f"  stake step failed: {type(exc).__name__}: {str(exc)[:160]}")
        if publish:
            now_fp = trade_fingerprint(service.RUNS_DIR)
            if now_fp != shown:                              # only when the trading page would show something new
                try:
                    site_publish("Site data update (trading agent)")
                    shown = now_fp
                except Exception as exc:  # noqa: BLE001
                    print(f"  publish failed: {type(exc).__name__}: {str(exc)[:160]}")
        time.sleep(max(60, cfg.live.strategy.check_minutes * 60))


def cmd_pending(s, cfg) -> int:  # noqa: ANN001
    state = load_state(STATE)
    waiting = [p for p in state.proposals if p.mode == "live" and p.status == "proposed"]
    if not waiting:
        print("no live proposal is waiting for approval")
        return 0
    for p in waiting:
        what = f"SELL {round((p.fraction or 1) * 100)}% of {p.symbol} (about ${p.usd:.2f})" if p.side == "sell" else f"buy ${p.usd:.2f} of {p.symbol}"
        print(f"{p.id}  {p.created_at:%m-%d %H:%M} UTC  {what} ({p.topic})\n   why: {p.rationale[:300]}\n"
              f"   approve:  python scripts\\fund_trade.py approve {p.id}     reject:  python scripts\\fund_trade.py reject {p.id}")
    return 0


def run_check(s, cfg, shadow: bool, extra: list | None = None, depth: int = 0) -> int:  # noqa: ANN001
    """Strategy wake-up: look for triggers (new report, sharp move, routine review); if any, the agent assesses and decides.
    Shadow: filled with pretend money. Live: a proposal the owner approves (or, only if the owner set live.auto_approve, sent)."""
    import hashlib
    import json
    from app.fund import PriceBook
    from app.fund.live import shadow_portfolio
    from app.sources.prices import AlphaVantageClient
    st_cfg = cfg.live.strategy
    if not shadow and cfg.live.auto_approve:
        try:
            refresh_private_balance(s, cfg)
        except Exception as exc:  # noqa: BLE001
            print(f"  near.com balance not readable: {str(exc)[:100]}")
    state = load_state(STATE)
    now = datetime.now(timezone.utc)
    mode = "shadow" if shadow else "live"
    toks = tradable_tokens()
    if not toks:
        print("no tradable token in the funds; run scripts\\funds.py first")
        return 1
    # prices: the cache first, a few Alpha Vantage calls at most
    prices = AlphaVantageClient(s.alpha_vantage_key_value()) if s.alpha_vantage_key_value() else None
    book = PriceBook(prices, max_requests=st_cfg.price_requests_per_check)
    closes: dict = {}
    held_rows = state.live_holdings() if not shadow else []
    for t in toks + [h for h in held_rows if h["ticker"] not in {x["ticker"] for x in toks}]:
        bars = book.bars(t["ticker"])
        if len(bars) >= 2:
            closes[t["ticker"]] = (bars[-1].day.isoformat(), bars[-1].close, bars[-2].close)
        elif bars:
            closes[t["ticker"]] = (bars[-1].day.isoformat(), bars[-1].close, None)
    pf = shadow_portfolio(state, {t["symbol"]: t["price"] for t in toks if t.get("price")}, cfg.live.shadow_budget_usd)
    held = {p["ticker"] for p in pf["positions"]} if shadow else {p.ticker for p in state.proposals if p.mode == "live" and p.status == "success"}
    # shadow and live each react to every event once: live keys are prefixed so a shadow check does not "use up" a trigger
    kp = "" if shadow else "live:"
    seen_runs = {k[len(kp):]: v for k, v in state.seen_runs.items() if k.startswith(kp) and (shadow and not k.startswith("live:") or not shadow)}
    seen_closes = {k[len(kp):]: v for k, v in state.seen_closes.items() if k.startswith(kp) and (shadow and not k.startswith("live:") or not shadow)}
    triggers = detect_triggers(tokens=toks, seen_runs=seen_runs, closes=closes, seen_closes=seen_closes,
                               last_check=state.last_check_at if shadow else state.last_live_check_at, now=now, cfg=st_cfg, held=held)
    triggers += list(extra or [])
    check = Check(id=new_id(), at=now, mode=mode, triggers=triggers)
    print(f"[{now:%Y-%m-%d %H:%M} UTC] {mode} check: " + (", ".join(f"{t.kind} {t.ticker or t.topic}".strip() for t in triggers) or "no trigger"))
    if not triggers:
        check.action = "none"
        check.summary = "No trigger: no new report, no sharp move, no review due. The agent was not called."
    else:
        check = _assess(s, cfg, state, toks, triggers, check, shadow, now, pf, closes)
    for t in triggers:                       # remember what was reacted to, so the same event does not wake the agent twice
        if t.kind == "new_report":
            state.seen_runs[kp + t.topic] = next((x.get("run_id") for x in toks if x["topic"] == t.topic), "") or ""
        if t.kind in ("price_drop", "price_jump") and t.ticker in closes:
            state.seen_closes[kp + t.ticker] = closes[t.ticker][0]
    if shadow:
        state.last_check_at = now
    else:
        state.last_live_check_at = now
    check.sha256 = hashlib.sha256(json.dumps(check.model_dump(mode="json", exclude={"sha256", "correction"}), sort_keys=True).encode()).hexdigest()
    state.checks = (state.checks or [])[-199:] + [check.model_dump(mode="json")]
    save_state(state, STATE)
    print(f"  -> {check.action}: {check.summary[:200]}")
    rc, sold = 0, False
    if shadow and check.action == "sell" and check.proposal_id:
        sold = getattr(state.get(check.proposal_id), "status", "") == "shadow_filled"
    if not shadow and check.action in ("buy", "sell") and check.proposal_id:
        if cfg.live.auto_approve:
            print("  live.auto_approve is ON (owner setting): executing through the same checks as a typed approval")
            rc = cmd_approve(s, cfg, check.proposal_id, auto=True)
            sold = check.action == "sell" and getattr(load_state(STATE).get(check.proposal_id), "status", "") == "success"
        else:
            print(f"  waiting for the owner:  python scripts\\fund_trade.py approve {check.proposal_id}   (or reject)")
    if sold and depth == 0:
        p = load_state(STATE).get(check.proposal_id)
        got = p.result or p.quote or {}
        print("  sale done: waking the agent once more to decide what to do with the money")
        return run_check(s, cfg, shadow, extra=[Trigger(kind="after_sale", ticker=p.ticker, topic=p.topic,
                                                       detail=f"sold {got.get('amountInFormatted')} {p.symbol} for about ${float(got.get('amountOutUsd') or 0):.2f}; "
                                                              "that money is now available")], depth=1)
    return rc


def holding_value(ex, h: dict, account: str = "intents.near") -> float | None:  # noqa: ANN001
    """What the whole holding would fetch now: a real DRY sale quote (stock -> NEAR, from a balance inside NEAR Intents).
    The public token list leaves the tokenized stocks out, so a price lookup there gave $0 (bug seen 2026-11-10)."""
    try:
        q = ex.oneclick.quote(dry=True, pay_asset=h["asset_id"], dest_asset=ex.cfg.near_asset_id, amount_units=int(h["quantity"] * 10 ** 18),
                              account=account, slippage_bps=ex.cfg.slippage_bps, deadline=datetime.now(timezone.utc) + timedelta(minutes=10),
                              deposit_type="INTENTS")
        return round(float(q["amountInUsd"]), 2)
    except Exception:  # noqa: BLE001
        return None


def fund_reports_by_ticker() -> dict:
    """Every company any topic fund holds, with that fund's latest report verdict and confidence: also the ones NEAR Intents
    cannot trade right now (bug seen 2026-11-11: a holding whose route was down looked like 'no report names it any more')."""
    from app.fund import list_funds
    out: dict = {}
    for f in list_funds(service.RUNS_DIR / "funds"):
        last = f.decisions[-1] if f.decisions else None
        for h in f.holdings:
            row = {"ticker": h.ticker, "topic": f.topic, "band": last.band if last else None,
                   "confidence_pct": last.confidence_pct if last else None, "score": last.score if last else None,
                   "tradable_now": bool(h.route and h.route.available and h.route.asset_id)}
            if h.ticker not in out or (row["score"] or 0) > (out[h.ticker]["score"] or 0):
                out[h.ticker] = row
    return out


def _sellable(state, toks, pf, shadow, closes, now, ex):  # noqa: ANN001,ANN201
    """Holdings the agent may consider selling, each with its latest report (or a note that no fund includes it any more)."""
    rows = pf["positions"] if shadow else state.live_holdings()
    out = []
    in_funds = fund_reports_by_ticker()
    for h in rows:
        tok = next((t for t in toks if t["ticker"] == h["ticker"]), None) or in_funds.get(h["ticker"])
        try:
            first = datetime.fromisoformat(str(h.get("first_bought")))
            hours = (now - first).total_seconds() / 3600
        except ValueError:
            hours = 0.0
        value = h.get("value_usd")
        if value is None:
            value = holding_value(ex, h)
        day, close, _prev = closes.get(h["ticker"], (None, None, None))
        out.append({"ticker": h["ticker"], "symbol": h["symbol"], "asset_id": h.get("asset_id"), "topic": h.get("topic"), "quantity": h["quantity"],
                    "cost_usd": h.get("cost_usd"), "value_usd": value, "held_hours": round(hours, 1), "last_close": close, "last_close_date": day,
                    "report_verdict": (tok or {}).get("band") if tok and tok["ticker"] == h["ticker"] else None,
                    "report_confidence_pct": (tok or {}).get("confidence_pct") if tok and tok["ticker"] == h["ticker"] else None,
                    "still_in_a_fund": bool(tok and tok["ticker"] == h["ticker"]),
                    "note": ("" if tok and tok["ticker"] == h["ticker"] and tok.get("tradable_now", True) else
                             "its report still names it, but NEAR Intents cannot trade it right now (no quote): not a reason to sell"
                             if tok and tok["ticker"] == h["ticker"] else
                             "no topic fund includes this company any more (its report no longer names it)")})
    return out


def _assess(s, cfg, state, toks, triggers, check, shadow, now, pf, closes=None):  # noqa: ANN001,ANN201
    """Build candidates with real dry quotes, give the agent the evidence, apply its decision (shadow fill or live proposal)."""
    lv = cfg.live
    ex = make_executor(s, cfg, with_signer=False)
    account = (s.fund_mainnet_account_id or "intents.near").strip() or "intents.near"
    day = now.date().isoformat()
    if shadow:
        budget, fixed = pf["cash_usd"], None
    else:
        budget = min(lv.max_trade_usd, lv.max_total_usd - state.invested("live", lv.budget_mode), lv.max_day_usd - state.spent("live", day))
        fixed = budget if budget >= lv.min_trade_usd else None
    can_buy = budget >= (1 if shadow else lv.min_trade_usd)
    sells_on = True if shadow else lv.sells_enabled
    sells_left = max(0, lv.max_sells_per_day - state.sells_today("shadow" if shadow else "live", day))
    sellable = _sellable(state, toks, pf, shadow, closes or {}, now, ex)
    if not can_buy and not (sells_on and sells_left and sellable):
        check.action, check.summary = "hold", f"No budget left (${budget:.2f}) and nothing can be sold; the agent was not called."
        return check
    cands = []
    for t in toks:
        c = Candidate(ticker=t["ticker"], symbol=t["symbol"], asset_id=t["asset_id"], topic=t["topic"], verdict_band=t["band"], score=t["score"],
                      confidence_pct=t.get("confidence_pct"), tier=t["tier"], why=t["why"], price_stretch=t["stretch"], last_close=t["last_close"],
                      last_close_date=t["last_close_date"])
        try:
            q = ex.dry_quote(c.asset_id, fixed or (min(1000.0, budget) if can_buy else lv.max_trade_usd), account)
            c.quotable, c.dry_quote = True, q
            c.quote_cost_pct = round((float(q["amountInUsd"]) - float(q["amountOutUsd"])) / float(q["amountInUsd"]) * 100, 2)
        except (RuntimeError, KeyError, ValueError, httpx.HTTPError) as exc:
            c.note = str(exc)[:120]
        cands.append(c)
    context = evidence_context(s, toks)
    if not shadow and cfg.economy.enabled:
        bought = economy_buy_reports(s, cfg, toks, cands, now, execute=cfg.live.auto_approve, only_actionable=True)
        dropped = sorted({c.ticker for c in cands if c.topic not in bought})
        cands = [c for c in cands if c.topic in bought]
        context = {k: v for k, v in context.items() if k in bought}
        if dropped:
            check.notes.append(f"not usable (report not bought): {', '.join(dropped)}")
            print(f"  reports not bought, so not usable: {', '.join(dropped)}")
    if not shadow and cfg.live.auto_approve and cfg.live.route == "confidential":
        # Size by the NEAR really in near.com (after any report payments), not only by the caps (bug seen 2026-11-10:
        # a $60 order was proposed with 12.465 NEAR, about $45, available; the pre-sign check refused it, nothing was sent).
        try:
            priv = refresh_private_balance(s, cfg)
        except Exception as exc:  # noqa: BLE001
            priv = None
            print(f"  near.com balance not readable: {str(exc)[:100]}")
        if priv is not None:
            room = max(0.0, (priv - lv.private_reserve_near) * near_price(ex) * 0.99)
            if fixed and room < fixed:
                check.notes.append(f"trade size cut from ${fixed:.2f} to ${room:.2f}: near.com holds {priv:.3f} NEAR "
                                   f"({lv.private_reserve_near} NEAR kept back)")
                print(f"  near.com holds {priv:.3f} NEAR: trade size cut from ${fixed:.2f} to ${room:.2f}")
                fixed = round(room, 2) if room >= lv.min_trade_usd else None
                budget = min(budget, room)
                can_buy = fixed is not None
    holdings = pf["positions"] if shadow else [{"ticker": h["ticker"], "symbol": h["symbol"], "cost_usd": h["cost_usd"]} for h in state.live_holdings()]
    adds = {}
    for p in state.proposals:
        if p.mode == ("shadow" if shadow else "live") and p.side == "buy" and p.status in ("shadow_filled", "success", "deposited", "executing", "proposed", "approved"):
            adds[p.ticker.upper()] = adds.get(p.ticker.upper(), 0) + 1
    d, cand, model, cost, notes = assess(ModelRouter(load_model_config(), s), triggers=triggers, candidates=cands, holdings=holdings, context=context,
                                         budget_usd=max(0.0, budget), fixed_usd=fixed, cfg=lv.strategy, adds_so_far=adds, sellable=sellable,
                                         sells_enabled=sells_on, can_buy=can_buy, sells_left_today=sells_left,
                                         min_sale_usd=0.0 if shadow else lv.min_trade_usd, price_band_pct=lv.price_band_pct)
    check.model, check.cost_usd, check.notes, check.what_changed = model, cost, notes, d.what_changed
    check.action, check.summary = d.action, d.rationale
    for n in notes:
        print("  note:", n)
    print(f"  agent ({model}, ${cost:.3f}): {d.what_changed}")
    mode = "shadow" if shadow else "live"
    if d.action == "sell" and isinstance(cand, dict):
        h = cand
        p = Proposal(id=new_id(), created_at=now, mode=mode, side="sell", topic=h.get("topic") or "", ticker=h["ticker"], symbol=h["symbol"],
                     asset_id=h["asset_id"], usd=float(d.usd or 0), fraction=d.fraction, quantity=round(h["quantity"] * (d.fraction or 1), 12),
                     rationale=f"{d.what_changed} {d.rationale}".strip(), risks=d.risks, confidence=d.confidence, model=model, model_cost_usd=cost,
                     ref_close=h.get("last_close"), ref_close_date=h.get("last_close_date"))
        p.mark("proposed", f"strategy check ({', '.join(t.kind for t in triggers)}): the agent proposed to SELL {round((d.fraction or 1) * 100)}% of its "
                           f"{p.symbol} (about ${p.usd:.2f})", now)
        state.proposals.append(p)
        check.ticker, check.usd, check.proposal_id = h["ticker"], p.usd, p.id
        if shadow:
            ex.shadow_fill(state, p, account=account)
            print(f"  shadow sale: {p.status}: {p.history[-1].note[:120]}")
        else:
            print(f"  PROPOSAL {p.id}: SELL {round((d.fraction or 1) * 100)}% of {p.symbol}. To approve:  python scripts\\fund_trade.py approve {p.id}")
        return check
    if d.action == "hold" or cand is None:
        p = Proposal(id=new_id(), created_at=now, mode=mode, side="hold", topic="", ticker="", symbol="", asset_id="", usd=0.0,
                     rationale=f"{d.what_changed} {d.rationale}".strip(), risks=d.risks, confidence=d.confidence, model=model, model_cost_usd=cost)
        p.mark("hold", "strategy check: " + ", ".join(t.kind for t in triggers), now)
        p.sha256 = fingerprint(p)
        state.proposals.append(p)
        check.proposal_id = p.id
        return check
    p = Proposal(id=new_id(), created_at=now, mode=mode, topic=cand.topic, ticker=cand.ticker, symbol=cand.symbol, asset_id=cand.asset_id, usd=float(d.usd),
                 rationale=f"{d.what_changed} {d.rationale}".strip(), risks=d.risks, confidence=d.confidence, model=model, model_cost_usd=cost,
                 ref_close=cand.last_close, ref_close_date=cand.last_close_date, dry_quote=cand.dry_quote)
    p.mark("proposed", f"strategy check ({', '.join(t.kind for t in triggers)}): the agent proposed to buy ${p.usd:.2f} of {p.symbol}", now)
    state.proposals.append(p)
    check.ticker, check.usd, check.proposal_id = cand.ticker, float(d.usd), p.id
    if shadow:
        ex.shadow_fill(state, p, account=account)
        print(f"  shadow: {p.status}: {p.history[-1].note[:120]}")
    else:
        print(f"  PROPOSAL {p.id}: buy ${p.usd:.2f} of {p.symbol}. To approve (sends money):  python scripts\\fund_trade.py approve {p.id}")
    return check


def near_price(ex) -> float:  # noqa: ANN001
    return ex.oneclick.price_usd(ex.cfg.near_asset_id)


_TOKEN_PRICES: dict = {}


def token_price(ex, symbol: str) -> float | None:  # noqa: ANN001
    """Live price of a tokenized stock from the public NEAR Intents token list (cached 10 minutes); None if unavailable."""
    import time
    if not _TOKEN_PRICES or time.time() - _TOKEN_PRICES.get("_at", 0) > 600:
        try:
            from app.fund.intents_signed import SignedIntents
            _TOKEN_PRICES.clear()
            _TOKEN_PRICES.update({str(t.get("symbol") or "").upper(): float(t["price"]) for t in SignedIntents(load_fund_config().intents.api).tokens() if t.get("price")})
            _TOKEN_PRICES["_at"] = time.time()
        except Exception:  # noqa: BLE001
            return None
    return _TOKEN_PRICES.get(symbol.upper())


def valued_holding(state, ex, h: dict, now: datetime | None = None) -> tuple[float, str]:  # noqa: ANN001
    """(USD value, how it was valued) of one live holding: a real dry sale quote when NEAR Intents answers (saved as the
    last known value); otherwise the last known quote, else what it cost. Owner 2026-11-10: a holding that cannot be
    quoted (Intents down) is not worth $0."""
    v = holding_value(ex, h)
    if v is not None:
        state.last_values[h["symbol"]] = {"usd": v, "at": (now or datetime.now(timezone.utc)).isoformat()}
        return v, "live quote"
    px = token_price(ex, h["symbol"])
    if px:                                             # the live NEAR Intents price (as near.com shows) when no swap quote exists
        return round(h["quantity"] * px, 2), "NEAR Intents price of the tokenized stock"
    last = state.last_values.get(h["symbol"])
    if last:
        return float(last["usd"]), f"last known quote ({str(last['at'])[:16]})"
    return round(float(h.get("cost_usd") or 0.0), 2), "what it cost (no quote yet)"


def live_fund_value(s, cfg, ex, private_near: float = 0.0) -> float:  # noqa: ANN001
    """Value of the live fund: its holdings at a real dry sale quote (or the last known value when NEAR Intents cannot
    quote), the NEAR in the trading wallet and, when known, the NEAR in its near.com (private) balance (read only after
    a signed login, i.e. in the owner's own loop)."""
    from app.fund.economy import account_near
    state = load_state(STATE)
    value = 0.0
    for h in state.live_holdings():
        v, how = valued_holding(state, ex, h)
        value += v
        if how != "live quote":
            print(f"  {h['symbol']}: no swap quote from NEAR Intents; valued at the {how}: ${v:.2f}")
    save_state(state, STATE)
    acc = (s.fund_mainnet_account_id or "").strip()
    if acc:
        liquid, _ = account_near(httpx.Client(timeout=30), cfg.live.rpc, acc)
        value += liquid / 1e24 * near_price(ex)
    value += private_near * near_price(ex)
    return round(value, 2)


def refresh_private_balance(s, cfg) -> float | None:  # noqa: ANN001
    """Read the near.com balance (signed login, owner's loop only) and save it for the website."""
    near = private_near_balance(s, cfg)
    if near is not None:
        st = load_state(STATE)
        st.private_near, st.private_checked_at = round(near, 4), datetime.now(timezone.utc)
        save_state(st, STATE)
    return near


def private_near_balance(s, cfg) -> float | None:  # noqa: ANN001
    """NEAR in the trading agent's near.com balance. Needs a signed login with the trading key: only call it in the
    owner's own loop (live.auto_approve) or from an owner command, never from a read-only check."""
    from app.fund.economy_pay import WNEAR
    from app.fund.signed_exec import held
    creds = s.fund_mainnet_credentials()
    if not creds or not s.oneclick_api_key:
        return None
    api = SignedIntents(cfg.intents.api, api_key=s.oneclick_api_key.get_secret_value().strip())
    token = api.login(creds[0], creds[1], str(rpc_view_salt(cfg)))["accessToken"]
    return held(api.balances(token), WNEAR) / 1e24


def economy_buy_reports(s, cfg, toks, cands, now, *, execute: bool, max_new: int | None = None,  # noqa: ANN001
                        only_actionable: bool = False) -> set:
    """Make sure the trading agent holds the reports behind its candidates: price each one (report agent) and, when
    `execute` (the owner's own loop with live.auto_approve, or `economy buy`), pay for it in NEAR. Returns the usable topics."""
    from app.fund.economy import (account_near, buy_report, load_economy, price_report, purchase_blocks, read_tx,
                                  report_budget_near, save_economy)
    from app.api.main import _default_store
    ec = cfg.economy
    ex = make_executor(s, cfg, with_signer=False)
    state = load_economy(ECONOMY)
    store = _default_store(s)
    px = near_price(ex)
    creds = s.fund_mainnet_credentials()
    buyer = creds[0] if creds else (s.fund_mainnet_account_id or "").strip()
    usable: set = set()
    priv = 0.0
    if execute and ec.pay_from == "private":
        try:
            priv = refresh_private_balance(s, cfg) or 0.0
            print(f"  near.com balance: {priv:.3f} NEAR (counted in the fund's value)")
        except Exception as exc:  # noqa: BLE001
            print(f"  near.com balance not readable ({str(exc)[:100]}); the fund is valued without it")
    want = sorted({c.topic: c for c in cands}.values(), key=lambda c: -(c.score or 0))     # best-scored reports first
    new_bought = 0
    for c in want:
        rid = next((t.get("run_id") for t in toks if t["topic"] == c.topic and t.get("run_id")), None)
        if not rid:
            continue
        if state.bought(rid):
            usable.add(c.topic)
            continue
        if only_actionable:
            # owner 2026-11-11: buy a report only when the agent could act on it now: a stock from it is rated
            # 'strong' or 'building' AND NEAR Intents quotes it (the 6G report, rated 'early', was bought for nothing)
            mine = [x for x in cands if x.topic == c.topic]
            if not any(x.verdict_band in ("strong", "building") and x.quotable for x in mine):
                why = ("rated '" + str(c.verdict_band) + "'" if all(x.verdict_band not in ("strong", "building") for x in mine)
                       else "NEAR Intents cannot quote its stocks right now")
                print(f"  report '{c.topic}': not bought ({why}; nothing the agent could trade from it now)")
                continue
        found = store.get(rid)
        if not found:
            continue
        rep = found[0]
        score = rep.investment.score.score if rep.investment and rep.investment.score else None
        conf = getattr(rep.investment.score.confidence, "value", None) if rep.investment and rep.investment.score else None
        searches = int(((rep.patent.source_usage or {}).get("requests") or 0) if rep.patent else 0)
        price = price_report(run_id=rid, topic=c.topic, cost_usd=rep.total_cost_usd or 0.0, score=score,
                             confidence_pct=c.confidence_pct, near_usd=px, cfg=ec, now=now, patent_searches=searches)
        state.prices[rid] = price
        budget = report_budget_near(fund_value_usd=live_fund_value(s, cfg, ex, priv), near_usd=px, state=state, cfg=ec)
        private = ec.pay_from == "private"
        wallet = None if private else (account_near(httpx.Client(timeout=30), cfg.live.rpc, buyer)[0] / 1e24 if buyer else 0.0)
        blocks = purchase_blocks(state=state, price=price, budget_near=budget, wallet_near=wallet, cfg=ec,
                                 trading_enabled=cfg.live.trading_enabled, kill_switch=ex.kill_switch())
        if not creds:
            blocks.append("FUND_MAINNET_ACCOUNT_ID / FUND_MAINNET_PRIVATE_KEY are not set")
        if private and not cfg.live.signed_route_enabled:
            blocks.append("paying from the near.com balance needs live.signed_route_enabled")
        if private and not s.oneclick_api_key:
            blocks.append("ONECLICK_API_KEY is not set (the private route needs the partner key)")
        print(f"  report '{c.topic}': {price.price_near:g} NEAR (${price.price_usd:.2f}); budget left {budget:.3f} NEAR")
        if max_new is not None and new_bought >= max_new:
            blocks.append(f"the owner limited this run to {max_new} new report(s) (--max)")
        if blocks:
            print("    not bought: " + "; ".join(blocks))
            continue
        if not execute:
            print("    would buy it; real payments run in the owner's loop (live.auto_approve) or with:  python scripts\\fund_trade.py economy buy")
            continue
        if private:
            from app.fund.economy_pay import pay_from_private, seller_total_reader
            api_key = s.oneclick_api_key.get_secret_value().strip()
            http = httpx.Client(timeout=40)
            try:
                p = pay_from_private(state=state, path=ECONOMY, price=price, account=creds[0], private_key=creds[1], cfg=ec,
                                     api=SignedIntents(cfg.intents.api, api_key=api_key), salt_reader=lambda: str(rpc_view_salt(cfg)),
                                     submit=lambda order, key: submit_signed_order(http, cfg.intents.api, api_key, order, key),
                                     allowed_recipients=cfg.live.order_recipients,
                                     read_seller_total=seller_total_reader(httpx.Client(timeout=30), ec.rpc, ec.seller_account),
                                     now=lambda: datetime.now(timezone.utc))
            except RuntimeError as exc:
                print(f"    not bought: {str(exc)[:240]}")
                continue
        else:
            signer = MainnetSigner(creds[0], creds[1], cfg.live.rpc)
            p = buy_report(state=state, path=ECONOMY, price=price, buyer=creds[0], cfg=ec, send=signer.transfer,
                           read=lambda h, who: read_tx(httpx.Client(timeout=60), ec.rpc, h, who), now=now)
        print(f"    bought: {p.status} (tx {p.tx_hash}) {p.note}")
        if p.status in ("paid", "sending"):
            new_bought += 1
        if p.status == "paid":
            usable.add(c.topic)
    save_economy(state, ECONOMY)
    if execute and ec.pay_from == "private" and any(p.status == "paid" for p in state.purchases if p.at >= now):
        try:
            refresh_private_balance(s, cfg)          # the website shows the balance after these payments, not before
        except Exception as exc:  # noqa: BLE001
            print(f"  near.com balance not re-read after paying: {str(exc)[:100]}")
    return usable


def cmd_record_sale(s, cfg, symbol: str, near_received: float | None, why: str) -> int:  # noqa: ANN001
    """Record a sale the OWNER made by hand in near.com, so the records and the website match the real holdings.
    It is labelled as the owner's action, never as an agent decision. Without --near the amount is estimated from a
    real dry sale quote and labelled as an estimate (the owner's near.com history has the exact figure)."""
    state = load_state(STATE)
    h = next((x for x in state.live_holdings() if x["symbol"].upper() == symbol.upper()), None)
    if h is None:
        print(f"the live fund holds no {symbol} according to its records")
        return 1
    ex = make_executor(s, cfg, with_signer=False)
    px = near_price(ex)
    value = holding_value(ex, h)
    if near_received is not None:
        near_amt, usd, how = near_received, round(near_received * px, 2), "amount given by the owner from near.com"
    else:
        usd = value or 0.0
        near_amt, how = round(usd / px, 6) if px else 0.0, "amount ESTIMATED from a dry sale quote when recorded (near.com has the exact figure)"
    now = datetime.now(timezone.utc)
    p = Proposal(id=new_id(), created_at=now, mode="live", side="sell", topic=h["topic"], ticker=h["ticker"], symbol=h["symbol"],
                 asset_id=h["asset_id"], usd=usd, fraction=1.0, quantity=h["quantity"],
                 rationale=f"Sold by the owner by hand in near.com, not by the trading agent: {why}",
                 risks=[], confidence="low", model=None)
    rec = {"amountInFormatted": str(h["quantity"]), "amountOutFormatted": str(near_amt), "amountOutUsd": str(usd), "route": "manual"}
    p.quote = dict(rec)
    p.result = {**rec, "status": "SUCCESS (manual sale by the owner in near.com; recorded by hand)", "amounts_are": how}
    p.mark("approved", "manual sale by the owner in near.com (no agent decision, no code checks)", now)
    p.mark("success", f"recorded by hand: all {h['quantity']} {h['symbol']} sold for about {near_amt:g} NEAR (${usd:.2f}); {how}", now)
    p.sha256 = fingerprint(p)
    state.proposals.append(p)
    save_state(state, STATE)
    seal(s, p)
    save_state(state, STATE)
    print(f"recorded: owner sold {h['quantity']} {h['symbol']} for about {near_amt:g} NEAR (${usd:.2f}); {how}")
    return 0


def cmd_economy(s, cfg, what: str, max_new: int | None = None) -> int:  # noqa: ANN001
    """economy status | price | buy | stake"""
    from app.fund.economy import (YOCTO, account_near, load_economy, save_economy, stake, stake_amount_yocto,
                                  staked_amount)
    ec = cfg.economy
    ex = make_executor(s, cfg, with_signer=False)
    now = datetime.now(timezone.utc)
    if what in ("price", "buy"):
        toks = tradable_tokens()
        cands = [Candidate(ticker=t["ticker"], symbol=t["symbol"], asset_id=t["asset_id"], topic=t["topic"], verdict_band=t["band"],
                           score=t["score"], confidence_pct=t.get("confidence_pct")) for t in toks]
        if what == "buy" and not ec.enabled:
            print("economy.enabled is false in config/funds.yaml: nothing is bought")
            return 1
        usable = economy_buy_reports(s, cfg, toks, cands, now, execute=(what == "buy"), max_new=max_new)
        print(f"reports the trading agent may use: {len(usable)} topic(s)")
        return 0
    if what == "stake":
        creds = s.report_agent_credentials()
        if not ec.enabled or not creds or not ec.staking_contract:
            print("cannot stake: needs economy.enabled, economy.staking_contract and REPORT_AGENT_ACCOUNT_ID / _PRIVATE_KEY in .env")
            return 1
        if creds[0] != ec.seller_account:
            print(f"REPORT_AGENT_ACCOUNT_ID ({creds[0]}) is not economy.seller_account ({ec.seller_account}); nothing staked")
            return 1
        from app.fund.economy_pay import wnear_balance
        signer = MainnetSigner(creds[0], creds[1], ec.rpc)
        wrapped = wnear_balance(httpx.Client(timeout=30), ec.rpc, creds[0])
        if wrapped > 0:                                   # a payment from the near.com balance may arrive as wNEAR: unwrap it first
            tx = signer.call("wrap.near", "near_withdraw", {"amount": str(wrapped)}, 10 * 10 ** 12, 1)
            print(f"unwrapped {wrapped / YOCTO:.4f} wNEAR into NEAR (tx {tx})")
        liquid, _ = account_near(httpx.Client(timeout=30), ec.rpc, creds[0])
        st0 = load_economy(ECONOMY)
        # Agent Market fees join the same split (owner 2026-11-11); the report agent records them, maybe on another machine
        from app import market_income
        fees = market_income.best(service.RUNS_DIR / market_income.FILE, service.BACKEND_DIR / "site_data" / market_income.FILE)
        extra = fees.near()
        if extra:
            print(f"Agent Market fees counted as received: ${fees.usd():.2f} = {extra:g} NEAR ({len(fees.fees)} hire(s))")
        if stake_amount_yocto(liquid, ec, st0, extra) is None:
            owed = (st0.received_near() + extra) * ec.stake_share - st0.staked_near()
            print(f"nothing to stake: {ec.stake_share:.0%} of the {st0.received_near() + extra:g} NEAR received for reports, minus "
                  f"{st0.staked_near():g} NEAR already staked, is {max(0.0, owed):.3f} NEAR (minimum {ec.min_stake_near} NEAR; "
                  f"wallet {liquid / YOCTO:.3f} NEAR, {ec.stake_reserve_near} NEAR always kept for gas). Other NEAR in the wallet is never staked.")
            return 0
        state = load_economy(ECONOMY)
        ev = stake(state=state, path=ECONOMY, account=creds[0], balance_yocto=liquid, cfg=ec, call=signer.call, now=now,
                   extra_received_near=extra)
        print(f"{ev.status}: {ev.note} (tx {ev.tx_hash})")
        return 0 if ev.status == "staked" else 1
    state = load_economy(ECONOMY)
    seller = ec.seller_account
    print(f"agent economy: {'ON' if ec.enabled else 'off (economy.enabled is false)'}; report agent {seller or '-'}; "
          f"staking contract {ec.staking_contract or '- (not set)'}")
    try:
        px = near_price(ex)
        tst = load_state(STATE)
        snap = tst.private_near or 0.0
        if tst.private_near is not None:
            print(f"near.com balance {snap:g} NEAR as last read {str(tst.private_checked_at)[:16]} (re-read by economy buy)")
        val = live_fund_value(s, cfg, ex, snap)
        from app.fund.economy import report_budget_near
        print(f"NEAR ${px:.2f}; live fund worth about ${val:.2f}; report budget {ec.budget_share_of_fund:.0%} = "
              f"{ec.budget_share_of_fund * val / px:.3f} NEAR, spent {state.spent_near():g} NEAR, left "
              f"{report_budget_near(fund_value_usd=val, near_usd=px, state=state, cfg=ec):.3f} NEAR")
    except Exception as exc:  # noqa: BLE001
        print(f"(prices unavailable: {str(exc)[:100]})")
    if seller:
        liquid, locked = account_near(httpx.Client(timeout=30), ec.rpc, seller)
        st = staked_amount(httpx.Client(timeout=30), ec, seller)
        print(f"report agent wallet: {liquid / YOCTO:.3f} NEAR; staked: {('%.3f NEAR' % (st / YOCTO)) if st is not None else 'n/a'}")
    for p in state.purchases[-10:]:
        print(f"  bought {p.topic[:30]:30} {p.price_near:g} NEAR  {p.status:8} tx {p.tx_hash}")
    for e in state.stakes[-5:]:
        print(f"  staked {e.amount_near:g} NEAR into {e.contract}: {e.status} (tx {e.tx_hash})")
    save_economy(state, ECONOMY)
    return 0


def evidence_context(s, toks) -> dict:  # noqa: ANN001
    """Per topic: the latest sealed report's verdict and its dated X / market findings (claims with labels). Read-only."""
    from app.api.main import _default_store
    from app.report.verdict import build_verdict
    store = _default_store(s)
    out: dict = {}
    for t in toks:
        if t["topic"] in out or not t.get("run_id"):
            continue
        found = store.get(t["run_id"])
        if not found:
            continue
        report = found[0]
        v = build_verdict(report)
        items = []
        for group, res in (("x", report.x), ("market", report.market)):
            for f in (res.findings if res else [])[:6]:
                items.append({"from": group, "label": f.label.value, "date": report.generated_at.date().isoformat(), "claim": f.claim[:240]})
        out[t["topic"]] = {"report_date": report.generated_at.date().isoformat(), "verdict": v.get("band"), "score": v.get("score"),
                           "confidence_pct": v.get("confidence_pct"), "findings": items[:10]}
    return out


def seal(s, p: Proposal) -> None:  # noqa: ANN001
    """Seal a trade record's fingerprint on NEAR, only when the owner switched it on (SEAL_TRADES=true). By default
    only reports are sealed (owner 2026-11-11); the record keeps its own fingerprint either way."""
    if not getattr(s, "seal_trades", False):
        return
    from app.chain.near_record import make_recorder
    try:
        recorder = make_recorder(s)
    except NearRecordError as exc:
        print(f"  (record not sealed: {str(exc)[:100]})")
        return
    if recorder is None or not p.sha256:
        return
    try:
        p.chain = recorder.record_fund_decision(f"trade_{p.id}", {"sha256": p.sha256, "status": p.status, "symbol": p.symbol,
                                                                              "usd": str(p.usd), "mode": p.mode}).as_dict()
        print(f"  record fingerprint sealed on NEAR {p.chain.get('network', '')}")
    except NearRecordError as exc:
        print(f"  (record not sealed: {str(exc)[:100]})")


def rpc_view_salt(cfg):  # noqa: ANN001,ANN201
    from app.fund.live import rpc_view
    return rpc_view(httpx.Client(timeout=30), cfg.live.rpc, cfg.live.intents_contract, "current_salt", {})


def cmd_approve(s, cfg, pid: str, *, auto: bool = False) -> int:  # noqa: ANN001
    """auto=True is used only by the strategy loop when live.auto_approve is true in config/funds.yaml (owner-only switch)."""
    if auto and not cfg.live.auto_approve:
        raise RuntimeError("auto approval requested but live.auto_approve is false")
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
    if p.side == "sell" and not signed_route:
        blocked.append("sales run only on the private signed route (live.route: confidential): the stocks are in the private balance")
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
    if p.side == "sell":
        print(f"REAL MONEY. About to SELL {round((p.fraction or 1) * 100)}% of the {p.symbol} in {source} of {creds[0]} (NEAR mainnet) "
              f"for NEAR (about ${p.usd:.2f}).")
    else:
        print(f"REAL MONEY. About to pay ${p.usd:.2f} of {coin} from {source} of {creds[0]} (NEAR mainnet) to buy {p.symbol}.")
    print(f"  agent's reason: {p.rationale}")
    if auto:
        p.mark("approved", "approved AUTOMATICALLY: live.auto_approve is on (owner's setting); all code checks passed", datetime.now(timezone.utc))
    else:
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
    ap.add_argument("command", choices=["status", "propose", "list", "approve", "reject", "resume", "confirm", "refunded", "stop", "start", "register-usdc", "check", "rules", "watch", "pending", "holdings", "economy", "record-sale", "balance"])
    ap.add_argument("--near", type=float, help="with record-sale: NEAR the owner received (from near.com); else estimated")
    ap.add_argument("--why", default="to pay for research reports (the agent economy)", help="with record-sale: the owner's reason")
    ap.add_argument("--review", action="store_true", help="with check: an extra full keep / sell / buy review now, outside the hourly schedule")
    ap.add_argument("id", nargs="?")
    ap.add_argument("--shadow", action="store_true")
    ap.add_argument("--usd", type=float)
    ap.add_argument("--max", type=int, help="with economy buy: buy at most this many new reports (best-scored first)")
    ap.add_argument("--publish", action="store_true", help="with watch: export, commit and git push backend/site_data after a trade, a report purchase or a stake")
    ap.add_argument("--loop", action="store_true", help="with check: run forever, one check every strategy.check_minutes")
    args = ap.parse_args()
    s, cfg = get_settings(), load_fund_config()
    STATE.parent.mkdir(parents=True, exist_ok=True)
    stop = STATE.with_name("STOP")
    if args.command == "status":
        return cmd_status(s, cfg)
    if args.command == "propose":
        return cmd_propose(s, cfg, args.shadow, args.usd)
    if args.command == "check":
        if args.review:
            return run_check(s, cfg, args.shadow, extra=[Trigger(kind="manual", detail="an extra full review, outside the hourly schedule: keep, sell (part of) a holding, or buy")])
        return cmd_check(s, cfg, args.shadow, args.loop)
    if args.command == "balance":
        near = refresh_private_balance(s, cfg)
        print("near.com balance: " + (f"{near:.4f} NEAR (saved for the website)" if near is not None else "not readable (keys missing)"))
        return 0
    if args.command == "record-sale":
        if not args.id:
            print("usage: fund_trade.py record-sale <SYMBOL> [--near X] [--why ...]")
            return 1
        return cmd_record_sale(s, cfg, args.id, args.near, args.why)
    if args.command == "economy":
        return cmd_economy(s, cfg, args.id or "status", args.max)
    if args.command == "holdings":
        rows = load_state(STATE).live_holdings()
        if not rows:
            print("the live fund holds nothing according to its records")
        for h in rows:
            print(f"  {h['symbol']:8} {h['quantity']:.8f}  cost ${h['cost_usd']:.2f}  ({h['topic']}; first bought {h['first_bought'][:16]})")
        st = load_state(STATE)
        print(f"spent on buys ${st.spent('live'):.2f}; sale proceeds ${st.proceeds('live'):.2f}; counted against the total cap "
              f"(budget_mode {cfg.live.budget_mode}): ${st.invested('live', cfg.live.budget_mode):.2f} of ${cfg.live.max_total_usd:.2f}")
        return 0
    if args.command == "watch":
        return cmd_watch(s, cfg, args.publish)
    if args.command == "pending":
        return cmd_pending(s, cfg)
    if args.command == "rules":
        for r in RULES:
            print("-", r)
        return 0
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

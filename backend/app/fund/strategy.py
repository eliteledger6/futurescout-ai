"""Trading strategy: WHEN the trading agent wakes up, and the fixed rules it must follow when it does.

Owner request 2026-11-10: the agent should not wait for a manual `propose`. It should react to (1) a new sealed
report for a topic it trades, (2) a large one-day price move in a stock it holds or may buy, and (3) a periodic
review, then "check the reason" and decide.

What "check the reason" can honestly mean here: the agent is given the latest report's verdict, score and
confidence for the topic, the X-signal and market findings that report already contains (dated, labelled), the
price move itself, and what it already holds. It does NOT browse the news; when the evidence it has does not
explain a move, it must say so and prefer holding.

Everything that moves money stays as before: in live mode a decision becomes a PROPOSAL the owner approves in the
terminal; in shadow mode (pretend money, real quotes) it is filled automatically so the strategy can be watched
without risk. Every check is recorded with its triggers and the agent's reasoning, and the record is fingerprinted.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.agents.trader.agent import AGENT, Candidate
from app.models.router import ModelRouter, ModelRouterError

STRATEGY_VERSION = 2          # 2026-11-10: the agent may also SELL (owner's written yes), under the rules below
_PROMPT_PATH = Path(__file__).resolve().parents[1] / "agents" / "trader" / "prompt_strategy.md"


class StrategyConfig(BaseModel):
    check_minutes: int = 60              # how often `fund_trade.py check --loop` looks
    review_hours: int = 24               # a routine review even when nothing moved
    drop_pct: float = 7.0                # one-day fall that wakes the agent
    jump_pct: float = 10.0               # one-day rise that wakes the agent (it must not chase)
    min_confidence_pct: float = 45.0     # reports below this are "low confidence": no new buys; 0 = no minimum, the agent weighs it
    max_adds_per_ticker: int = 2         # buying the dip is allowed at most this many times per ticker
    max_ticker_share_pct: float = 25.0   # shadow mode: one company may not exceed this share of the budget
    price_requests_per_check: int = 6    # Alpha Vantage calls allowed per check (free plan: 25 a day)
    min_hold_hours: float = 24.0         # a holding is not sold before it was held this long (no churning)
    min_sell_fraction: float = 0.25      # a sale is at least this share of the holding (smaller sales cost more than they move)


class Trigger(BaseModel):
    kind: Literal["new_report", "price_drop", "price_jump", "review", "manual", "after_sale"]
    ticker: str = ""
    topic: str = ""
    detail: str = ""


class Check(BaseModel):
    """One wake-up of the trading agent: why it woke, what it saw, what it decided."""
    id: str
    at: datetime
    mode: str                                    # live | shadow
    triggers: list[Trigger] = Field(default_factory=list)
    action: str = "hold"                         # buy | sell | hold | none (no trigger, agent not called)
    ticker: str = ""
    usd: float = 0.0
    summary: str = ""
    what_changed: str = ""
    proposal_id: Optional[str] = None
    model: Optional[str] = None
    cost_usd: float = 0.0
    notes: list[str] = Field(default_factory=list)
    sha256: Optional[str] = None
    correction: Optional[str] = None             # a later, clearly marked correction of the wording (not part of the fingerprint)


class StrategyDecision(BaseModel):
    """What the model returns. Code checks every field before anything happens."""
    action: Literal["buy", "sell", "hold"]
    ticker: Optional[str] = None
    usd: Optional[float] = None
    fraction: Optional[float] = None             # sell: share of the holding to sell
    what_changed: str = ""                       # the agent's reading of the trigger: what the evidence says about it
    rationale: str = ""
    risks: list[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "low"


RULES = [
    "Wake on: a new sealed report for a traded topic; a one-day move beyond the thresholds in a held or allowed stock; a routine review.",
    "Buy only companies named by the research evidence (patents or papers), from reports with verdict 'strong' or 'building'; the agent weighs each report's confidence itself (code enforces a minimum only when the owner sets one).",
    "On a sharp fall: if the latest report and its findings still support the company and nothing in them explains the fall, the agent may add once more at the lower price (at most the allowed number of adds); if the report weakened or the findings explain the fall, hold.",
    "On a sharp rise: never chase; hold and note it.",
    "Size follows confidence: less confident reports get smaller orders; in live mode the size is fixed by the caps.",
    "Diversify: in shadow mode one company stays under the share cap; keeping cash is allowed and must be explained.",
    "Sell only a holding kept at least the minimum time, and only when its report weakened (verdict below 'building', or below the "
    "confidence minimum when the owner sets one), when the evidence explains a fall as a real problem, or to rotate into a clearly better-evidenced candidate "
    "when there is no cash; never sell in panic on a fall the evidence does not explain. Selling is the owner's switch (live.sells_enabled).",
    "After a sale the agent is woken once more at once and may buy with the money (live: only if the owner counts the budget net of sales).",
    "Every wake-up is recorded with its triggers and reasoning, and the record is fingerprinted.",
]


def price_vs_close(c) -> dict:  # noqa: ANN001
    """The quoted price per token (from the real dry quote) and how far it is from the stock's last close, for the agent."""
    q = c.dry_quote or {}
    try:
        per_token = float(q["amountInUsd"]) / float(q["amountOutFormatted"])
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return {"quoted_price_per_token": None, "gap_vs_last_close_pct": None}
    gap = round((per_token / c.last_close - 1) * 100, 2) if c.last_close else None
    return {"quoted_price_per_token": round(per_token, 2), "gap_vs_last_close_pct": gap}


def price_line(price_band_pct: float) -> str:
    """What the agent is told about the price it would pay (owner 2026-11-11: no band in code; the agent takes that risk)."""
    if price_band_pct > 0:
        return (f"Code refuses a trade whose quoted price is more than {price_band_pct:.0f}% from the stock's last close "
                "(a little more when the close is older).")
    return ("No price band in code: for every candidate compare quoted_price_per_token with last_close (gap_vs_last_close_pct; the "
            "close may be a day or more old, and a tokenized stock can trade at a premium or discount). Decide yourself whether the "
            "price is acceptable, say so in your reasoning, and take that risk; a sale is filled at the quoted price too.")


# How each wake-up reason is named to the agent (and so in its reasoning). "manual" is only the internal name of an
# extra review started from the command line; it is not a person's decision.
TRIGGER_NAMES = {"new_report": "new report", "price_drop": "sharp fall", "price_jump": "sharp rise", "review": "daily review",
                 "manual": "extra review", "after_sale": "after a sale"}


def confidence_line(cfg) -> str:  # noqa: ANN001
    """What the agent is told about report confidence (owner 2026-11-11: no fixed minimum; the agent judges it)."""
    if cfg.min_confidence_pct > 0:
        return f"Minimum report confidence for a new buy: {cfg.min_confidence_pct:.0f}%."
    return ("No minimum report confidence: weigh each report's confidence yourself (below 70% is not confident), say how it "
            "shaped your choice, and size a buy smaller when the evidence is thinner.")


# ------------------------------------------------------------------ triggers (pure code)
def detect_triggers(*, tokens: list[dict], seen_runs: dict[str, str], closes: dict[str, tuple[str, float, Optional[float]]],
                    seen_closes: dict[str, str], last_check: Optional[datetime], now: datetime, cfg: StrategyConfig,
                    held: set[str]) -> list[Trigger]:
    """tokens: allowlist rows (ticker, topic, run_id...). closes: ticker -> (date, close, previous close).
    seen_runs / seen_closes: what earlier checks already reacted to (topic -> run_id, ticker -> close date)."""
    out: list[Trigger] = []
    for t in tokens:
        rid = t.get("run_id")
        if rid and seen_runs.get(t["topic"]) != rid:
            out.append(Trigger(kind="new_report", ticker=t["ticker"], topic=t["topic"],
                               detail=f"report {rid[:8]} for '{t['topic']}' not yet considered (verdict {t.get('band')}, score {t.get('score')}, "
                                      f"confidence {t.get('confidence_pct')}%)"))
    for ticker, (day, close, prev) in closes.items():
        if not prev or seen_closes.get(ticker) == day:
            continue
        pct = (close / prev - 1) * 100
        where = "held" if ticker in held else "allowed"
        if pct <= -cfg.drop_pct:
            out.append(Trigger(kind="price_drop", ticker=ticker, detail=f"{ticker} ({where}) closed {pct:+.1f}% on {day} at ${close:.2f} (previous ${prev:.2f})"))
        elif pct >= cfg.jump_pct:
            out.append(Trigger(kind="price_jump", ticker=ticker, detail=f"{ticker} ({where}) closed {pct:+.1f}% on {day} at ${close:.2f} (previous ${prev:.2f})"))
    if last_check is None or now - last_check >= timedelta(hours=cfg.review_hours):
        out.append(Trigger(kind="review", detail="routine review" if last_check else "first review"))
    return out


# ------------------------------------------------------------------ the agent, with the strategy
def assess(router: ModelRouter, *, triggers: list[Trigger], candidates: list[Candidate], holdings: list[dict], context: dict,
           budget_usd: float, fixed_usd: Optional[float], cfg: StrategyConfig, adds_so_far: dict[str, int],
           sellable: Optional[list[dict]] = None, sells_enabled: bool = False, can_buy: bool = True,
           sells_left_today: int = 0, min_sale_usd: float = 0.0,
           price_band_pct: float = 0.0) -> tuple[StrategyDecision, "Optional[Candidate | dict]", Optional[str], float, list[str]]:
    """Returns (decision, target, model alias, cost, notes). target: the Candidate to buy, or the holding (dict) to sell.
    `fixed_usd` is set in live mode (size fixed by the caps). `sellable`: holdings with ticker, symbol, asset_id, quantity,
    value_usd, held_hours, report verdict and confidence."""
    notes: list[str] = []
    sellable = sellable or []
    quotable = [c for c in candidates if c.quotable]
    listing = [{"ticker": c.ticker, "token": c.symbol, "topic": c.topic, "report_verdict": c.verdict_band, "report_score": c.score,
                "report_confidence_pct": c.confidence_pct, "company_size_risk": c.tier, "why_in_fund": c.why, "price_stretch": c.price_stretch or "unknown",
                "last_close": c.last_close, "last_close_date": c.last_close_date, "quotable": c.quotable, "quote_cost_pct": c.quote_cost_pct,
                **price_vs_close(c),
                "adds_so_far": adds_so_far.get(c.ticker.upper(), 0)} for c in candidates]
    size_line = (f"Trade size is FIXED at ${fixed_usd:.2f} (live mode)." if fixed_usd else
                 f"Pretend budget available: ${budget_usd:,.2f}; one company may not exceed {cfg.max_ticker_share_pct:.0f}% of the whole budget.")
    if not can_buy:
        size_line = "NO CASH for a buy right now: you may only SELL (to free money for a better candidate) or HOLD."
    sell_line = (f"SELLING is allowed: up to {sells_left_today} sale(s) left today; a holding must have been held at least {cfg.min_hold_hours:.0f} h; "
                 f"sell a share of a holding (`fraction`, {cfg.min_sell_fraction} to 1); the market's minimum trade is ${min_sale_usd:.2f}." if sells_enabled and sells_left_today > 0
                 else "SELLING is not available now (switched off by the owner or today's sales used up): buy or hold.")
    user = (f"WHY YOU WOKE UP:\n" + "\n".join(f"- {TRIGGER_NAMES.get(t.kind, t.kind)}: {t.detail}" for t in triggers) + "\n\n"
            f"{size_line}\n{sell_line}\n{confidence_line(cfg)} {price_line(price_band_pct)} Max adds per ticker: {cfg.max_adds_per_ticker}.\n\n"
            f"WHAT YOU ALREADY HOLD:\n{json.dumps(holdings)}\n\n"
            f"HOLDINGS YOU COULD SELL (with their latest report):\n{json.dumps(sellable, indent=1)}\n\n"
            f"LATEST EVIDENCE PER TOPIC (from the sealed reports; dated, labelled; nothing else was read):\n{json.dumps(context, indent=1)}\n\n"
            f"CANDIDATES:\n{json.dumps(listing, indent=1)}")
    messages = [{"role": "system", "content": _PROMPT_PATH.read_text(encoding="utf-8")}, {"role": "user", "content": user}]
    try:
        reply = router.complete(AGENT, messages, response_model=StrategyDecision)
    except ModelRouterError as exc:
        return StrategyDecision(action="hold", rationale="The trading model did not answer; nothing is done.", what_changed=""), None, None, 0.0, [f"model error: {str(exc)[:160]}"]
    d: StrategyDecision = reply.parsed  # type: ignore[assignment]
    cost = round(sum(u.get("cost_usd", 0.0) for u in router.usage_summary() if u.get("agent") == AGENT), 6)
    if d.confidence == "high":
        d.confidence = "medium"
        notes.append("confidence capped at medium (small test, thin evidence)")
    if d.action == "hold":
        return d, None, reply.llm_alias, cost, notes
    if d.action == "sell":
        def no(why: str):  # noqa: ANN202
            notes.append(f"sale of '{d.ticker}' refused by code: {why}; turned into hold")
            d.action, d.ticker, d.usd, d.fraction = "hold", None, None, None
            return d, None, reply.llm_alias, cost, notes
        h = next((x for x in sellable if str(x.get("ticker", "")).upper() == (d.ticker or "").upper()), None)
        if not sells_enabled:
            return no("selling is switched off")
        if sells_left_today <= 0:
            return no("no sales left today")
        if h is None:
            return no("not a holding")
        if float(h.get("held_hours") or 0) < cfg.min_hold_hours:
            return no(f"held only {float(h.get('held_hours') or 0):.0f} h (minimum {cfg.min_hold_hours:.0f} h)")
        frac = d.fraction if d.fraction and d.fraction > 0 else 1.0
        if frac > 1:
            notes.append(f"share {frac} capped at the whole holding")
            frac = 1.0
        if frac < cfg.min_sell_fraction:
            notes.append(f"share {frac} raised to the minimum {cfg.min_sell_fraction}")
            frac = cfg.min_sell_fraction
        if h.get("value_usd") is None:
            return no("the holding's current value could not be quoted")
        value = float(h.get("value_usd") or 0)
        if min_sale_usd and value * frac < min_sale_usd:
            if value < min_sale_usd:
                return no(f"the whole holding is worth about ${value:.2f}, below the market's minimum trade ${min_sale_usd:.2f}")
            notes.append(f"share {frac} raised to {min(1.0, min_sale_usd / value):.2f} so the sale reaches the market's minimum ${min_sale_usd:.2f}")
            frac = min(1.0, min_sale_usd * 1.02 / value)
        d.ticker, d.fraction = h["ticker"], round(min(1.0, frac), 4)
        d.usd = round(value * d.fraction, 2) or None
        return d, h, reply.llm_alias, cost, notes
    if not can_buy:
        notes.append(f"buy of '{d.ticker}' refused by code: no cash (sell first); turned into hold")
        d.action, d.ticker, d.usd = "hold", None, None
        return d, None, reply.llm_alias, cost, notes
    cand = next((c for c in quotable if c.ticker.upper() == (d.ticker or "").upper()), None)
    if cand is None:
        notes.append(f"buy of '{d.ticker}' refused by code: not a quotable candidate; turned into hold")
        d.action, d.ticker, d.usd = "hold", None, None
        return d, None, reply.llm_alias, cost, notes
    if cfg.min_confidence_pct > 0 and (cand.confidence_pct or 0) < cfg.min_confidence_pct:
        notes.append(f"buy of {cand.ticker} refused by code: report confidence {cand.confidence_pct}% is below {cfg.min_confidence_pct:.0f}%; turned into hold")
        d.action, d.ticker, d.usd = "hold", None, None
        return d, None, reply.llm_alias, cost, notes
    if (cand.verdict_band or "") not in ("strong", "building"):
        notes.append(f"buy of {cand.ticker} refused by code: verdict '{cand.verdict_band}' is not strong or building; turned into hold")
        d.action, d.ticker, d.usd = "hold", None, None
        return d, None, reply.llm_alias, cost, notes
    if adds_so_far.get(cand.ticker.upper(), 0) >= cfg.max_adds_per_ticker and any(t.kind == "price_drop" for t in triggers):
        notes.append(f"buy of {cand.ticker} refused by code: already added {cfg.max_adds_per_ticker} time(s) on dips; turned into hold")
        d.action, d.ticker, d.usd = "hold", None, None
        return d, None, reply.llm_alias, cost, notes
    if fixed_usd:
        if d.usd != fixed_usd:
            notes.append(f"size set to the fixed ${fixed_usd:.2f} (the model said {d.usd})")
        d.usd = fixed_usd
    else:
        cap = cfg.max_ticker_share_pct / 100 * (budget_usd + sum(float(h.get("cost_usd", 0)) for h in holdings))
        held_cost = sum(float(h.get("cost_usd", 0)) for h in holdings if str(h.get("ticker", "")).upper() == cand.ticker.upper())
        room = max(0.0, min(budget_usd, cap - held_cost))
        if not d.usd or d.usd <= 0:
            notes.append("no positive size from the model; turned into hold")
            d.action, d.ticker, d.usd = "hold", None, None
            return d, None, reply.llm_alias, cost, notes
        if d.usd > room:
            notes.append(f"size cut from ${d.usd:,.2f} to ${room:,.2f} (budget and {cfg.max_ticker_share_pct:.0f}% share cap)")
            d.usd = round(room, 2)
        if d.usd < 1:
            notes.append("no room left under the share cap; turned into hold")
            d.action, d.ticker, d.usd = "hold", None, None
            return d, None, reply.llm_alias, cost, notes
    d.ticker = cand.ticker
    return d, cand, reply.llm_alias, cost, notes

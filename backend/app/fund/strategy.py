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

STRATEGY_VERSION = 1
_PROMPT_PATH = Path(__file__).resolve().parents[1] / "agents" / "trader" / "prompt_strategy.md"


class StrategyConfig(BaseModel):
    check_minutes: int = 60              # how often `fund_trade.py check --loop` looks
    review_hours: int = 24               # a routine review even when nothing moved
    drop_pct: float = 7.0                # one-day fall that wakes the agent
    jump_pct: float = 10.0               # one-day rise that wakes the agent (it must not chase)
    min_confidence_pct: float = 45.0     # reports below this are "low confidence": no new buys
    max_adds_per_ticker: int = 2         # buying the dip is allowed at most this many times per ticker
    max_ticker_share_pct: float = 25.0   # shadow mode: one company may not exceed this share of the budget
    price_requests_per_check: int = 6    # Alpha Vantage calls allowed per check (free plan: 25 a day)


class Trigger(BaseModel):
    kind: Literal["new_report", "price_drop", "price_jump", "review", "manual"]
    ticker: str = ""
    topic: str = ""
    detail: str = ""


class Check(BaseModel):
    """One wake-up of the trading agent: why it woke, what it saw, what it decided."""
    id: str
    at: datetime
    mode: str                                    # live | shadow
    triggers: list[Trigger] = Field(default_factory=list)
    action: str = "hold"                         # buy | hold | none (no trigger, agent not called)
    ticker: str = ""
    usd: float = 0.0
    summary: str = ""
    what_changed: str = ""
    proposal_id: Optional[str] = None
    model: Optional[str] = None
    cost_usd: float = 0.0
    notes: list[str] = Field(default_factory=list)
    sha256: Optional[str] = None


class StrategyDecision(BaseModel):
    """What the model returns. Code checks every field before anything happens."""
    action: Literal["buy", "hold"]
    ticker: Optional[str] = None
    usd: Optional[float] = None
    what_changed: str = ""                       # the agent's reading of the trigger: what the evidence says about it
    rationale: str = ""
    risks: list[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "low"


RULES = [
    "Wake on: a new sealed report for a traded topic; a one-day move beyond the thresholds in a held or allowed stock; a routine review.",
    "Buy only companies named by the research evidence (patents or papers), from reports with verdict 'strong' or 'building' and confidence at or above the minimum.",
    "On a sharp fall: if the latest report and its findings still support the company and nothing in them explains the fall, the agent may add once more at the lower price (at most the allowed number of adds); if the report weakened or the findings explain the fall, hold.",
    "On a sharp rise: never chase; hold and note it.",
    "Size follows confidence: less confident reports get smaller orders; in live mode the size is fixed by the caps.",
    "Diversify: in shadow mode one company stays under the share cap; keeping cash is allowed and must be explained.",
    "Only buys. Selling, auto-approval and more budget each need the owner's written yes.",
    "Every wake-up is recorded with its triggers and reasoning, and the record is fingerprinted.",
]


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
           budget_usd: float, fixed_usd: Optional[float], cfg: StrategyConfig, adds_so_far: dict[str, int]) -> tuple[StrategyDecision, Optional[Candidate], Optional[str], float, list[str]]:
    """Returns (decision, candidate, model alias, cost, notes). `fixed_usd` is set in live mode (size fixed by the caps)."""
    notes: list[str] = []
    quotable = [c for c in candidates if c.quotable]
    listing = [{"ticker": c.ticker, "token": c.symbol, "topic": c.topic, "report_verdict": c.verdict_band, "report_score": c.score,
                "report_confidence_pct": c.confidence_pct, "company_size_risk": c.tier, "why_in_fund": c.why, "price_stretch": c.price_stretch or "unknown",
                "last_close": c.last_close, "last_close_date": c.last_close_date, "quotable": c.quotable, "quote_cost_pct": c.quote_cost_pct,
                "adds_so_far": adds_so_far.get(c.ticker.upper(), 0)} for c in candidates]
    size_line = (f"Trade size is FIXED at ${fixed_usd:.2f} (live mode)." if fixed_usd else
                 f"Pretend budget available: ${budget_usd:,.2f}; one company may not exceed {cfg.max_ticker_share_pct:.0f}% of the whole budget.")
    user = (f"WHY YOU WOKE UP:\n" + "\n".join(f"- {t.kind}: {t.detail}" for t in triggers) + "\n\n"
            f"{size_line}\nMinimum report confidence for a new buy: {cfg.min_confidence_pct:.0f}%. Max adds per ticker: {cfg.max_adds_per_ticker}.\n\n"
            f"WHAT YOU ALREADY HOLD:\n{json.dumps(holdings)}\n\n"
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
    cand = next((c for c in quotable if c.ticker.upper() == (d.ticker or "").upper()), None)
    if cand is None:
        notes.append(f"buy of '{d.ticker}' refused by code: not a quotable candidate; turned into hold")
        d.action, d.ticker, d.usd = "hold", None, None
        return d, None, reply.llm_alias, cost, notes
    if (cand.confidence_pct or 0) < cfg.min_confidence_pct:
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

"""Trading Agent: a strong model proposes ONE small buy (or hold) from an allowlist. It never executes anything.

The model's answer is checked by code: the ticker must be a quotable candidate and the amount inside the limits,
otherwise the proposal becomes a hold with the reason. Execution, limits and approval live in app/fund/live.py and
scripts/fund_trade.py.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.models.router import ModelRouter, ModelRouterError

AGENT = "trader"                      # model alias in config/model_config.yaml
_PROMPT_PATH = Path(__file__).with_name("prompt.md")


class Candidate(BaseModel):
    ticker: str
    symbol: str                       # token symbol, e.g. INTCon
    asset_id: str
    topic: str
    verdict_band: Optional[str] = None
    score: Optional[float] = None
    confidence_pct: Optional[float] = None     # confidence of that report (evidence x risk multiplier)
    tier: str = ""
    why: str = ""
    price_stretch: Optional[str] = None
    last_close: Optional[float] = None
    last_close_date: Optional[str] = None
    quotable: bool = False
    quote_cost_pct: Optional[float] = None
    dry_quote: Optional[dict] = None
    note: str = ""


class TraderDecision(BaseModel):
    action: Literal["buy", "hold"]
    ticker: Optional[str] = None
    usd: Optional[float] = None
    rationale: str = ""
    risks: list[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "low"


class TraderResult(BaseModel):
    decision: TraderDecision
    candidate: Optional[Candidate] = None
    model: Optional[str] = None
    cost_usd: float = 0.0
    notes: list[str] = Field(default_factory=list)


def decide(router: ModelRouter, candidates: list[Candidate], *, budget_usd: float, min_usd: float) -> TraderResult:
    quotable = [c for c in candidates if c.quotable]
    if not quotable:
        return TraderResult(decision=TraderDecision(action="hold", rationale="No candidate can be bought at this size right now."),
                            notes=["no quotable candidate; the model was not called"])
    listing = [{"ticker": c.ticker, "token": c.symbol, "topic": c.topic, "report_verdict": c.verdict_band, "report_score": c.score, "report_confidence_pct": c.confidence_pct,
                "company_size_risk": c.tier, "why_in_fund": c.why, "price_stretch": c.price_stretch or "unknown",
                "quotable": c.quotable, "quote_cost_pct": c.quote_cost_pct} for c in candidates]
    messages = [
        {"role": "system", "content": _PROMPT_PATH.read_text(encoding="utf-8")},
        {"role": "user", "content": f"Trade size (fixed): ${budget_usd:.2f}.\n\nCANDIDATES:\n{json.dumps(listing, indent=1)}"},
    ]
    try:
        reply = router.complete(AGENT, messages, response_model=TraderDecision)
    except ModelRouterError as exc:
        return TraderResult(decision=TraderDecision(action="hold", rationale="The trading model did not answer, so nothing is proposed."),
                            notes=[f"model error: {str(exc)[:160]}"])
    d: TraderDecision = reply.parsed  # type: ignore[assignment]
    cost = sum(u.get("cost_usd", 0.0) for u in router.usage_summary() if u.get("agent") == AGENT)
    out = TraderResult(decision=d, model=reply.llm_alias, cost_usd=round(cost, 6))
    if d.confidence == "high":
        d.confidence = "medium"
        out.notes.append("confidence capped at medium (small test, thin evidence)")
    if d.action == "hold":
        d.ticker, d.usd = None, None
        return out
    cand = next((c for c in quotable if c.ticker.upper() == (d.ticker or "").upper()), None)
    problem = None
    if cand is None:
        problem = f"the model chose '{d.ticker}', which is not a quotable candidate"
    elif d.usd is None or d.usd < min_usd - 1e-9 or d.usd > budget_usd + 1e-9:
        problem = f"the model's amount {d.usd} is outside ${min_usd:.2f}-${budget_usd:.2f}"
    if problem:
        out.notes.append(problem + "; turned into a hold")
        out.decision = TraderDecision(action="hold", rationale=f"Proposal rejected by code: {problem}.", confidence="low")
        return out
    if abs(float(d.usd) - budget_usd) > 0.005:
        out.notes.append(f"amount set to the quote-tested size ${budget_usd:.2f} (the model said {d.usd})")
    d.usd = round(float(budget_usd), 2)      # the size is the owner's cap and the size the quotes were tested at
    out.candidate = cand
    return out


# ------------------------------------------------------------------ shadow mode: the agent spreads a pretend budget
_SHADOW_PROMPT = Path(__file__).with_name("prompt_shadow.md")


class TraderOrder(BaseModel):
    ticker: str
    usd: float
    reason: str = ""


class TraderPlan(BaseModel):
    orders: list[TraderOrder] = Field(default_factory=list)
    summary: str = ""
    risks: list[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "low"


class PlanResult(BaseModel):
    plan: TraderPlan
    orders: list[tuple[Candidate, float, str]] = Field(default_factory=list)   # validated: (candidate, usd, reason)
    model: Optional[str] = None
    cost_usd: float = 0.0
    notes: list[str] = Field(default_factory=list)


def allocate(router: ModelRouter, candidates: list[Candidate], *, budget_usd: float, holdings: Optional[list[dict]] = None) -> PlanResult:
    """Shadow mode only: the model decides sizes freely; code keeps it to the candidate list and inside the budget."""
    if not candidates or budget_usd <= 0:
        return PlanResult(plan=TraderPlan(summary="Nothing to allocate."), notes=["no candidates or no budget; the model was not called"])
    listing = [{"ticker": c.ticker, "token": c.symbol, "topic": c.topic, "report_verdict": c.verdict_band, "report_score": c.score, "report_confidence_pct": c.confidence_pct,
                "company_size_risk": c.tier, "why_in_fund": c.why, "price_stretch": c.price_stretch or "unknown",
                "quote_cost_pct": c.quote_cost_pct} for c in candidates]
    messages = [
        {"role": "system", "content": _SHADOW_PROMPT.read_text(encoding="utf-8")},
        {"role": "user", "content": f"Pretend budget available: ${budget_usd:,.2f}.\n\nAlready held in the shadow portfolio: "
                                    f"{json.dumps(holdings or [])}\n\nCANDIDATES:\n{json.dumps(listing, indent=1)}"},
    ]
    try:
        reply = router.complete(AGENT, messages, response_model=TraderPlan)
    except ModelRouterError as exc:
        return PlanResult(plan=TraderPlan(summary="The trading model did not answer, so nothing is allocated."), notes=[f"model error: {str(exc)[:160]}"])
    plan: TraderPlan = reply.parsed  # type: ignore[assignment]
    cost = sum(u.get("cost_usd", 0.0) for u in router.usage_summary() if u.get("agent") == AGENT)
    out = PlanResult(plan=plan, model=reply.llm_alias, cost_usd=round(cost, 6))
    if plan.confidence == "high":
        plan.confidence = "medium"
    by = {c.ticker.upper(): c for c in candidates}
    seen: set[str] = set()
    valid: list[tuple[Candidate, float, str]] = []
    for o in plan.orders:
        t = (o.ticker or "").upper()
        if t not in by:
            out.notes.append(f"order for '{o.ticker}' dropped: not a candidate")
        elif t in seen:
            out.notes.append(f"second order for {t} dropped: one order per ticker")
        elif not (o.usd and o.usd > 0):
            out.notes.append(f"order for {t} dropped: no positive amount")
        else:
            seen.add(t)
            valid.append((by[t], float(o.usd), o.reason))
    total = sum(u for _, u, _ in valid)
    if total > budget_usd + 0.005:                       # never more pretend money than there is: scale every order down
        k = budget_usd / total
        valid = [(c, u * k, r) for c, u, r in valid]
        out.notes.append(f"orders added up to ${total:,.2f}; scaled to the ${budget_usd:,.2f} available")
    out.orders = [(c, round(u, 2), r) for c, u, r in valid if round(u, 2) > 0]
    return out

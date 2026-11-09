"""Chief Research Agent: plans the research and reviews it for gaps. Never does research itself."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from app.agents.formatting import format_findings, title_map
from app.models.router import ModelRouter, ModelRouterError
from app.schemas.common import AgentError
from app.schemas.market import MarketResult
from app.schemas.research import GapReview, ResearchPlan, RiskResult
from app.schemas.science import ScienceResult
from app.schemas.patent import PatentResult
from app.schemas.xsignals import XResult

log = logging.getLogger("futurescout.chief")

_DIR = Path(__file__).parent
MAX_QUERY_CHARS = 100


def clean_queries(queries: list[str], *, limit: int, exclude: Optional[list[str]] = None) -> list[str]:
    """Strip, drop empties/duplicates/too-long strings, cap the count."""
    seen = {q.strip().lower() for q in (exclude or [])}
    out: list[str] = []
    for q in queries:
        q = " ".join(str(q).split())
        if not q or len(q) > MAX_QUERY_CHARS or q.lower() in seen:
            continue
        seen.add(q.lower())
        out.append(q)
    return out[:limit]


def fallback_plan(topic: str) -> ResearchPlan:
    """Used when the model is unavailable: plain, deterministic, no model-made claims."""
    return ResearchPlan(
        source="default",
        topic_summary=f"Research on '{topic}' (default plan: the model could not produce one).",
        science_queries=[topic],
        risk_queries=[f"{topic} limitations", f"{topic} challenges"],
        market_keywords=[topic],
        key_questions=[],
    )


class ChiefAgent:
    name = "chief"

    def __init__(self, router: ModelRouter) -> None:
        self.router = router

    def plan(self, topic: str, question: Optional[str] = None, sector: Optional[str] = None,
             sector_hints: Optional[str] = None) -> tuple[ResearchPlan, list[AgentError]]:
        user = f"Research topic: {topic}"
        if sector:
            user += f"\nSector: {sector}" + (f" (themes that usually matter here: {sector_hints})" if sector_hints else "")
        if question:
            user += f"\nSpecific question from the user: {question}"
        messages = [
            {"role": "system", "content": (_DIR / "plan_prompt.md").read_text(encoding="utf-8")},
            {"role": "user", "content": user},
        ]
        try:
            plan: ResearchPlan = self.router.complete(self.name, messages, response_model=ResearchPlan).parsed  # type: ignore[assignment]
        except ModelRouterError as exc:
            return fallback_plan(topic), [AgentError(
                agent=self.name, source="model", message=f"planning failed, default plan used: {exc} {exc.attempts}".strip(),
                recoverable=True)]

        science = clean_queries([topic, *plan.science_queries], limit=6)  # the topic itself always comes first
        risk = clean_queries(plan.risk_queries, limit=6) or fallback_plan(topic).risk_queries
        market = clean_queries([topic, *plan.market_keywords], limit=6)
        return plan.model_copy(update={"science_queries": science, "risk_queries": risk, "market_keywords": market}), []

    def review(
        self,
        topic: str,
        plan: ResearchPlan,
        science: Optional[ScienceResult],
        risk: Optional[RiskResult],
        *,
        agents_not_run: list[str],
        market: Optional[MarketResult] = None,
        x: Optional[XResult] = None,
        patent: Optional[PatentResult] = None,
    ) -> tuple[GapReview, list[AgentError]]:
        sources = (science.sources if science else [])
        titles = title_map(sources, risk.sources if risk else [], market.sources if market else [], x.sources if x else [],
                           patent.sources if patent else [])
        science_findings = format_findings(science.findings if science else [], titles)
        risk_findings = format_findings(risk.findings if risk else [], titles)
        market_findings = format_findings(market.findings if market else [], titles)
        paper_lines = "\n".join(f"- {s.id}: {s.title} ({s.published_at})" for s in sources) or "(none)"
        user = (
            f"Topic: {topic}\n"
            f"Planned science queries: {plan.science_queries}\nPlanned risk queries: {plan.risk_queries}\n"
            f"Science status: {science.status if science else 'did not run'}\n"
            f"Agents NOT run in this version: {', '.join(agents_not_run) or 'none'}\n\n"
            f"Papers retrieved by Science ({len(sources)}):\n{paper_lines}\n\n"
            f"Science findings:\n{science_findings}\n\nRisk findings:\n{risk_findings}\n\n"
            f"Market findings (company filings and news; a paper search cannot fill gaps here):\n{market_findings}\n\n"
            f"X findings (social signals from approved accounts; never facts):\n{format_findings(x.findings if x else [], titles)}\n\n"
            f"Patent findings (EPO publications):\n{format_findings(patent.findings if patent else [], titles)}"
        )
        messages = [
            {"role": "system", "content": (_DIR / "review_prompt.md").read_text(encoding="utf-8")},
            {"role": "user", "content": user},
        ]
        try:
            review: GapReview = self.router.complete(self.name, messages, response_model=GapReview).parsed  # type: ignore[assignment]
        except ModelRouterError as exc:
            return GapReview(sufficient=True, gaps=["Chief gap review was unavailable (model failure); evidence was not reviewed."]), [
                AgentError(agent=self.name, source="model", message=f"gap review failed: {exc} {exc.attempts}".strip(), recoverable=True)]

        used = [*plan.science_queries, *plan.risk_queries]
        extra = [] if review.sufficient else clean_queries(review.extra_science_queries, limit=3, exclude=used)
        return review.model_copy(update={"extra_science_queries": extra}), []

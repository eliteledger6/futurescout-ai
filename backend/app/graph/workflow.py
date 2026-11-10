"""LangGraph workflow connecting the agents.

  chief_plan -> science  -> market (companies FROM the papers and patents) \
             -> patent  ->                                                   >-> chief_review -> (gap? -> science_more -> chief_review)
             -> risk_independent                                            /       -> risk_challenge -> investment
             -> x                                                          /

Science, the independent Risk pass, X and Patent run in parallel; Market waits for Science and Patent because it
reads the SEC filings of the companies they point to (no fixed company list). The Chief may request ONE extra
Science round (MAX_EXTRA_ROUNDS) so cost stays bounded. A crashing agent is recorded as an
error and the workflow continues with what it has.
"""

from __future__ import annotations

import logging
import operator
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Callable, Optional, TypedDict

from langgraph.graph import END, START, StateGraph

from app.agents.chief import ChiefAgent
from app.agents.chief.agent import fallback_plan
from app.agents.investment import InvestmentAgent
from app.agents.market import MarketAgent
from app.agents.x import XAgent
from app.agents.patent import PatentAgent
from app.agents.risk.price_timing import run_price_timing
from app.agents.risk import RiskAgent
from app.agents.science import ScienceAgent
from app.config import ConfigError
from app.models.router import ModelRouter
from app.schemas.common import AgentError
from app.schemas.research import GapReview, InvestmentResult, ResearchPlan, ResearchReport, RiskResult
from app.schemas.market import MarketResult
from app.schemas.science import ScienceResult
from app.schemas.xsignals import XResult
from app.schemas.patent import PatentResult
from app.schemas.timing import PriceTimingResult
from app.schemas.scout import ScoutResult
from app.scout import CompanyScout
from app.radar import load_sectors, sector_of_topic
from app.sources.arxiv import ArxivClient
from app.sources.edgar import EdgarClient
from app.sources.edgar_fulltext import EdgarFullTextClient
from app.sources.sec_facts import SecFactsClient
from app.sources.gdelt import GdeltClient
from app.sources.openalex import OpenAlexClient
from app.sources.x import XClient
from app.sources.epo import EpoOpsClient
from app.sources.prices import AlphaVantageClient

log = logging.getLogger("futurescout.workflow")

MAX_EXTRA_ROUNDS = 1
AGENTS_NOT_BUILT: list[str] = []  # every agent is built in this version


def agents_not_run(market: Optional[MarketResult], x: Optional[XResult] = None,
                   patent: Optional[PatentResult] = None) -> list[str]:
    """Agents that gave no analysed evidence (their model analysis did not succeed, or they were not configured)."""
    missing = list(AGENTS_NOT_BUILT)
    if not (patent and patent.llm_alias):
        missing.append("patent")
    if not (market and market.llm_alias):
        missing.append("market")
    if not (x and x.llm_alias):
        missing.append("x")
    return missing


class State(TypedDict, total=False):
    topic: str
    question: Optional[str]
    sector: Optional[str]
    plan: ResearchPlan
    science: ScienceResult
    risk: RiskResult
    market: MarketResult
    x: XResult
    patent: PatentResult
    timing: PriceTimingResult
    scout: ScoutResult
    reviews: Annotated[list[GapReview], operator.add]
    loops: int
    investment: InvestmentResult
    errors: Annotated[list[AgentError], operator.add]


@dataclass
class Deps:
    chief: ChiefAgent
    science: ScienceAgent
    risk: RiskAgent
    investment: InvestmentAgent
    market: Optional[MarketAgent] = None
    x: Optional[XAgent] = None
    patent: Optional[PatentAgent] = None
    prices: Optional[AlphaVantageClient] = None
    scout: Optional[CompanyScout] = None
    sector_hints: Optional[str] = None
    now: Callable[[], datetime] = lambda: datetime.now(timezone.utc)
    from_year: Optional[int] = None
    max_papers: int = 12


def _safe(name: str, fn: Callable[[State], dict]) -> Callable[[State], dict]:
    """Turn an unexpected crash into a recorded error so the rest of the run can continue."""
    def wrapper(state: State) -> dict:
        try:
            return fn(state)
        except ConfigError:
            raise  # missing credentials: stop loudly instead of failing every node
        except Exception as exc:  # noqa: BLE001
            log.exception("node %s crashed", name)
            return {"errors": [AgentError(agent=name, source="agent crash", message=f"{type(exc).__name__}: {str(exc)[:300]}")]}
    return wrapper


def build_graph(deps: Deps):
    def plan_of(state: State) -> ResearchPlan:
        return state.get("plan") or fallback_plan(state["topic"])

    def chief_plan(state: State) -> dict:
        plan, errors = deps.chief.plan(state["topic"], state.get("question"), sector=state.get("sector"),
                                       sector_hints=deps.sector_hints)
        return {"plan": plan, "errors": errors}

    def science(state: State) -> dict:
        plan = plan_of(state)
        return {"science": deps.science.run(state["topic"], queries=plan.science_queries,
                                            from_year=deps.from_year, max_papers=deps.max_papers)}

    def risk_independent(state: State) -> dict:
        plan = plan_of(state)
        return {"risk": deps.risk.run_independent(state["topic"], plan.risk_queries,
                                                  from_year=deps.from_year, max_papers=deps.max_papers)}

    def market(state: State) -> dict:
        if deps.market is None:
            return {}
        return {"market": deps.market.run(state["topic"], keywords=plan_of(state).market_keywords,
                                          science=state.get("science"), patent=state.get("patent"))}

    def x(state: State) -> dict:
        if deps.x is None:
            return {}
        return {"x": deps.x.run(state["topic"], keywords=plan_of(state).market_keywords)}

    def patent(state: State) -> dict:
        if deps.patent is None:
            return {}
        return {"patent": deps.patent.run(state["topic"], keywords=plan_of(state).market_keywords)}

    def chief_review(state: State) -> dict:
        review, errors = deps.chief.review(state["topic"], plan_of(state), state.get("science"), state.get("risk"),
                                           agents_not_run=agents_not_run(state.get("market"), state.get("x"), state.get("patent")),
                                           market=state.get("market"), x=state.get("x"), patent=state.get("patent"))
        return {"reviews": [review], "loops": state.get("loops", 0) + 1, "errors": errors}

    def route_after_review(state: State) -> str:
        last = state["reviews"][-1] if state.get("reviews") else None
        if last and not last.sufficient and last.extra_science_queries and state.get("loops", 0) <= MAX_EXTRA_ROUNDS:
            return "more"
        return "challenge"

    def science_more(state: State) -> dict:
        plan = plan_of(state)
        extra = state["reviews"][-1].extra_science_queries
        return {"science": deps.science.run(state["topic"], queries=[*plan.science_queries, *extra],
                                            from_year=deps.from_year, max_papers=deps.max_papers + 4)}

    def risk_challenge(state: State) -> dict:
        out: dict = {}
        risk = state.get("risk")
        if risk is not None:
            out["risk"] = deps.risk.challenge(state["topic"], state.get("science"), risk)
        if deps.prices is not None:
            # Price & timing risk for the companies Market found (part of the Risk agent's job)
            out["timing"] = run_price_timing(state["topic"], state.get("market"), deps.prices, deps.risk.router, now=deps.now)
        if deps.scout is not None:
            # Company Scout: who is really working on it (patent assignees, paper affiliations, SEC filers); code only
            out["scout"] = deps.scout.run(state["topic"], state.get("science"), state.get("market"), state.get("patent"))
        return out

    def investment(state: State) -> dict:
        return {"investment": deps.investment.run(state["topic"], state.get("science"), state.get("risk"),
                                                  agents_not_run=agents_not_run(state.get("market"), state.get("x"), state.get("patent")),
                                                  question=state.get("question"), market=state.get("market"),
                                                  x=state.get("x"), patent=state.get("patent"), timing=state.get("timing"),
                                                  scout=state.get("scout"))}

    graph = StateGraph(State)
    for name, fn in [("chief_plan", chief_plan), ("science", science), ("risk_independent", risk_independent),
                     ("market", market), ("x", x), ("patent", patent),
                     ("chief_review", chief_review), ("science_more", science_more),
                     ("risk_challenge", risk_challenge), ("investment", investment)]:
        graph.add_node(name, _safe(name, fn))
    graph.add_edge(START, "chief_plan")
    graph.add_edge("chief_plan", "science")
    graph.add_edge("chief_plan", "risk_independent")
    graph.add_edge("chief_plan", "x")
    graph.add_edge("chief_plan", "patent")
    graph.add_edge(["science", "patent"], "market")
    graph.add_edge(["market", "risk_independent", "x"], "chief_review")
    graph.add_conditional_edges("chief_review", route_after_review, {"more": "science_more", "challenge": "risk_challenge"})
    graph.add_edge("science_more", "chief_review")
    graph.add_edge("risk_challenge", "investment")
    graph.add_edge("investment", END)
    return graph.compile()


def run_research(
    topic: str,
    *,
    router: ModelRouter,
    openalex: Optional[OpenAlexClient],
    arxiv: Optional[ArxivClient],
    question: Optional[str] = None,
    from_year: Optional[int] = None,
    max_papers: int = 12,
    edgar: Optional[EdgarClient] = None,
    gdelt: Optional[GdeltClient] = None,
    discovery: Optional[EdgarFullTextClient] = None,
    facts: Optional[SecFactsClient] = None,
    market_agent: Optional[MarketAgent] = None,
    x_client: Optional[XClient] = None,
    x_agent: Optional[XAgent] = None,
    epo: Optional[EpoOpsClient] = None,
    patent_agent: Optional[PatentAgent] = None,
    prices: Optional[AlphaVantageClient] = None,
    scout: Optional[CompanyScout] = None,
    sector: Optional[str] = None,
    now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    phrase_check: bool = False,      # synonyms + AI relevance check behind paper counts (live runs turn it on)
) -> ResearchReport:
    # The topic's sector (from config/topics.yaml unless given) steers the Chief's queries and which configured
    # companies the Market agent reads. Unknown topics run as plain "technology".
    if sector is None:
        try:
            sector = sector_of_topic(topic)
        except Exception:  # noqa: BLE001  (a broken config file must not stop a run)
            sector = None
    hints = None
    if sector:
        try:
            hints = next((s.hints for s in load_sectors() if s.key == sector), None)
        except Exception:  # noqa: BLE001
            hints = None
    if market_agent is None and (edgar or gdelt):
        market_agent = MarketAgent(router, edgar, gdelt, discovery=discovery, facts=facts, now=now)
    if scout is None:
        # Always runs (code only). Without an SEC client it can still list the names it found, marked "not matched".
        scout = CompanyScout(edgar, facts, now=now)
    if x_agent is None and x_client is not None:
        x_agent = XAgent(router, x_client, now=now)
    if patent_agent is None and epo is not None:
        patent_agent = PatentAgent(router, epo, now=now)
    deps = Deps(
        chief=ChiefAgent(router),
        science=ScienceAgent(router, openalex, arxiv, now=now, use_phrase_check=phrase_check),
        risk=RiskAgent(router, openalex, arxiv, now=now),
        investment=InvestmentAgent(router, now=now),
        market=market_agent,
        x=x_agent,
        patent=patent_agent,
        prices=prices,
        scout=scout,
        sector_hints=hints,
        now=now,
        from_year=from_year,
        max_papers=max_papers,
    )
    state: State = build_graph(deps).invoke({"topic": topic, "question": question, "sector": sector, "loops": 0})

    science, risk, investment = state.get("science"), state.get("risk"), state.get("investment")
    market, x, patent, timing = state.get("market"), state.get("x"), state.get("patent"), state.get("timing")
    scout_result = state.get("scout")
    errors = list(state.get("errors", []))
    for part in (science, risk, market, x, patent, timing, scout_result, investment):
        if part is not None:
            errors += part.errors

    # An agent counts as "run" only if its model analysis succeeded (retrieval alone, or a
    # default plan after a model failure, is not analysis and must not be reported as such).
    plan = state.get("plan")
    run = []
    if plan and plan.source == "model":
        run.append("chief")
    if science and science.llm_alias:
        run.append("science")
    if risk and risk.analyzed:
        run.append("risk")
    if market and market.llm_alias:
        run.append("market")
    if x and x.llm_alias:
        run.append("x")
    if patent and patent.llm_alias:
        run.append("patent")
    if timing and timing.llm_alias:
        run.append("timing")
    if scout_result and (scout_result.status == "ok" or (scout_result.status == "partial" and (scout_result.incumbents or scout_result.unlisted))):
        run.append("scout")   # partial with incumbents/unlisted = it ran and found companies, just no NEW listed one
    if investment and investment.draft:
        run.append("investment")
    usage = router.usage_summary()
    if x and x.x_usage.get("requests"):
        # X data is paid per post read: show it next to the model costs so the total is honest
        usage.append({"agent": "x (data)", "model": "X API pay-per-use", "calls": x.x_usage["requests"],
                      "failed_calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                      "cost_usd": x.x_usage.get("cost_usd", 0.0), "posts_read": x.x_usage.get("posts_read", 0)})
    return ResearchReport(
        topic=topic, question=question, sector=sector, generated_at=now(),
        agents_run=run, agents_not_run=agents_not_run(market, x, patent),
        plan=state.get("plan"), gap_reviews=list(state.get("reviews", [])),
        science=science, risk=risk, market=market, x=x, patent=patent, timing=timing, scout=scout_result, investment=investment,
        usage=usage, total_cost_usd=round(sum(u["cost_usd"] for u in usage), 6), errors=errors,
    )

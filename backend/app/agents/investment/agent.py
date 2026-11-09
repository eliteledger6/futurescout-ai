"""Investment Intelligence Agent.

The model writes the assessment; code then
  * checks every finding id it cited (invalid ids removed, unsupported statements are
    relabelled `assumption`, companies without evidence are dropped),
  * makes sure all three time horizons exist for each theme,
  * computes the opportunity score from cited ratings (app/scoring).
If there are no findings at all, the model is NOT called.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from app.agents.formatting import format_findings, title_map
from app.models.router import ModelRouter, ModelRouterError
from app.schemas.common import AgentError, Confidence, Horizon, Label
from app.schemas.research import (
    HorizonView, InvestmentDraft, InvestmentResult, Referenced, RiskResult, ScenarioDraft, ThesisDraft,
)
from app.schemas.market import MarketResult
from app.schemas.patent import PatentResult
from app.schemas.scout import ScoutResult
from app.schemas.timing import PriceTimingResult
from app.schemas.xsignals import XResult
from app.schemas.science import ScienceResult
from app.scoring.engine import RISK_KEY, ScoringConfig, compute_opportunity_score, load_scoring_config

log = logging.getLogger("futurescout.investment")

_PROMPT_PATH = Path(__file__).with_name("prompt.md")
_HORIZONS = [Horizon.NEAR, Horizon.MEDIUM, Horizon.LONG]


def _check(item: Referenced, valid_ids: set[str], where: str, issues: list[dict]) -> None:
    """Normalise one referenced statement in place."""
    ids = [i for i in dict.fromkeys(item.finding_ids) if i in valid_ids]
    removed = [i for i in item.finding_ids if i not in valid_ids]
    notes = []
    if removed:
        notes.append(f"unknown finding id(s) removed: {', '.join(dict.fromkeys(removed))}")
        issues.append({"where": where, "action": "removed_unknown_finding_ids", "detail": ", ".join(removed)})
    item.finding_ids = ids
    if item.label == Label.VERIFIED_FACT:
        item.label = Label.AI_INTERPRETATION
        notes.append("relabelled ai_interpretation: facts belong to findings, not to this assessment")
    if not ids:
        item.label = Label.ASSUMPTION
        notes.append("no supporting finding cited, so treated as an assumption")
        issues.append({"where": where, "action": "no_supporting_finding", "detail": "relabelled assumption"})
    if notes:
        item.note = "; ".join(notes)


def validate_draft(draft: InvestmentDraft, valid_ids: set[str]) -> tuple[InvestmentDraft, list[dict]]:
    issues: list[dict] = []
    draft = draft.model_copy(deep=True)
    for t_index, theme in enumerate(draft.themes, start=1):
        base = f"theme {t_index} '{theme.name}'"
        for scenario_name in ("bull", "base", "bear"):
            _check(getattr(theme, scenario_name), valid_ids, f"{base} {scenario_name}", issues)
        for view in theme.horizons:
            _check(view, valid_ids, f"{base} horizon {view.horizon.value}", issues)
        for group in ("catalysts", "risks", "invalidation_conditions", "conflicting_evidence"):
            for item in getattr(theme, group):
                _check(item, valid_ids, f"{base} {group}", issues)
        # Companies need evidence: drop (not downgrade) any company no finding supports.
        kept = []
        for company in theme.companies:
            _check(company, valid_ids, f"{base} company '{company.name}'", issues)
            if company.finding_ids:
                kept.append(company)
            else:
                issues.append({"where": base, "action": "company_dropped", "detail": company.name})
        theme.companies = kept
        # Always show all three horizons; a missing one is stated, not hidden.
        present = {v.horizon for v in theme.horizons}
        for horizon in _HORIZONS:
            if horizon not in present:
                theme.horizons.append(HorizonView(
                    horizon=horizon, assessment="Not assessed: the analysis gave no view for this horizon.",
                    label=Label.ASSUMPTION, confidence=Confidence.LOW, note="horizon missing from model output",
                ))
        theme.horizons.sort(key=lambda v: _HORIZONS.index(v.horizon) if v.horizon in _HORIZONS else 99)
    for rating in draft.dimension_ratings:
        _check(rating, valid_ids, f"rating '{rating.dimension}'", issues)
    return draft, issues


class InvestmentAgent:
    name = "investment"

    def __init__(
        self,
        router: ModelRouter,
        scoring: Optional[ScoringConfig] = None,
        *,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.router = router
        self.scoring = scoring or load_scoring_config()
        self._now = now

    def run(
        self,
        topic: str,
        science: Optional[ScienceResult],
        risk: Optional[RiskResult],
        *,
        agents_not_run: list[str],
        question: Optional[str] = None,
        market: Optional[MarketResult] = None,
        x: Optional[XResult] = None,
        patent: Optional[PatentResult] = None,
        timing: Optional[PriceTimingResult] = None,
        scout: Optional[ScoutResult] = None,
    ) -> InvestmentResult:
        sci_findings = list(science.findings) if science else []
        risk_findings = list(risk.findings) if risk else []
        challenge_findings = [c.finding for c in (risk.challenges if risk else [])]
        market_findings = list(market.findings) if market else []
        x_findings = list(x.findings) if x else []
        patent_findings = list(patent.findings) if patent else []
        timing_findings = list(timing.findings) if timing else []
        scout_findings = list(scout.findings) if scout else []
        all_findings = [*sci_findings, *risk_findings, *challenge_findings, *market_findings, *x_findings,
                        *patent_findings, *timing_findings, *scout_findings]
        valid_ids = {f.fid for f in all_findings if f.fid}

        result = InvestmentResult(topic=topic, status="no_data")
        if not valid_ids:
            result.errors.append(AgentError(agent=self.name, source="inputs", message="no findings available; assessment not generated"))
            return result

        titles = title_map(science.sources if science else [], risk.sources if risk else [],
                           market.sources if market else [], x.sources if x else [],
                           patent.sources if patent else [], timing.sources if timing else [])
        metrics = "none available"
        if science and science.acceleration:
            a = science.acceleration
            metrics = (f"OpenAlex works with the exact topic phrase in title/abstract: {science.publication_counts}. "
                       f"Research Acceleration {a.previous_year}->{a.last_full_year}: "
                       f"{a.previous_year_count}->{a.last_full_year_count} (YoY {a.yoy_growth_pct}%). Basis: {a.basis}")
        if science and science.ytd:
            y = science.ytd
            metrics += (f"\nThis year so far (1 Jan-{y.cutoff}): {y.previous_year} {y.previous_count} -> {y.year} {y.count} "
                        f"({y.growth_pct}%, trend: {y.trend or 'base too small'}). Use this to say whether momentum is still "
                        f"building or fading in the current year; the full-year figure alone cannot show that.")
        dims = "\n".join(f"- {k}: {d.label}" for k, d in self.scoring.dimensions.items())
        user = (
            f"Topic: {topic}\n" + (f"User question: {question}\n" if question else "")
            + f"Today's date: {self._now().date().isoformat()}\n"
            f"Agents NOT run in this version (no evidence from them): {', '.join(agents_not_run) or 'none'}\n\n"
            f"Research-activity metrics (computed by code):\n{metrics}\n\n"
            f"SCIENCE findings:\n{format_findings(sci_findings, titles)}\n\n"
            f"RISK findings:\n{format_findings(risk_findings, titles)}\n\n"
            f"RISK challenges to Science findings:\n"
            + (format_findings(challenge_findings, titles) + "\n" + "\n".join(
                f"  {c.finding.fid} targets: {c.target_finding_ids or 'general'}; severity: {c.severity.value}"
                for c in (risk.challenges if risk else [])) if challenge_findings else "(none)")
            + f"\n\nMARKET findings (company filing excerpts and news headlines):\n{format_findings(market_findings, titles)}"
            + f"\n\nX findings (posts by approved company/standards/press accounts, last 7 days; social signals, never facts):\n{format_findings(x_findings, titles)}"
            + f"\n\nPATENT findings (EPO worldwide publications; applications are claims, not proof):\n{format_findings(patent_findings, titles)}"
            + (f"\nPatent publications per year (computed by code): {patent.publication_counts}; Patent Acceleration "
               f"{patent.acceleration.previous_year}->{patent.acceleration.last_full_year}: {patent.acceleration.yoy_growth_pct}% "
               f"(recent years undercounted by publication delay)" if patent and patent.acceleration else "")
            + (f"\nPatents this year so far (computed by code): {patent.ytd.count} by {patent.ytd.cutoff} {patent.ytd.year} vs "
               f"{patent.ytd.previous_count} by the same date in {patent.ytd.previous_year} ({patent.ytd.growth_pct}%, "
               f"trend {patent.ytd.trend or 'base too small'})" if patent and patent.ytd else "")
            + f"\n\nPRICE & TIMING RISK findings (code-computed metrics over ~100 trading days; risk input only, never a buy/sell signal):\n{format_findings(timing_findings, titles)}"
            + ("\n" + "\n".join(f"  {m.ticker}: timing risk {m.timing_risk} ({'; '.join(m.reasons)})" for m in timing.metrics)
               if timing and timing.metrics else "")
            + f"\n\nCOMPANY SCOUT findings (K1...; code-computed from patent assignees, company author affiliations and SEC filers, "
              f"with SEC XBRL financials; the next-runner score is a transparent heuristic):\n{format_findings(scout_findings, titles)}"
            + (f"\n  Not SEC-listed names also seen (no financials; private or foreign): "
               + ", ".join(f"{u.name} ({u.patents} patents, {u.papers} papers)" for u in scout.unlisted[:6])
               if scout and scout.unlisted else "")
            + f"\n\nScoring dimension keys (rate each, plus 'risk_adjustment'):\n{dims}\n- {RISK_KEY}: Risk Adjustment (0-5 on the RISK SCALE in your instructions; 5 = severe risk)"
        )
        messages = [
            {"role": "system", "content": _PROMPT_PATH.read_text(encoding="utf-8")},
            {"role": "user", "content": user},
        ]
        try:
            reply = self.router.complete(self.name, messages, response_model=InvestmentDraft)
        except ModelRouterError as exc:
            result.status = "partial"
            result.errors.append(AgentError(agent=self.name, source="model", message=f"{exc} {exc.attempts}".strip(), recoverable=True))
            return result

        draft, issues = validate_draft(reply.parsed, valid_ids)  # type: ignore[arg-type]
        result.draft = draft
        result.reference_issues = issues
        result.score = compute_opportunity_score(draft.dimension_ratings, valid_ids, self.scoring)
        result.status = "ok"
        return result

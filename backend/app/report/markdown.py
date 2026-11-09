"""Render a ResearchReport as Markdown. Pure formatting: it adds no content of its own
beyond fixed disclaimers, and shows gaps/errors instead of hiding them."""

from __future__ import annotations

from typing import Iterable, Optional

from app.schemas.common import Finding, SourceRecord
from app.schemas.research import Referenced, ResearchReport

DISCLAIMER = (
    "**Research information only, not investment advice.** This report is produced by AI agents "
    "from the sources listed below. It does not recommend buying or selling anything, does not "
    "predict prices, and does not promise any return. Forecasts are uncertain and may be wrong."
)

LEGEND = (
    "`verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the "
    "AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting "
    "evidence cited. `unverified_claim` = asserted but not confirmed."
)


_MISSING_EVIDENCE = {
    "patent": "patent",
    "market": "company, customer, manufacturing or supply-chain",
    "x": "social-media",
}


def _refs(item: Referenced) -> str:
    return f" [{', '.join(item.finding_ids)}]" if item.finding_ids else " [no supporting finding]"


def _tag(item: Referenced) -> str:
    return f"*({item.label.value})*" + (f" _{item.note}_" if item.note else "")


def _finding_block(f: Finding, urls: dict[str, SourceRecord]) -> list[str]:
    lines = [f"- **[{f.fid}]** *({f.label.value}, confidence {f.confidence.value})* {f.claim}"]
    for sid in f.source_ids:
        s = urls.get(sid)
        if s:
            lines.append(f"  - source: [{s.title}]({s.url}) ({s.source_name}, {s.published_at or 'date unknown'}, {s.text_depth})")
    if f.supporting_excerpt:
        lines.append(f"  - excerpt: \"{f.supporting_excerpt}\"")
    if f.rationale:
        lines.append(f"  - reasoning: {f.rationale}")
    if f.guard_note:
        lines.append(f"  - citation check: {f.guard_note}")
    return lines


def _bullets(items: Iterable[str]) -> list[str]:
    return [f"- {i}" for i in items]


def render_markdown(report: ResearchReport) -> str:
    out: list[str] = [f"# FUTURESCOUT AI research report: {report.topic}", ""]
    out += [f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M UTC')}", ""]
    if report.question:
        out += [f"Question: {report.question}", ""]
    out += [DISCLAIMER, "", f"How to read the labels: {LEGEND}", ""]

    sources: dict[str, SourceRecord] = {}
    for group in ((report.science.sources if report.science else []), (report.risk.sources if report.risk else []),
                  (report.market.sources if report.market else []), (report.x.sources if report.x else []),
                  (report.patent.sources if report.patent else []), (report.timing.sources if report.timing else [])):
        for s in group:
            sources[s.id] = s

    out += ["## Coverage", f"- Agents that produced output: {', '.join(report.agents_run) or 'none'}"]
    if report.agents_not_run:
        gaps = [_MISSING_EVIDENCE.get(a, a) for a in report.agents_not_run]
        out.append(
            f"- Agents NOT run in this version: {', '.join(report.agents_not_run)}. Conclusions therefore have no "
            f"{', '.join(gaps)} evidence."
        )
    out.append("")

    inv = report.investment
    draft = inv.draft if inv else None
    from app.report.verdict import build_verdict
    v = build_verdict(report)
    out += ["## Verdict (forecast, computed from the report)"]
    if v.get("available"):
        out += [f"**{v['headline']}**" + (f" — score {v['score']}" if v.get('score') is not None else "") + f", confidence {v['confidence']}."]
        if v.get("qualifiers"):
            out.append("Qualifiers: " + "; ".join(v["qualifiers"]) + ".")
        if v.get("plain"):
            out += ["", v["plain"]]
        if v.get("why"):
            out += ["", "Why:"] + _bullets(v["why"])
        if v.get("watch"):
            out += ["", "Watch out for:"] + _bullets(v["watch"])
        if v.get("change"):
            out += ["", "What would change this view:"] + _bullets(v["change"])
    else:
        out.append(v["headline"])
    out += ["", f"_{v['disclaimer']}_", ""]
    out += ["## Summary"]
    out += [draft.summary if draft else "_No assessment was generated (see errors below)._", ""]

    # ---- score
    if inv and inv.score:
        sc = inv.score
        out += ["## Technology Opportunity Score"]
        if sc.reportable:
            conf = (f"**Confidence: {sc.confidence_pct:.0f}%** ({sc.confidence.value}; evidence {sc.evidence_confidence_pct:.0f}% x risk multiplier "
                    f"{sc.risk_multiplier})" if sc.confidence_pct is not None else f"confidence: {sc.confidence.value}")
            out.append(f"**Opportunity score: {sc.score} / 100** · {conf} · evidence coverage {sc.coverage:.0%}")
        elif sc.score is not None:
            out.append(f"**Not reportable.** Indicative value {sc.score} / 100 uses only {sc.coverage:.0%} of the scoring weight; do not compare it with other technologies.")
        else:
            out.append("**No score computed:** no dimension had cited evidence.")
        out.append("")
        if sc.risk_rating is not None:
            if sc.risk_penalty_pct is not None:      # method v1 (older reports)
                out += [f"Risk adjustment: rating {sc.risk_rating}/5 lowered the score by {sc.risk_penalty_pct}% (base {sc.base_score}).", ""]
            else:
                out += [f"Risk: rating {sc.risk_rating}/5 does not change the score; it multiplies confidence by {sc.risk_multiplier}.", ""]
        if sc.commercialization_gap is not None:
            out += [f"Commercialization Gap (research momentum rating minus commercial readiness rating): {sc.commercialization_gap:+.0f}", ""]
        out += ["", "| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |", "|---|---|---|---|---|"]
        for d in sc.dimensions:
            if d.status == "scored":
                out.append(f"| {d.label} | {d.weight:.0%} | {d.rating} | {', '.join(d.finding_ids)} | {d.rationale} |")
            else:
                out.append(f"| {d.label} | {d.weight:.0%} | missing | none | {d.missing_reason} |")
        out += ["", f"Formula: {sc.formula}", ""] + _bullets(sc.notes) + [""]

    # ---- themes
    if draft and draft.themes:
        out += ["## Investment themes", "_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._", ""]
        for theme in draft.themes:
            out += [f"### {theme.name}", ""]
            if theme.technologies:
                out += [f"Technologies: {', '.join(theme.technologies)}", ""]
            out += ["| Horizon | Assessment | Confidence |", "|---|---|---|"]
            for v in theme.horizons:
                out.append(f"| {v.horizon.value} | {v.assessment} {_tag(v)}{_refs(v)} | {v.confidence.value} |")
            out.append("")
            for name, sc_ in (("Bull case", theme.bull), ("Base case", theme.base), ("Bear case", theme.bear)):
                out += [f"**{name}:** {sc_.narrative} {_tag(sc_)}{_refs(sc_)}", ""]
            for title, items in (("Catalysts", theme.catalysts), ("Risks", theme.risks),
                                 ("What would invalidate this thesis", theme.invalidation_conditions),
                                 ("Conflicting evidence", theme.conflicting_evidence)):
                out.append(f"**{title}:**")
                out += [f"- {i.text} {_tag(i)}{_refs(i)}" for i in items] or ["- none stated"]
                out.append("")
            out.append("**Companies named by cited evidence:**")
            out += [f"- {c.name}: {c.relevance}{_refs(c)}" for c in theme.companies] or ["- none (no company evidence in the cited findings)"]
            out.append("")

    # ---- evidence
    if report.science:
        s = report.science
        out += ["## Evidence: academic research", f"Status: {s.status}. {s.coverage_note}", ""]
        if s.publication_counts:
            out.append(f"OpenAlex works per year with the exact topic phrase in title/abstract: {s.publication_counts}")
        if s.acceleration:
            a = s.acceleration
            out.append(f"Research Acceleration {a.previous_year}->{a.last_full_year}: {a.previous_year_count} -> {a.last_full_year_count} ({a.yoy_growth_pct}% YoY). {a.basis}")
        if s.ytd:
            y = s.ytd
            out.append(f"This year so far (1 Jan to {y.cutoff}): {y.previous_year} {y.previous_count} -> {y.year} {y.count} "
                       f"({y.growth_pct}%, trend: {y.trend or 'base too small to call'}). {y.basis}")
        out.append("")
        for f in s.findings:
            out += _finding_block(f, sources)
        for title, items in (("Emerging directions", s.emerging_directions), ("Open problems", s.open_problems), ("Limitations", s.limitations)):
            if items:
                out += ["", f"**{title}:**"] + _bullets(items)
        out.append("")
    if report.risk:
        r = report.risk
        out += ["## Evidence: risks and contrarian findings", f"Status: {r.status}. Risk search queries: {r.queries}", ""]
        for f in r.findings:
            out += _finding_block(f, sources)
        if r.hype_flags:
            out += ["", "**Possible hype:**"] + _bullets(r.hype_flags)
        if r.challenges:
            out += ["", "**Challenges to the Science findings:**"]
            for c in r.challenges:
                out.append(f"- Targets {c.target_finding_ids or 'general'}, severity {c.severity.value}:")
                out += ["  " + line for line in _finding_block(c.finding, sources)]
        if r.limitations:
            out += ["", "**Limitations:**"] + _bullets(r.limitations)
        out.append("")
    if report.market:
        m = report.market
        out += ["## Evidence: company filings and news", f"Status: {m.status}. {m.coverage_note}", "",
                f"Keywords searched in filings: {', '.join(m.keywords) or 'none'}"]
        if m.news_query:
            out.append(f"News headline search: \"{m.news_query}\" (GDELT)")
        if m.companies:
            out += ["", "| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |", "|---|---|---|---|---|---|---|"]
            for c in m.companies:
                f = c.fundamentals or {}
                rev = f.get("revenue") or {}
                latest = str(f.get("latest_year")) if f.get("latest_year") else None
                size = f"{f.get('size_class')}: {rev.get(latest, 0) / 1e9:.1f}B {f.get('currency', 'USD')}" if latest and latest in rev else "n/a"
                growth = f"{f['revenue_growth_pct']:+.1f}%" if f.get("revenue_growth_pct") is not None else "n/a"
                rnd = f"{f['rnd_intensity_pct']:.1f}% of revenue" if f.get("rnd_intensity_pct") is not None else "n/a"
                note = " ".join(x for x in [("discovered by full-text search" if c.discovered else ""),
                                            (f"{c.press_releases_read} press release(s) read" if c.press_releases_read else ""), c.error or ""] if x)
                out.append(f"| {c.name} ({c.ticker}) | {c.filings_checked} | {c.filings_with_mentions} | {size} | {growth} | {rnd} | {note} |")
            out += ["", "_A report that does not mention the keywords does not show that the company is absent from this market. "
                        "Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._"]
        out.append("")
        for f in m.findings:
            out += _finding_block(f, sources)
        if m.limitations:
            out += ["", "**Limitations:**"] + _bullets(m.limitations)
        out.append("")
    if report.x:
        xr = report.x
        out += ["## Social signals from X", f"Status: {xr.status}. {xr.coverage_note}", ""]
        if xr.accounts:
            out.append(f"Accounts searched ({len(xr.accounts)}): {', '.join('@' + a for a in xr.accounts)}")
        if xr.x_usage:
            out.append(f"Posts read: {xr.x_usage.get('posts_read', 0)} (estimated X cost ${xr.x_usage.get('cost_usd', 0):.3f})")
        out.append("")
        for f in xr.findings:
            out += _finding_block(f, sources)
        if xr.suggested_accounts:
            out += ["", "**Accounts the X agent found posting about this topic (suggestions, not yet watched unless listed under changes):**"]
            out += [f"- @{s['handle']} ({s['name']}): score {s['score']}, {s['posts_on_topic']} on-topic post(s), "
                    f"{s['followers'] if s['followers'] is not None else '?'} followers" + (f"; caution: {'; '.join(s['flags'])}" if s["flags"] else "")
                    for s in xr.suggested_accounts]
        if xr.watchlist_changes:
            out += ["", "**Watchlist changes made by the agent (auto_manage on):**"] + _bullets(xr.watchlist_changes)
        if xr.limitations:
            out += ["", "**Limitations:**"] + _bullets(xr.limitations)
        out.append("")
    if report.patent:
        pt = report.patent
        out += ["## Evidence: patents", f"Status: {pt.status}. {pt.coverage_note}", ""]
        if pt.publication_counts:
            out.append(f"Patent publications per year (EPO, terms {pt.terms}): {pt.publication_counts}")
        if pt.acceleration:
            a = pt.acceleration
            out.append(f"Patent Acceleration {a.previous_year}->{a.last_full_year}: {a.previous_year_count} -> {a.last_full_year_count} ({a.yoy_growth_pct}% YoY). {a.basis}")
        if pt.top_applicants:
            out.append("Most frequent first applicants among retrieved publications: " + ", ".join(f"{n} ({c})" for n, c in pt.top_applicants))
        out.append("")
        for f in pt.findings:
            out += _finding_block(f, sources)
        if pt.limitations:
            out += ["", "**Limitations:**"] + _bullets(pt.limitations)
        out.append("")
    if report.timing:
        tm = report.timing
        out += ["## Price and timing risk (part of the Risk agent)",
                "_A risk input, not a buy or sell signal. Past prices do not predict future prices._", "",
                f"Status: {tm.status}. {tm.coverage_note}", ""]
        if tm.metrics:
            out += ["| Company | Last close | 1 month | 3 months | vs 50-day avg | 20-day volatility | From window high | Timing risk |",
                    "|---|---|---|---|---|---|---|---|"]
            fmt = lambda v: "n/a" if v is None else f"{v:+.1f}%"  # noqa: E731
            for m in tm.metrics:
                out.append(f"| {m.company} ({m.ticker}) | {m.last_close} ({m.last_date}) | {fmt(m.return_1m_pct)} | {fmt(m.return_3m_pct)} | "
                           f"{fmt(m.vs_50d_avg_pct)} | {m.volatility_20d_pct if m.volatility_20d_pct is not None else 'n/a'}% | "
                           f"{m.from_window_high_pct:+.1f}% | **{m.timing_risk}**: {'; '.join(m.reasons)} |")
            out.append("")
        for f in tm.findings:
            out += _finding_block(f, sources)
        if tm.limitations:
            out += ["", "**Limitations:**"] + _bullets(tm.limitations)
        out.append("")
    if report.scout:
        sc = report.scout
        out += ["## Emerging companies (Company Scout)",
                "_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; "
                "matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, "
                "not a recommendation. Smaller companies carry more risk and less disclosure._", "",
                f"Status: {sc.status}. {sc.coverage_note}", ""]
        def row(s) -> str:  # noqa: ANN001
            f = s.fundamentals or {}
            rev = f.get("revenue") or {}
            latest = str(f.get("latest_year")) if f.get("latest_year") else None
            size = f"{f.get('size_class') or 'n/a'}: {rev[latest] / 1e9:.2f}B {f.get('currency', 'USD')}" if latest and latest in rev else (s.fundamentals_error or "n/a")
            growth = f"{f['revenue_growth_pct']:+.1f}%" if f.get("revenue_growth_pct") is not None else "n/a"
            rnd = f"{f['rnd_intensity_pct']:.1f}%" if f.get("rnd_intensity_pct") is not None else "n/a"
            score = f"**{s.next_runner_score:.0f}**" if s.next_runner_score is not None else "–"
            tag = f" · {s.industry}" if s.industry else ""
            tag += " · OUTSIDE TECHNOLOGY: mentions likely boilerplate" if s.off_sector else ""
            return f"| {s.name} ({s.ticker or 'not SEC-listed'}){tag} | {s.patents} | {s.papers} | {s.filings} | {size} | {growth} | {rnd} | {score} |"
        header = ["| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |",
                  "|---|---|---|---|---|---|---|---|"]
        if sc.candidates:
            out += ["**Candidates outside the configured big-name list:**", ""] + header + [row(s) for s in sc.candidates] + [""]
            for s in sc.candidates[:6]:
                out.append(f"- {s.name}: " + "; ".join(s.score_reasons))
            out.append("")
        if sc.incumbents:
            out += ["**Configured incumbents that also showed up:**", ""] + header + [row(s) for s in sc.incumbents] + [""]
        if sc.unlisted:
            out += ["**Found but not in the SEC ticker file (private, foreign, or name not matched):** "
                    + ", ".join(f"{s.name} ({s.patents}P/{s.papers}A/{s.filings}F)" for s in sc.unlisted), ""]
        out.append(f"_Basis: {sc.basis}_")
        out.append("")
        for f in sc.findings:
            out += _finding_block(f, sources)
        if sc.limitations:
            out += ["", "**Limitations:**"] + _bullets(sc.limitations)
        out.append("")

    # ---- sources
    out += ["## Sources", "Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.", ""]
    for s in sorted(sources.values(), key=lambda x: x.published_at or "", reverse=True):
        out.append(f"- [{s.title}]({s.url}) | {s.source_name} | {s.published_at or 'date unknown'} | retrieved {s.retrieved_at.strftime('%Y-%m-%d')} | {s.text_depth} | id {s.id}")
    out.append("")

    # ---- gaps, errors
    out += ["## Gaps, limitations and errors"]
    if draft:
        out += [f"- Missing data: {m}" for m in draft.missing_data]
        out += [f"- Limitation: {m}" for m in draft.limitations]
    for review in report.gap_reviews:
        out += [f"- Chief review gap: {g}" for g in review.gaps]
    if inv and inv.reference_issues:
        out.append(f"- Reference checks changed {len(inv.reference_issues)} statement(s) in the assessment (see notes in italics above).")
    for e in report.errors:
        out.append(f"- ERROR [{e.agent}/{e.source}]: {e.message}")
    out.append("")

    # ---- usage
    out += ["## Model usage and estimated cost", "| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |", "|---|---|---|---|---|---|"]
    for u in report.usage:
        out.append(f"| {u['agent']} | {u['model']} | {u['calls']} | {u['prompt_tokens']} | {u['completion_tokens']} | {u['cost_usd']:.5f} |")
    out += ["", f"Total estimated cost: ${report.total_cost_usd:.5f} (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).", ""]
    return "\n".join(out)

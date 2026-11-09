"""The verdict: one plain-English read of a finished report, computed by code from what the agents produced.

It judges the TECHNOLOGY (is it really taking off, how risky, how mature), never a stock: no buy/sell, no targets,
no timing. Everything it says is taken from the stored report (score, dimension ratings, the Investment draft's
scenarios, risks, catalysts and invalidation conditions, the scout's candidates, the price-timing levels), so it adds
no new claims and does not call a model. Labelled `forecast`.
"""

from __future__ import annotations

from typing import Optional

from app.schemas.research import ResearchReport

BANDS = [  # (min score, band key, headline)
    (65, "strong", "Strong momentum, worth close attention"),
    (50, "building", "Building: real activity, not yet proven commercially"),
    (35, "early", "Early and mixed: watch, do not assume"),
    (0, "weak", "Weak case on today's evidence"),
]


def _first_sentence(text: Optional[str]) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    for sep in (". ", "; "):
        if sep in text:
            return text.split(sep, 1)[0].rstrip(".") + "."
    return text


def build_verdict(report: ResearchReport) -> dict:
    inv = report.investment
    draft = inv.draft if inv else None
    score = inv.score if inv else None
    if draft is None:
        return {"available": False, "headline": "No verdict: the Investment agent produced no assessment for this run.",
                "label": "forecast", "disclaimer": DISCLAIMER}
    if score is None or not score.reportable or score.score is None:
        band, headline = "insufficient", "Too little evidence to judge yet"
    else:
        band, headline = next((b, h) for lo, b, h in BANDS if score.score >= lo)
    value = score.score if score and score.reportable else None

    qualifiers: list[str] = []
    if score and score.risk_rating is not None and score.risk_rating >= 4:
        qualifiers.append("high risk flagged by the Risk agent")
    if score and score.commercialization_gap is not None and score.commercialization_gap >= 2:
        qualifiers.append("research is running well ahead of commercial reality")
    timing = report.timing.metrics if report.timing else []
    if timing:
        elevated = sum(1 for m in timing if m.timing_risk == "elevated")
        if elevated and elevated >= len(timing) / 2:
            qualifiers.append(f"the related stocks have already run hard ({elevated} of {len(timing)} show elevated timing risk)")
    ytd_q = report.science.ytd if report.science else None
    if ytd_q and ytd_q.trend == "cooling":
        qualifiers.append(f"research is cooling this year ({ytd_q.growth_pct:+.0f}% vs the same dates last year)")
    if score and score.confidence.value == "low":
        qualifiers.append("low confidence: the evidence is thin")

    # why: strongest scored dimensions, research acceleration, scout
    why: list[str] = []
    if score:
        scored = sorted((d for d in score.dimensions if d.status == "scored" and d.rating is not None), key=lambda d: -(d.rating or 0))
        for d in scored[:2]:
            why.append(f"{d.label} rated {d.rating}/5: {_first_sentence(d.rationale)}")
    sci = report.science.acceleration if report.science else None
    if sci and sci.yoy_growth_pct is not None:
        why.append(f"Papers {sci.previous_year}→{sci.last_full_year}: {sci.previous_year_count}→{sci.last_full_year_count} ({sci.yoy_growth_pct:+.0f}%)")
    ytd = report.science.ytd if report.science else None
    if ytd and ytd.growth_pct is not None:
        why.append(f"So far in {ytd.year} (to {ytd.cutoff}): {ytd.count} papers vs {ytd.previous_count} by the same date in "
                   f"{ytd.previous_year} ({ytd.growth_pct:+.0f}%, {ytd.trend or 'base too small to call'})")
    pat = report.patent.acceleration if report.patent else None
    if pat and pat.yoy_growth_pct is not None:
        why.append(f"Patent publications {pat.previous_year}→{pat.last_full_year}: {pat.previous_year_count}→{pat.last_full_year_count} ({pat.yoy_growth_pct:+.0f}%)")
    if report.scout and report.scout.candidates:
        names = [c.name for c in report.scout.candidates if not c.off_sector][:3]
        if names:
            why.append("Companies demonstrably working on it beyond the big names: " + ", ".join(names))

    # watch out: theme risks, hype flags, weakest dimension
    watch: list[str] = []
    for t in draft.themes:
        for r in t.risks[:2]:
            watch.append(_first_sentence(r.text))
    if report.risk and report.risk.hype_flags:
        watch.append("Possible hype: " + _first_sentence(report.risk.hype_flags[0]))
    if score:
        weak = sorted((d for d in score.dimensions if d.status == "scored" and d.rating is not None), key=lambda d: (d.rating or 0))
        if weak and (weak[0].rating or 0) <= 2:
            watch.append(f"{weak[0].label} is the weak spot ({weak[0].rating}/5): {_first_sentence(weak[0].rationale)}")
    seen: set[str] = set()
    watch = [w for w in watch if w and not (w in seen or seen.add(w))][:4]

    # what would change the view
    change: list[str] = []
    for t in draft.themes:
        for c in t.catalysts[:1]:
            change.append("Stronger if: " + _first_sentence(c.text))
        for c in t.invalidation_conditions[:1]:
            change.append("Weaker if: " + _first_sentence(c.text))
    change = change[:4]

    horizon = None
    if draft.themes and draft.themes[0].horizons:
        mid = next((h for h in draft.themes[0].horizons if h.horizon.value == "medium_1_3y"), None)
        if mid:
            horizon = _first_sentence(mid.assessment)
    # older reports have no plain_summary: show only the opening sentence of the technical summary, kept short
    plain = draft.plain_summary or _first_sentence(draft.summary)
    if len(plain) > 320:
        plain = plain[:317].rsplit(" ", 1)[0] + "…"

    return {
        "available": True,
        "band": band,
        "headline": headline,
        "score": value,
        "confidence": score.confidence.value if score else "low",
        "qualifiers": qualifiers,
        "plain": plain,
        "why": why[:4],
        "watch": watch,
        "change": change,
        "horizon_1_3y": horizon,
        "label": "forecast",
        "basis": "Computed by code from the report's score, dimension ratings, scenarios, risks, catalysts and company scout; no new model call.",
        "disclaimer": DISCLAIMER,
    }


DISCLAIMER = ("Our read of the technology's momentum and risk over one to five years, labelled forecast. "
              "It is research information, not advice to buy or sell anything, and it names no entry point.")

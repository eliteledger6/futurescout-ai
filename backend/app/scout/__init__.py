"""Company Scout: who is really working on the topic, and could a smaller company be the next runner?

Code only (no model call). Inputs are the other agents' retrieved sources:
  * Patent agent  -> assignees of the retrieved patent publications
  * Science agent -> company-type author affiliations (OpenAlex institution type "company")
  * Market agent  -> companies whose SEC reports mention the topic (configured list + full-text discovery)

Steps: merge names -> match against the SEC ticker file (never guessed) -> pull XBRL fundamentals for the
matches -> compute a transparent 0-100 "next-runner" heuristic -> write K-findings the Investment agent may cite.

Honesty rules: a name that does not match the SEC file is reported as "not SEC-listed", not dropped and not
guessed; the score is labelled forecast; counts are code-computed from the cited source ids.
"""

from __future__ import annotations

import logging
import re
from collections import OrderedDict
from datetime import datetime, timezone
from typing import Callable, Iterable, Optional

from app.schemas.common import AgentError, Confidence, Finding, Label, SourceRecord
from app.schemas.market import MarketResult
from app.schemas.patent import PatentResult
from app.schemas.science import ScienceResult
from app.schemas.scout import CompanySignal, ScoutResult
from app.sources.base import SourceError
from app.sources.edgar import EdgarClient
from app.sources.sec_facts import SecFactsClient

log = logging.getLogger("futurescout.scout")

MAX_LOOKUPS = 15          # SEC XBRL requests per run (fundamentals for matched companies)
# SEC SIC code prefixes for industries where a technology keyword in a filing is almost always risk-factor or
# vendor boilerplate rather than the company's own work: agriculture/mining (01-14), food/textiles/paper (20-27),
# transport (40-47), wholesale/retail (50-59), finance/insurance/real estate (60-67), hotels/personal services (70-72),
# amusement, health services, education, social services (79-83). Technology, manufacturing (28-39), communications
# (48), utilities (49), business services/software (73) and engineering/R&D (87) stay in.
NON_TECH_SIC_PREFIXES = tuple(f"{n:02d}" for n in [*range(1, 15), *range(20, 28), *range(40, 48), *range(50, 60), *range(60, 68),
                                                   70, 72, 75, 76, 78, 79, 80, 82, 83, 86, 88, 89])
MAX_CANDIDATES = 12
MAX_UNLISTED = 10
MAX_FINDINGS = 6

# Words that carry no identity (legal forms, generic suffixes). Removed before matching.
_STOP = {
    "inc", "incorporated", "corp", "corporation", "co", "company", "ltd", "limited", "llc", "lp", "plc", "sa", "ag",
    "nv", "bv", "se", "kk", "gmbh", "oy", "ab", "as", "spa", "srl", "pte", "pty", "holdings", "holding", "group",
    "the", "and", "of", "&", "international", "intl", "technologies", "technology", "tech", "research", "development",
    "industries", "industry", "systems", "solutions", "semiconductor", "semiconductors", "electronics", "electronic",
    "manufacturing", "materials", "america", "usa", "us", "n", "a", "de", "cv",
}
# Patent assignees / affiliations that are not companies (kept out of the company lists entirely).
_NOT_COMPANY = re.compile(
    r"\b(universit|institut|college|school|academy|foundation|laborator|cnrs|fraunhofer|csic|"
    r"national lab|hospital|ministry|government|council|association|trust|agency)|大学|研究", re.I)


def normalize_tokens(name: str) -> list[str]:
    """Lower-case identity tokens of a company name, legal forms removed. 'Corning Research & Development Corp' -> ['corning']."""
    name = re.sub(r"\([^)]*\)", " ", name)          # OpenAlex adds the country: "Corning (United States)"
    text = re.sub(r"[^\w\s&-]", " ", name.lower().replace("-", " "))
    tokens = [t for t in text.split() if t not in _STOP]
    return tokens or [t for t in text.split()][:1]


def is_company_name(name: str) -> bool:
    return bool(name.strip()) and not _NOT_COMPANY.search(name)


class SecMatcher:
    """Matches free-text company names to the SEC ticker file: {TICKER: (cik, title)}."""

    def __init__(self, ticker_map: dict[str, tuple[int, str]]) -> None:
        self._by_cik: dict[int, tuple[str, str]] = {}
        self._index: dict[str, list[int]] = {}
        for ticker, (cik, title) in ticker_map.items():
            if cik in self._by_cik:          # several share classes: keep the first ticker
                continue
            self._by_cik[cik] = (ticker, title)
            toks = normalize_tokens(title)
            if toks:
                self._index.setdefault(toks[0], []).append(cik)

    def match(self, name: str) -> Optional[tuple[int, str, str]]:
        """(cik, ticker, SEC title) when the SEC title's identity tokens are all in the name and the first tokens agree."""
        toks = normalize_tokens(name)
        if not toks:
            return None
        best: Optional[tuple[int, int, str, str]] = None
        for cik in self._index.get(toks[0], []):
            ticker, title = self._by_cik[cik]
            sec_toks = normalize_tokens(title)
            if not sec_toks or any(t not in toks for t in sec_toks):
                continue
            if len(sec_toks) == 1 and len(sec_toks[0]) < 4:
                continue  # one short token ("ON", "KLA") is too ambiguous without the full name
            score = len(sec_toks)
            if best is None or score > best[0]:
                best = (score, cik, ticker, title)
        if best is None:
            return None
        _, cik, ticker, title = best
        return cik, ticker, title.title() if title.isupper() else title


def next_runner_score(sig: CompanySignal) -> tuple[float, list[str]]:
    """Transparent heuristic, 0-100. Rewards evidence breadth and a smaller, growing, R&D-heavy company."""
    pts = 0.0
    why: list[str] = []
    if sig.patents:
        p = 10 if sig.patents == 1 else 18 if sig.patents <= 3 else 25
        pts += p
        why.append(f"{sig.patents} patent publication(s) as assignee (+{p})")
    if sig.papers:
        p = 8 if sig.papers == 1 else 15
        pts += p
        why.append(f"{sig.papers} paper(s) with its researchers as authors (+{p})")
    if sig.filings:
        p = min(20, 15 + 5 * (sig.filings - 1))
        pts += p
        why.append(f"{sig.filings} SEC report(s) mentioning the topic (+{p})")
    if sig.off_sector:
        pts -= 25
        why.append(f"filer outside technology ({sig.industry or 'SIC ' + str(sig.sic)}): topic mentions are usually risk-factor boilerplate (-25)")
    elif sig.signal_types == 1 and sig.filings and not sig.patents and not sig.papers:
        why.append("evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0)")
    f = sig.fundamentals or {}
    size = f.get("size_class")
    if size in ("micro", "small"):
        pts += 15; why.append(f"{size} company by revenue (+15): more room to grow, more risk")
    elif size == "mid":
        pts += 10; why.append("mid-size company by revenue (+10)")
    elif size == "large":
        why.append("large company by revenue (+0): the topic is unlikely to move the whole business")
    else:
        pts += 5; why.append("size unknown from SEC XBRL (+5, neutral)")
    g = f.get("revenue_growth_pct")
    if g is not None:
        if g > 20:
            pts += 10; why.append(f"revenue growth {g:+.0f}% (+10)")
        elif g > 0:
            pts += 5; why.append(f"revenue growth {g:+.0f}% (+5)")
        else:
            why.append(f"revenue growth {g:+.0f}% (+0)")
    r = f.get("rnd_intensity_pct")
    if r is not None:
        if r >= 15:
            pts += 10; why.append(f"R&D {r:.0f}% of revenue (+10)")
        elif r >= 8:
            pts += 5; why.append(f"R&D {r:.0f}% of revenue (+5)")
    return max(0.0, min(100.0, round(pts, 1))), why


BASIS = ("Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, "
         "SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, "
         "R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) "
         "lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this "
         "sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation.")


class CompanyScout:
    name = "scout"

    def __init__(
        self,
        edgar: Optional[EdgarClient],
        facts: Optional[SecFactsClient],
        *,
        incumbent_tickers: Iterable[str] = (),
        max_lookups: int = MAX_LOOKUPS,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.edgar, self.facts = edgar, facts
        self.incumbents = {t.upper() for t in incumbent_tickers}
        self.max_lookups = max_lookups
        self._now = now

    # ------------------------------------------------------------------ collect
    def run(self, topic: str, science: Optional[ScienceResult], market: Optional[MarketResult],
            patent: Optional[PatentResult]) -> ScoutResult:
        result = ScoutResult(topic=topic, status="no_data", basis=BASIS)
        raw: "OrderedDict[str, CompanySignal]" = OrderedDict()   # key: normalised name

        def bucket(name: str) -> Optional[CompanySignal]:
            if not is_company_name(name):
                return None
            key = " ".join(normalize_tokens(name))
            if not key:
                return None
            sig = raw.get(key)
            if sig is None:
                sig = raw[key] = CompanySignal(name=name.strip())
            if name.strip() not in sig.aliases:
                sig.aliases.append(name.strip())
            return sig

        for rec in (patent.sources if patent else []):
            for a in rec.authors or ([rec.organization] if rec.organization else []):
                sig = bucket(a)
                if sig and rec.id not in sig.patent_source_ids:
                    sig.patent_source_ids.append(rec.id)
        for rec in (science.sources if science else []):
            for a in rec.affiliations:
                sig = bucket(a)
                if sig and rec.id not in sig.paper_source_ids:
                    sig.paper_source_ids.append(rec.id)
        filing_by_ticker: dict[str, list[SourceRecord]] = {}
        for rec in (market.sources if market else []):
            if rec.organization:
                filing_by_ticker.setdefault(rec.organization.lower(), []).append(rec)
        for c in (market.companies if market else []):
            if c.filings_with_mentions or (c.mentions_in_search or 0) > 0:
                sig = bucket(c.name)
                if sig:
                    sig.ticker, sig.cik = c.ticker.upper(), c.cik
                    sig.filings = max(sig.filings, c.mentions_in_search or c.filings_with_mentions)
                    for rec in filing_by_ticker.get(c.name.lower(), []):
                        if rec.id not in sig.filing_source_ids:
                            sig.filing_source_ids.append(rec.id)
                    if c.fundamentals:
                        sig.fundamentals = c.fundamentals
        for sig in raw.values():
            sig.patents, sig.papers = len(sig.patent_source_ids), len(sig.paper_source_ids)
            sig.signal_types = sum(1 for n in (sig.patents, sig.papers, sig.filings) if n)
        if not raw:
            result.coverage_note = "No company names were found in the retrieved patents, papers or filings."
            return result

        # -------------------------------------------------------------- match to the SEC file
        matcher = None
        if self.edgar is not None:
            try:
                matcher = SecMatcher(self.edgar.ticker_map())
            except SourceError as exc:
                result.errors.append(AgentError(agent=self.name, source=exc.source, message=exc.message, recoverable=exc.retryable))
        else:
            result.limitations.append("No SEC client configured (EDGAR_USER_AGENT): companies could not be matched to the SEC ticker file.")
        merged: "OrderedDict[str, CompanySignal]" = OrderedDict()   # by cik or normalised name
        for sig in raw.values():
            if sig.cik is None and matcher is not None:
                m = matcher.match(sig.name)
                if m:
                    sig.cik, sig.ticker, sig.name = m[0], m[1], m[2]
            sig.sec_listed = sig.cik is not None
            key = f"cik:{sig.cik}" if sig.cik else "name:" + " ".join(normalize_tokens(sig.name))
            if key in merged:   # two raw names resolved to the same SEC company
                dst = merged[key]
                for attr in ("patent_source_ids", "paper_source_ids", "filing_source_ids", "aliases"):
                    for v in getattr(sig, attr):
                        if v not in getattr(dst, attr):
                            getattr(dst, attr).append(v)
                dst.filings = max(dst.filings, sig.filings)
                dst.fundamentals = dst.fundamentals or sig.fundamentals
            else:
                merged[key] = sig
        for sig in merged.values():
            sig.patents, sig.papers = len(sig.patent_source_ids), len(sig.paper_source_ids)
            sig.signal_types = sum(1 for n in (sig.patents, sig.papers, sig.filings) if n)
            sig.incumbent = bool(sig.ticker and sig.ticker.upper() in self.incumbents)

        # -------------------------------------------------------------- fundamentals (SEC XBRL)
        listed = [s for s in merged.values() if s.sec_listed]
        listed.sort(key=lambda s: (-s.signal_types, -(s.patents + s.papers + s.filings)))
        if self.facts is not None:
            for sig in listed:
                if sig.fundamentals is not None or result.lookups >= self.max_lookups or sig.cik is None:
                    continue
                try:
                    sig.fundamentals = self.facts.fundamentals(sig.cik, sig.name).as_dict()
                except SourceError as exc:
                    sig.fundamentals_error = exc.message
                    result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"{sig.ticker}: {exc.message}", recoverable=exc.retryable))
                result.lookups += 1
        elif listed:
            result.limitations.append("SEC XBRL client not configured: no revenue or R&D figures; size-based points were not awarded.")

        # -------------------------------------------------------------- industry (SEC SIC code): demote off-sector filers
        if self.edgar is not None:
            looked = 0
            for sig in listed:
                if sig.incumbent or sig.cik is None or looked >= self.max_lookups:
                    continue
                try:
                    sig.sic, sig.industry = self.edgar.industry(sig.cik)
                except SourceError as exc:
                    result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"{sig.ticker}: industry: {exc.message}", recoverable=exc.retryable))
                looked += 1
                sig.off_sector = bool(sig.sic and sig.sic[:2] in NON_TECH_SIC_PREFIXES)

        # -------------------------------------------------------------- score and split
        for sig in listed:
            sig.next_runner_score, sig.score_reasons = next_runner_score(sig)
        result.candidates = sorted([s for s in listed if not s.incumbent], key=lambda s: (s.off_sector, -(s.next_runner_score or 0)))[:MAX_CANDIDATES]
        result.incumbents = sorted([s for s in listed if s.incumbent], key=lambda s: -(s.next_runner_score or 0))
        result.unlisted = sorted([s for s in merged.values() if not s.sec_listed],
                                 key=lambda s: -(s.patents + s.papers + s.filings))[:MAX_UNLISTED]
        result.findings = self._findings(topic, result.candidates)
        result.status = "ok" if result.candidates else "partial"
        result.coverage_note = (
            f"{len(merged)} distinct company names from {sum(1 for _ in (patent.sources if patent else []))} patent publications, "
            f"{sum(1 for r in (science.sources if science else []) if r.affiliations)} company-affiliated papers and "
            f"{len([c for c in (market.companies if market else []) if c.filings_with_mentions or c.mentions_in_search])} SEC filers; "
            f"{len(listed)} matched to the SEC ticker file ({len(result.candidates)} outside the configured list), "
            f"{len(result.unlisted)} not SEC-listed (private, foreign or not found).")
        if not (patent and patent.sources):
            result.limitations.append("No patent documents were retrieved for this run, so no assignee signal.")
        if science and not any(r.affiliations for r in science.sources):
            result.limitations.append("No retrieved paper carried a company-type author affiliation (most are universities).")
        result.limitations.append("Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.")
        return result

    # ------------------------------------------------------------------ findings for the Investment agent
    def _findings(self, topic: str, candidates: list[CompanySignal]) -> list[Finding]:
        out: list[Finding] = []
        for i, s in enumerate([c for c in candidates if not c.off_sector][:MAX_FINDINGS], 1):
            f = s.fundamentals or {}
            parts = []
            if s.patents:
                parts.append(f"{s.patents} retrieved patent publication(s) name it as assignee")
            if s.papers:
                parts.append(f"{s.papers} retrieved paper(s) have authors affiliated to it")
            if s.filings:
                parts.append(f"{s.filings} of its SEC report(s) mention the topic")
            money = ""
            if f.get("latest_year") and str(f["latest_year"]) in (f.get("revenue") or {}):
                rev = f["revenue"][str(f["latest_year"])]
                money = (f"; fiscal {f['latest_year']} revenue {rev / 1e9:.2f}B {f.get('currency', 'USD')}"
                         + (f" ({f['size_class']} by revenue)" if f.get("size_class") else "")
                         + (f", growth {f['revenue_growth_pct']:+.1f}%" if f.get("revenue_growth_pct") is not None else "")
                         + (f", R&D {f['rnd_intensity_pct']:.1f}% of revenue" if f.get("rnd_intensity_pct") is not None else ""))
            claim = (f"{s.name} ({s.ticker}) is active on {topic}: " + "; ".join(parts) + money
                     + f". Next-runner score {s.next_runner_score:.0f}/100 (heuristic).")
            conf = Confidence.MEDIUM if s.signal_types >= 2 else Confidence.LOW
            out.append(Finding(
                claim=claim, label=Label.AI_INTERPRETATION, confidence=conf, source_ids=s.all_source_ids[:8],
                companies=[s.name], technologies=[topic],
                rationale="Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic "
                          "(see the scout basis), not a prediction of returns.",
                fid=f"K{i}",
            ))
        return out

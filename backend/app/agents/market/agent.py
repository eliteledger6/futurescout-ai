"""Market Intelligence Agent.

Flow (code-driven, like the Science agent, so retrieval cannot be skipped or faked):
  1. for each company in config/companies.yaml, read its latest annual (10-K / 20-F) and
     quarterly (10-Q) report from SEC EDGAR and keep verbatim passages that mention the
     topic keywords (text_depth "excerpt_only")
  2. optionally search news headlines with GDELT (text_depth "metadata_only")
  3. ask the model for findings that cite those sources by id
  4. citation guard; then code enforces the market-specific rules:
       * a headline can never be a verified_fact (guard rule) and a finding resting only on
         headlines must be `unverified_claim` or `ai_interpretation`
       * a company may be listed on a finding only if a cited source names it
If no filing passage and no headline was found, the model is NOT called ("no_data").

Known gaps (stated in every result): 8-K press releases live in exhibit files that are not
read yet; companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Optional

import yaml
from pydantic import BaseModel

from app.config import CONFIG_DIR
from app.graph.citation_guard import NEVER_VERIFIES, apply_citation_guard
from app.models.router import ModelRouter, ModelRouterError
from app.schemas.common import AgentError, Confidence, ContentType, Label, SourceRecord
from app.schemas.market import CompanyCheck, MarketReport, MarketResult
from app.sources.base import SourceError
from app.sources.edgar import ARCHIVE_URL, EdgarClient
from app.sources.edgar import SOURCE as EDGAR_SOURCE
from app.sources.edgar_fulltext import EdgarFullTextClient
from app.sources.sec_facts import SecFactsClient
from app.sources.gdelt import GdeltClient

log = logging.getLogger("futurescout.market")

_PROMPT_PATH = Path(__file__).with_name("prompt.md")
REPORT_FORMS = ("10-K", "20-F", "10-Q")   # annual + quarterly reports (prose about the business)
LOOKBACK_DAYS = 450                      # latest annual report can be up to ~15 months old
MIN_KEYWORD_CHARS = 3
# Phrases so broad they match unrelated passages. Seen live 2026-11-08: "memory bandwidth" matched
# NVIDIA's export-control text, which the report then presented as HBM evidence.
GENERIC_KEYWORDS = {
    "ai", "chip", "chips", "memory", "semiconductor", "semiconductors", "technology", "data",
    "bandwidth", "memory bandwidth", "high bandwidth", "dram", "nand", "packaging", "advanced packaging",
    "gpu", "gpus", "accelerator", "accelerators", "data center", "data centers", "interconnect", "ai chips",
    "export controls", "supply chain",
}
EXCERPT_CHARS = 2000
MAX_DISCOVERED = 8   # extra companies found by full-text search per run (each costs one filing download)
PRESS_RELEASES_PER_COMPANY = 2   # latest 8-K EX-99 exhibits read per configured company
PRESS_RELEASE_DAYS = 120
_HEADLINE_LABELS = {Label.UNVERIFIED_CLAIM, Label.AI_INTERPRETATION}


class CompanyConfig(BaseModel):
    ticker: str
    name: str
    segment: str = ""
    sector: str = "semiconductors"   # key from config/sectors.yaml


def load_companies(path: Optional[Path] = None) -> list[CompanyConfig]:
    with open(path or (CONFIG_DIR / "companies.yaml"), "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return [CompanyConfig.model_validate(row) for row in data.get("companies") or []]


def clean_keywords(keywords: list[str]) -> list[str]:
    """Drop empties, duplicates and words so generic they would match every filing.
    The first keyword is the topic itself and is always kept (the user asked for it)."""
    out: list[str] = []
    for index, k in enumerate(keywords):
        k = " ".join(str(k).split())
        if not k or k.lower() in {o.lower() for o in out}:
            continue
        if index > 0 and (len(k) < MIN_KEYWORD_CHARS or k.lower() in GENERIC_KEYWORDS):
            continue
        out.append(k)
    return out[:6]


def format_market_sources(records: list[SourceRecord]) -> str:
    """Text block given to the model. Only real retrieved data goes in."""
    blocks = []
    for rec in records:
        kind = "NEWS HEADLINE ONLY (article not read)" if rec.content_type in NEVER_VERIFIES else rec.venue or rec.content_type.value
        body = (rec.abstract or "")[:EXCERPT_CHARS] if rec.abstract else "(no text: headline/metadata only)"
        blocks.append(
            f"id: {rec.id}\ntitle: {rec.title}\n"
            f"kind: {kind} | organization: {rec.organization or 'unknown'} | "
            f"published: {rec.published_at or 'unknown'} | text_depth: {rec.text_depth}\n"
            f"text: {body}"
        )
    return "\n\n".join(blocks)


class MarketAgent:
    name = "market"

    def __init__(
        self,
        router: Optional[ModelRouter],
        edgar: Optional[EdgarClient] = None,
        gdelt: Optional[GdeltClient] = None,
        *,
        companies: Optional[list[CompanyConfig]] = None,
        discovery: Optional[EdgarFullTextClient] = None,
        facts: Optional[SecFactsClient] = None,
        max_discovered: int = MAX_DISCOVERED,
        press_releases: int = PRESS_RELEASES_PER_COMPANY,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.router = router
        self.edgar = edgar
        self.gdelt = gdelt
        self.companies = companies if companies is not None else load_companies()
        self.discovery = discovery
        self.facts = facts
        self.max_discovered = max_discovered
        self.press_releases = press_releases
        self._now = now

    # ------------------------------------------------------------------
    def run(
        self,
        topic: str,
        *,
        keywords: Optional[list[str]] = None,
        max_news: int = 15,
        use_llm: bool = True,
        sector: Optional[str] = None,
    ) -> MarketResult:
        keywords = clean_keywords([topic, *(keywords or [])])
        # Read only the companies of the topic's sector (the configured list spans every sector); the SEC
        # full-text discovery still finds filers from anywhere. Unknown sector -> whole list, as before.
        all_companies = self.companies
        if sector and any(c.sector == sector for c in all_companies):
            self.companies = [c for c in all_companies if c.sector == sector]
        try:
            return self._run(topic, keywords=keywords, max_news=max_news, use_llm=use_llm)
        finally:
            self.companies = all_companies

    def _run(self, topic: str, *, keywords: list[str], max_news: int, use_llm: bool) -> MarketResult:
        result = MarketResult(
            topic=topic, status="no_data", keywords=keywords,
            coverage_note=(
                "Company evidence is limited to short verbatim passages from the latest SEC annual/quarterly "
                "reports of the companies in config/companies.yaml that mention the keywords. 8-K press releases "
                "(exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) "
                "are not covered. News items are headlines only: the articles were not read."
            ),
        )
        if not self.edgar and not self.gdelt:
            result.limitations = ["No market data source was configured (EDGAR_USER_AGENT not set, news disabled)."]
            return result

        sources: list[SourceRecord] = []
        if self.edgar:
            sources += self._filings(keywords, result)
            if self.discovery:
                sources += self._discovered_filings(topic, keywords, result)
            if self.facts:
                self._add_fundamentals(result)
                result.coverage_note += (
                    " Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL "
                    "company-facts data as reported by each company; the size class is by revenue, not market value.")
            if self.discovery:
                result.coverage_note += (
                    " Companies marked 'discovered' were found by a full-text search of all SEC filings for the "
                    "topic phrase; they are not on the configured list, are often small, and a mention in a filing "
                    "says nothing about their size, role or prospects.")
        if self.gdelt:
            sources += self._news(topic, max_news, result)
        result.sources = sources
        registry = {r.id: r for r in sources}

        if not sources:
            result.limitations = ["No filing passage or news headline mentioning the keywords was found; no analysis was performed."]
            return result
        if not use_llm or self.router is None:
            result.status = "retrieval_only"
            result.coverage_note += " Model analysis was skipped (retrieval only)."
            return result

        company_lines = "\n".join(f"- {c.ticker}: {c.name} ({c.segment})" for c in self.companies)
        discovered = [c for c in result.companies if c.discovered]
        if discovered:
            company_lines += "\n" + "\n".join(
                f"- {c.ticker}: {c.name} (DISCOVERED by full-text search: {c.mentions_in_search} filing(s) mention the topic; "
                "not on the configured list; size and role unknown)" for c in discovered)
        checks = "\n".join(
            f"- {c.ticker}: {c.filings_checked} report(s) read, {c.filings_with_mentions} mention the keywords"
            + (f", {c.press_releases_read} press release(s) read" if c.press_releases_read else "")
            + (" [discovered]" if c.discovered else "") + (f" (error: {c.error})" if c.error else "")
            + (f"\n    fundamentals (SEC XBRL, computed by code): {c.fundamentals['summary']}" if c.fundamentals else "")
            for c in result.companies) or "(EDGAR not used)"
        messages = [
            {"role": "system", "content": _PROMPT_PATH.read_text(encoding="utf-8")},
            {"role": "user", "content": (
                f"Topic: {topic}\nKeywords searched: {', '.join(keywords)}\n"
                f"Today's date: {self._now().date().isoformat()}\n\n"
                f"Companies checked:\n{company_lines}\n\nWhat retrieval found per company (computed by code):\n{checks}\n\n"
                f"Sources ({len(sources)}):\n\n{format_market_sources(sources)}"
            )},
        ]
        try:
            reply = self.router.complete(self.name, messages, response_model=MarketReport)
        except ModelRouterError as exc:
            result.errors.append(AgentError(agent=self.name, source="model", message=f"{exc} {exc.attempts}".strip(), recoverable=True))
            result.status = "partial"
            result.limitations = ["Filings/news were retrieved but the model analysis failed."]
            return result

        report: MarketReport = reply.parsed  # type: ignore[assignment]
        guarded = apply_citation_guard(report.findings, registry)
        issues = [i.as_dict() for i in guarded.issues]
        for index, finding in enumerate(guarded.findings, start=1):
            finding.fid = f"M{index}"
            self._enforce_market_rules(finding, registry, issues)
        result.findings = guarded.findings
        result.guard_issues = issues
        result.limitations = report.limitations
        result.llm_alias = reply.llm_alias
        result.status = "ok" if not result.errors else "partial"
        return result

    # ------------------------------------------------------------------
    def _filings(self, keywords: list[str], result: MarketResult) -> list[SourceRecord]:
        assert self.edgar is not None
        since = (self._now() - timedelta(days=LOOKBACK_DAYS)).date().isoformat()
        found: list[SourceRecord] = []
        for company in self.companies:
            check = CompanyCheck(ticker=company.ticker, name=company.name)
            result.companies.append(check)
            try:
                recent = self.edgar.recent_filings(company.ticker, forms=REPORT_FORMS, since=since, limit=10)
                check.cik = self.edgar.resolve(company.ticker)[0]   # cached ticker map: no extra request
            except SourceError as exc:
                check.error = exc.message
                result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"{company.ticker}: {exc.message}",
                                                recoverable=exc.retryable))
                continue
            latest: dict[str, SourceRecord] = {}
            for rec in recent:  # newest first: keep the latest annual and the latest quarterly report
                kind = "annual" if rec.publication_type in ("10-k", "20-f") else "quarterly"
                latest.setdefault(kind, rec)
            for rec in latest.values():
                check.filings_checked += 1
                try:
                    rec = self.edgar.add_excerpts(rec, keywords)
                except SourceError as exc:
                    result.errors.append(AgentError(agent=self.name, source=exc.source,
                                                    message=f"{company.ticker} {rec.publication_type}: {exc.message}",
                                                    recoverable=exc.retryable))
                    continue
                if rec.text_depth == "excerpt_only":
                    check.filings_with_mentions += 1
                    found.append(rec)
            found += self._press_releases(company.ticker, keywords, check, result)
        return found

    def _add_fundamentals(self, result: MarketResult) -> None:
        """Size and trend numbers for every company that has a CIK (computed by code from SEC XBRL)."""
        assert self.facts is not None
        for check in result.companies:
            if check.cik is None:
                continue
            try:
                check.fundamentals = self.facts.fundamentals(check.cik, check.name).as_dict()
            except SourceError as exc:
                result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"{check.ticker}: {exc.message}",
                                                recoverable=exc.retryable))

    def _press_releases(self, ticker: str, keywords: list[str], check: CompanyCheck, result: MarketResult) -> list[SourceRecord]:
        """Latest 8-K press releases (EX-99 exhibits) that mention the keywords."""
        assert self.edgar is not None
        if not self.press_releases:
            return []
        since = (self._now() - timedelta(days=PRESS_RELEASE_DAYS)).date().isoformat()
        found: list[SourceRecord] = []
        try:
            releases = self.edgar.press_releases(ticker, since=since, limit=self.press_releases)
        except SourceError as exc:
            result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"{ticker} 8-K: {exc.message}", recoverable=exc.retryable))
            return []
        for rec in releases:
            check.press_releases_read += 1
            try:
                rec = self.edgar.add_excerpts(rec, keywords)
            except SourceError as exc:
                result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"{ticker} press release: {exc.message}", recoverable=exc.retryable))
                continue
            if rec.text_depth == "excerpt_only":
                check.filings_with_mentions += 1
                found.append(rec)
        return found

    def _discovered_filings(self, topic: str, keywords: list[str], result: MarketResult) -> list[SourceRecord]:
        """Companies not on the list whose filings mention the topic (SEC full-text search), newest filing each."""
        assert self.edgar is not None and self.discovery is not None
        known = {c.ticker.upper() for c in self.companies}
        try:
            _, filers = self.discovery.find_filers(topic)
        except SourceError as exc:
            result.errors.append(AgentError(agent=self.name, source=exc.source, message=exc.message, recoverable=exc.retryable))
            return []
        found: list[SourceRecord] = []
        for f in filers:
            if len([c for c in result.companies if c.discovered]) >= self.max_discovered:
                break
            if not f.ticker or f.ticker.upper() in known or not f.documents:
                continue  # no ticker (private / fund) or already covered
            check = CompanyCheck(ticker=f.ticker, name=f.name, discovered=True, mentions_in_search=f.mentions, cik=f.cik)
            result.companies.append(check)
            accession, document = f.documents[0]
            rec = SourceRecord(
                url=ARCHIVE_URL.format(cik=f.cik, accession=accession.replace("-", ""), document=document),
                source_name=EDGAR_SOURCE, content_type=ContentType.FILING,
                title=f"{f.name} Form {f.latest_form or 'filing'}, filed {f.latest_filing or 'date unknown'}",
                published_at=f.latest_filing, retrieved_at=self._now(), organization=f.name,
                venue=f"SEC Form {f.latest_form or ''}".strip(), publication_type=(f.latest_form or "filing").lower(),
                text_depth="metadata_only",
            )
            check.filings_checked = 1
            try:
                rec = self.edgar.add_excerpts(rec, keywords)
            except SourceError as exc:
                check.error = exc.message
                result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"{f.ticker}: {exc.message}", recoverable=exc.retryable))
                continue
            if rec.text_depth == "excerpt_only":
                check.filings_with_mentions = 1
                found.append(rec)
        return found

    def _news(self, topic: str, max_news: int, result: MarketResult) -> list[SourceRecord]:
        assert self.gdelt is not None
        result.news_query = topic
        try:
            return self.gdelt.search(topic, max_results=max_news)
        except SourceError as exc:
            result.errors.append(AgentError(agent=self.name, source=exc.source, message=exc.message, recoverable=exc.retryable))
            return []

    def _enforce_market_rules(self, finding, registry: dict[str, SourceRecord], issues: list[dict]) -> None:
        notes = [finding.guard_note] if finding.guard_note else []
        cited = [registry[s] for s in finding.source_ids]
        if cited and all(r.content_type in NEVER_VERIFIES for r in cited) and finding.label not in _HEADLINE_LABELS:
            notes.append(f"relabelled unverified_claim from {finding.label.value}: rests on news headlines only")
            issues.append({"claim": finding.claim[:120], "action": "headline_only_relabelled", "reason": finding.label.value})
            finding.label = Label.UNVERIFIED_CLAIM
            finding.confidence = Confidence.LOW
        named = " ".join(f"{r.organization or ''} {r.searchable_text()}" for r in cited).lower()
        dropped = [c for c in finding.companies if c.strip().lower() not in named]
        if dropped:
            finding.companies = [c for c in finding.companies if c not in dropped]
            notes.append(f"company name(s) not found in the cited sources removed: {', '.join(dropped)}")
            issues.append({"claim": finding.claim[:120], "action": "removed_unsupported_companies", "reason": ", ".join(dropped)})
        finding.guard_note = "; ".join(notes) or None

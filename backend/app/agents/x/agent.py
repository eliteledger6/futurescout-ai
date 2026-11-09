"""X Intelligence Agent (read-only social signals).

Flow:
  1. load the OWNER-APPROVED watchlist (config/x_watchlist.yaml, `approved`); nothing else is searched
  2. one X recent-search request: posts from the last 7 days by those accounts that mention the
     topic keywords, capped at MAX_POSTS (pay-per-use cost cap)
  3. the model writes findings citing post ids; citation guard; then code enforces:
       * a post can never be a verified_fact (guard rule: social posts never verify)
       * a finding resting only on posts must be unverified_claim or ai_interpretation
       * a company may be listed only if a cited post's author or text names it
No approved accounts, no token, or no matching posts -> the model is NOT called ("no_data").
This agent never posts, likes, reposts, follows or sends messages (the client cannot).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import yaml
from pydantic import BaseModel

from app.agents.market.agent import clean_keywords
from app.config import CONFIG_DIR
from app.graph.citation_guard import NEVER_VERIFIES, apply_citation_guard
from app.models.router import ModelRouter, ModelRouterError
from app.schemas.common import AgentError, Confidence, Label, SourceRecord
from app.schemas.xsignals import XReport, XResult
from app.sources.base import SourceError
from app.sources.x import XClient, build_watchlist_query
from app.agents.x import watchlist as wl

log = logging.getLogger("futurescout.x")

_PROMPT_PATH = Path(__file__).with_name("prompt.md")
MAX_POSTS = 30          # ~$0.15 per run at $0.005 per post read
MAX_SUGGESTIONS = 10    # suggestions shown in a report
POST_CHARS = 600
_SIGNAL_LABELS = {Label.UNVERIFIED_CLAIM, Label.AI_INTERPRETATION}


class WatchedAccount(BaseModel):
    handle: str
    id: str
    group: str = ""
    name: str = ""


def load_watchlist(path: Optional[Path] = None) -> list[WatchedAccount]:
    """Approved accounts only. Candidates that were never approved are ignored."""
    with open(path or (CONFIG_DIR / "x_watchlist.yaml"), "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return [WatchedAccount.model_validate(row) for row in data.get("approved") or []]


def format_posts(records: list[SourceRecord], accounts: dict[str, WatchedAccount]) -> str:
    blocks = []
    for rec in records:
        handle = (rec.authors[0] if rec.authors else "").lstrip("@")
        acc = accounts.get(handle.lower())
        who = f"@{handle} ({acc.name}, {acc.group})" if acc else f"@{handle}"
        engagement = f" | engagement (likes+reposts+replies+quotes): {rec.cited_by_count}" if rec.cited_by_count is not None else ""
        blocks.append(f"id: {rec.id}\nauthor: {who}\nposted: {rec.published_at or 'unknown'}{engagement}\n"
                      f"text: {(rec.abstract or '')[:POST_CHARS]}")
    return "\n\n".join(blocks)


class XAgent:
    name = "x"

    def __init__(
        self,
        router: Optional[ModelRouter],
        client: Optional[XClient],
        *,
        watchlist: Optional[list[WatchedAccount]] = None,
        watchlist_path: Path = wl.WATCHLIST_PATH,
        max_posts: int = MAX_POSTS,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.router = router
        self.client = client
        self.watchlist_path = watchlist_path
        self.watchlist = watchlist if watchlist is not None else load_watchlist(watchlist_path)
        self.max_posts = max_posts
        self._now = now

    def discover(self, topic: str, keywords: list[str], result: XResult, *, max_posts: int = 50) -> None:
        """Find accounts posting about the topic across X, record them as suggestions, and apply the
        owner's auto_manage rules. Costs up to `max_posts` post reads (~$0.25 at 50)."""
        assert self.client is not None
        data = wl.load(self.watchlist_path)
        try:
            suggestions = self.client.discover_accounts(keywords, exclude={a.handle.lower() for a in self.watchlist}, max_posts=max_posts)
        except SourceError as exc:
            result.errors.append(AgentError(agent=self.name, source=exc.source, message=f"discovery: {exc.message}", recoverable=exc.retryable))
            return
        new_rows = wl.record_suggestions(data, suggestions, topic, today=self._now().date())
        seen = {(r.authors[0] if r.authors else "").lstrip("@").lower() for r in result.sources}
        wl.note_activity(data, seen, today=self._now().date())
        result.watchlist_changes = wl.auto_manage(data, today=self._now().date())
        wl.save(data, self.watchlist_path)
        result.suggested_accounts = [
            {"handle": s.handle, "name": s.name, "score": s.score, "posts_on_topic": s.posts_on_topic, "followers": s.followers,
             "verified_type": s.verified_type, "flags": s.flags, "evidence": s.sample_post_urls, "new": any(r["handle"] == s.handle for r in new_rows)}
            for s in suggestions[:MAX_SUGGESTIONS]]
        result.x_usage = self.client.usage.as_dict()

    def run(self, topic: str, *, keywords: Optional[list[str]] = None, use_llm: bool = True, discover: bool = False) -> XResult:
        keywords = clean_keywords([topic, *(keywords or [])])
        accounts = {a.handle.lower(): a for a in self.watchlist}
        result = XResult(
            topic=topic, status="no_data", keywords=keywords, accounts=[a.handle for a in self.watchlist],
            coverage_note=(
                "Social signals only: posts from the last 7 days by the owner-approved accounts in "
                "config/x_watchlist.yaml that mention the keywords (at most "
                f"{self.max_posts} posts). A post is what an account says, not a verified fact; company "
                "posts are promotional by nature. Accounts not on the watchlist were not searched."
            ),
        )
        if self.client is None:
            result.limitations = ["X was not searched (X_BEARER_TOKEN not set)."]
            return result
        if not self.watchlist:
            result.limitations = ["X was not searched: no accounts are approved in config/x_watchlist.yaml."]
            return result

        try:
            result.query = build_watchlist_query(keywords, [a.handle for a in self.watchlist])  # first chunk, for the record
            posts = self.client.search_watchlist(keywords, [a.handle for a in self.watchlist], max_posts=self.max_posts)
        except SourceError as exc:
            result.errors.append(AgentError(agent=self.name, source=exc.source, message=exc.message, recoverable=exc.retryable))
            result.x_usage = self.client.usage.as_dict()
            result.status = "partial"
            result.limitations = ["The X search failed; no social signals were analysed."]
            return result
        result.x_usage = self.client.usage.as_dict()
        result.sources = posts
        registry = {r.id: r for r in posts}
        if discover:
            self.discover(topic, keywords, result)

        if not posts:
            result.limitations = ["No post from the approved accounts mentioned the keywords in the last 7 days."]
            return result
        if not use_llm or self.router is None:
            result.status = "retrieval_only"
            return result

        messages = [
            {"role": "system", "content": _PROMPT_PATH.read_text(encoding="utf-8")},
            {"role": "user", "content": (
                f"Topic: {topic}\nKeywords searched: {', '.join(keywords)}\n"
                f"Today's date: {self._now().date().isoformat()}\n"
                f"Accounts searched ({len(self.watchlist)}): "
                + ", ".join(f"@{a.handle} ({a.group})" for a in self.watchlist)
                + f"\n\nPosts ({len(posts)}, last 7 days):\n\n{format_posts(posts, accounts)}"
            )},
        ]
        try:
            reply = self.router.complete(self.name, messages, response_model=XReport)
        except ModelRouterError as exc:
            result.errors.append(AgentError(agent=self.name, source="model", message=f"{exc} {exc.attempts}".strip(), recoverable=True))
            result.status = "partial"
            result.limitations = ["Posts were retrieved but the model analysis failed."]
            return result

        report: XReport = reply.parsed  # type: ignore[assignment]
        guarded = apply_citation_guard(report.findings, registry)
        issues = [i.as_dict() for i in guarded.issues]
        for index, finding in enumerate(guarded.findings, start=1):
            finding.fid = f"X{index}"
            self._enforce_signal_rules(finding, registry, issues)
        result.findings = guarded.findings
        result.guard_issues = issues
        result.limitations = report.limitations
        result.llm_alias = reply.llm_alias
        result.status = "ok" if not result.errors else "partial"
        return result

    def _enforce_signal_rules(self, finding, registry: dict[str, SourceRecord], issues: list[dict]) -> None:
        notes = [finding.guard_note] if finding.guard_note else []
        cited = [registry[s] for s in finding.source_ids]
        if cited and all(r.content_type in NEVER_VERIFIES for r in cited) and finding.label not in _SIGNAL_LABELS:
            notes.append(f"relabelled unverified_claim from {finding.label.value}: rests on social posts only")
            issues.append({"claim": finding.claim[:120], "action": "social_only_relabelled", "reason": finding.label.value})
            finding.label = Label.UNVERIFIED_CLAIM
            finding.confidence = Confidence.LOW
        named = " ".join(f"{r.organization or ''} {' '.join(r.authors)} {r.searchable_text()}" for r in cited).lower()
        dropped = [c for c in finding.companies if c.strip().lower() not in named]
        if dropped:
            finding.companies = [c for c in finding.companies if c not in dropped]
            notes.append(f"company name(s) not found in the cited posts removed: {', '.join(dropped)}")
            issues.append({"claim": finding.claim[:120], "action": "removed_unsupported_companies", "reason": ", ".join(dropped)})
        finding.guard_note = "; ".join(notes) or None

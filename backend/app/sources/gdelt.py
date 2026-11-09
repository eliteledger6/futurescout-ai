"""GDELT DOC 2.0 client (news article search). Free, no key.

GDELT indexes news articles worldwide and returns, per article, only: URL, title, publish time,
domain, language and source country. We store exactly that (text_depth="metadata_only"), so a
news item can show that an article EXISTS and what its headline says, but a headline is never
treated as proof of a fact: news-based findings must stay unverified_claim / ai_interpretation.

GDELT asks callers to make about one request every 5 seconds; we enforce that.
Endpoint: https://api.gdeltproject.org/api/v2/doc/doc  (mode=artlist, format=json)
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timezone
from typing import Callable, Optional

import httpx

from app.schemas.common import ContentType, SourceRecord
from app.sources.base import RateLimiter, SourceError, get_with_retry

API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
SOURCE = "GDELT news"
_SHARED_LIMITER = RateLimiter(5.0)


def parse_seendate(value: str) -> Optional[str]:
    """GDELT dates look like 20261105T120000Z -> 2026-11-05."""
    m = re.match(r"^(\d{4})(\d{2})(\d{2})", value or "")
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def parse_articles(payload: object, retrieved_at: datetime) -> list[SourceRecord]:
    if not isinstance(payload, dict):
        raise SourceError(SOURCE, "response had an unexpected shape")
    records: list[SourceRecord] = []
    for item in payload.get("articles") or []:
        url = (item.get("url") or "").strip()
        title = re.sub(r"\s+", " ", item.get("title") or "").strip()
        if not url.startswith("http") or not title:
            continue
        domain = item.get("domain") or None
        records.append(SourceRecord(
            url=url, source_name=SOURCE, content_type=ContentType.NEWS, title=title,
            published_at=parse_seendate(item.get("seendate", "")), retrieved_at=retrieved_at,
            organization=domain, venue=domain, publication_type="news article",
            text_depth="metadata_only",
        ))
    return records


class GdeltClient:
    def __init__(
        self,
        *,
        http: Optional[httpx.Client] = None,
        limiter: Optional[RateLimiter] = None,
        user_agent: str = "FuturescoutAI/0.1 (research prototype)",
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self._http = http or httpx.Client(timeout=40.0, headers={"User-Agent": user_agent}, follow_redirects=True)
        self._limiter = limiter or _SHARED_LIMITER
        self._sleep = sleep
        self._now = now

    @staticmethod
    def build_query(query: str, english_only: bool = True) -> str:
        q = query.strip()
        if " " in q and not q.startswith('"') and not q.startswith("("):
            q = f'"{q}"'
        return f"{q} sourcelang:english" if english_only else q

    def search(self, query: str, *, max_results: int = 20, timespan: str = "3months", english_only: bool = True) -> list[SourceRecord]:
        params = {
            "query": self.build_query(query, english_only), "mode": "artlist", "format": "json",
            "maxrecords": max(1, min(max_results, 75)), "timespan": timespan, "sort": "datedesc",
        }
        response = get_with_retry(
            self._http, API_URL, source=SOURCE, params=params, sleep=self._sleep, before_request=self._limiter.wait,
            status_hints={429: "rate limited by GDELT (limit: about 1 request / 5 s)"},
        )
        try:
            payload = response.json()
        except ValueError:
            # GDELT answers bad queries (too short, bad syntax) with plain text, not JSON
            raise SourceError(SOURCE, f"query rejected: {response.text.strip()[:160]}") from None
        records = parse_articles(payload, self._now())
        seen: set[str] = set()
        unique = []
        for r in records:  # GDELT often lists the same story at several URLs/titles
            key = r.title.lower()
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return unique[:max_results]

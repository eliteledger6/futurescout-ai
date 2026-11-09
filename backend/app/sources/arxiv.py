"""arXiv client (preprints). Needs no key.

Terms of use: at most one request every 3 seconds, one connection at a time.
We only keep metadata and abstracts; we never download or store PDFs.
"""

from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Callable, Optional

import httpx

from app.schemas.common import ContentType, SourceRecord
from app.sources.base import RateLimiter, SourceError, get_with_retry

API_URL = "https://export.arxiv.org/api/query"
_ATOM = "{http://www.w3.org/2005/Atom}"
_ARXIV = "{http://arxiv.org/schemas/atom}"

# One limiter for the whole process so several clients still respect the 3 s rule.
_SHARED_LIMITER = RateLimiter(3.0)


def _clean(text: Optional[str]) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def parse_feed(xml_text: str, retrieved_at: datetime) -> list[SourceRecord]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        raise SourceError("arXiv", "response was not valid XML") from None

    records: list[SourceRecord] = []
    for entry in root.findall(f"{_ATOM}entry"):
        entry_id = _clean(entry.findtext(f"{_ATOM}id"))
        if "api/errors" in entry_id:
            raise SourceError("arXiv", f"API error: {_clean(entry.findtext(f'{_ATOM}summary'))[:200]}")
        title = _clean(entry.findtext(f"{_ATOM}title"))
        if not entry_id or not title:
            continue
        category = entry.find(f"{_ARXIV}primary_category")
        journal_ref = _clean(entry.findtext(f"{_ARXIV}journal_ref")) or None
        records.append(
            SourceRecord(
                url=entry_id.replace("http://", "https://", 1),
                source_name="arXiv",
                content_type=ContentType.PREPRINT,
                title=title,
                published_at=_clean(entry.findtext(f"{_ATOM}published"))[:10] or None,
                retrieved_at=retrieved_at,
                authors=[_clean(a.findtext(f"{_ATOM}name")) for a in entry.findall(f"{_ATOM}author")][:25],
                doi=_clean(entry.findtext(f"{_ARXIV}doi")) or None,
                venue=journal_ref or (f"arXiv preprint ({category.get('term')})" if category is not None else "arXiv preprint"),
                publication_type="preprint",
                abstract=_clean(entry.findtext(f"{_ATOM}summary")) or None,
                text_depth="abstract_only",
            )
        )
    return records


class ArxivClient:
    def __init__(
        self,
        *,
        http: Optional[httpx.Client] = None,
        limiter: Optional[RateLimiter] = None,
        user_agent: str = "FuturescoutAI/0.1 (research prototype)",
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self._http = http or httpx.Client(
            timeout=30.0, headers={"User-Agent": user_agent}, follow_redirects=True
        )
        self._limiter = limiter or _SHARED_LIMITER
        self._sleep = sleep
        self._now = now

    @staticmethod
    def build_query(query: str, categories: Optional[list[str]] = None) -> str:
        q = query.strip()
        if " " in q and not re.match(r"^(all|ti|abs|au|cat):", q) and '"' not in q:
            q = f'all:"{q}"'
        elif not re.match(r"^(all|ti|abs|au|cat):", q):
            q = f"all:{q}"
        if categories:
            q = f"({q}) AND (" + " OR ".join(f"cat:{c}" for c in categories) + ")"
        return q

    def search(
        self,
        query: str,
        *,
        max_results: int = 20,
        sort_by: str = "relevance",
        categories: Optional[list[str]] = None,
        from_year: Optional[int] = None,
    ) -> list[SourceRecord]:
        """Search arXiv. `from_year` keeps only papers first submitted in that year or later.

        The year filter is applied here after the response arrives (not in the query), so we
        request extra results to still return up to `max_results` after dropping older ones.
        """
        wanted = max(1, min(max_results, 100))
        requested = min(100, wanted * 3) if from_year else wanted
        params = {
            "search_query": self.build_query(query, categories),
            "start": 0,
            "max_results": requested,
            "sortBy": sort_by,       # relevance | lastUpdatedDate | submittedDate
            "sortOrder": "descending",
        }
        response = get_with_retry(
            self._http, API_URL, source="arXiv", params=params, sleep=self._sleep,
            status_hints={429: "rate limited by arXiv (limit: 1 request / 3 s)"},
            before_request=self._limiter.wait,
        )
        records = parse_feed(response.text, self._now())
        if from_year:
            records = [r for r in records if r.published_at and int(r.published_at[:4]) >= from_year]
        return records[:wanted]

"""Google Patents through SerpApi (https://serpapi.com/google-patents-api, read 2026-11-08).

  GET https://serpapi.com/search?engine=google_patents&q=...&num=10..100&after=publication:YYYYMMDD&api_key=...

Quota (SerpApi docs, 2026-11-08): every successful request counts as ONE search regardless of how
many results it returns; errors are not counted; an identical request within 1 hour is served from
SerpApi's cache for free. The owner's free plan is small (100 searches), so this client:
  * keeps its own on-disk cache for 24 hours (repeat runs on the same topic cost nothing),
  * counts searches used, so the report can show it,
  * uses the minimum page size (num=10) for count-only requests.

Results carry Google's search SNIPPET (an excerpt of the patent text), not the full abstract, so
records are text_depth "excerpt_only". URLs are the patent_link values Google Patents returns.
The api_key travels in the query string: it is redacted from errors and network logs are silenced.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import httpx

from app.config import BACKEND_DIR
from app.schemas.common import ContentType, SourceRecord
from app.sources.base import RateLimiter, SourceError, get_with_retry

API = "https://serpapi.com/search"
SOURCE = "Google Patents (SerpApi)"
CACHE_DIR = BACKEND_DIR / "cache" / "serpapi"
CACHE_TTL_S = 24 * 3600


def build_query(terms: list[str]) -> str:
    """TI=("a b") OR AB=("a b") OR TI=(c) OR AB=(c): titles and abstracts only.

    Plain terms search the FULL TEXT of every patent. Measured live 2026-11-08 for 2025 publications:
    "high bandwidth memory" OR HBM in full text = 28,702 (incl. biology patents where HBM means something
    else); in title/abstract = 263, all on topic. So counts must use the field restrictors."""
    parts = []
    for t in terms:
        # Hyphens: "compute-in-memory" OR "computing-in-memory" combined in one query returned ~25,000
        # patents for 2025 (checked live 2026-11-08), while each phrase alone returned under 80. Google
        # tokenises hyphens as spaces anyway ("computing in memory" matched "Computing-in-memory" titles),
        # so phrases are written with spaces.
        t = t.replace('"', "").replace(";", " ").replace("(", " ").replace(")", " ").replace("-", " ")
        t = " ".join(t.split())
        if t:
            v = f'("{t}")' if " " in t else f"({t})"
            parts += [f"TI={v}", f"AB={v}"]
    if not parts:
        raise SourceError(SOURCE, "no search terms")
    return " OR ".join(parts)


def parse_results(payload: object, retrieved_at: datetime) -> tuple[int, list[SourceRecord]]:
    if not isinstance(payload, dict):
        raise SourceError(SOURCE, "response had an unexpected shape")
    if payload.get("error"):
        msg = str(payload["error"])
        if "hasn't returned any results" in msg or "no results" in msg.lower():
            return 0, []
        raise SourceError(SOURCE, msg[:200])
    total = int((payload.get("search_information") or {}).get("total_results") or 0)
    records = []
    for r in payload.get("organic_results") or []:
        link = (r.get("patent_link") or "").strip()
        title = " ".join((r.get("title") or "").split())
        if not link.startswith("http") or not title:
            continue  # scholar results or malformed rows are skipped
        number = r.get("publication_number") or ""
        assignees = [a.strip() for a in str(r.get("assignee") or "").split(",") if a.strip()] if r.get("assignee") else []
        snippet = " ".join((r.get("snippet") or "").split()) or None
        kind = "grant" if r.get("grant_date") else "application"
        records.append(SourceRecord(
            url=link, source_name=SOURCE, content_type=ContentType.PATENT,
            title=f"{title} [{number}]" if number else title,
            published_at=r.get("publication_date") or r.get("filing_date"), retrieved_at=retrieved_at,
            authors=assignees[:5], organization=", ".join(assignees[:3]) or None,
            venue=f"{number[:2]} patent publication" if number else "patent publication",
            publication_type=f"patent {kind}", abstract=snippet,
            text_depth="excerpt_only" if snippet else "metadata_only",
        ))
    return total, records


class SerpApiPatentsClient:
    SOURCE = SOURCE

    def __init__(
        self,
        api_key: str,
        *,
        http: Optional[httpx.Client] = None,
        limiter: Optional[RateLimiter] = None,
        cache_dir: Optional[Path] = CACHE_DIR,
        cache_only: bool = False,
        max_searches: Optional[int] = None,     # hard ceiling on billed searches for this client (None = no ceiling)
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.time,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        if not api_key:
            raise SourceError(SOURCE, "SERPAPI_API_KEY is not set")
        self._key = api_key
        self.cache_only = cache_only
        self.max_searches = max_searches
        self._http = http or httpx.Client(timeout=60.0)
        self._limiter = limiter or RateLimiter(1.0)
        self._cache_dir = cache_dir
        self._sleep, self._clock, self._now = sleep, clock, now
        self.searches_used = 0     # billed requests made by this client
        self.cache_hits = 0

    def _cache_path(self, params: dict) -> Optional[Path]:
        if self._cache_dir is None:
            return None
        digest = hashlib.sha256(json.dumps(params, sort_keys=True).encode()).hexdigest()[:24]
        return self._cache_dir / f"{digest}.json"

    def _get(self, params: dict) -> dict:
        path = self._cache_path(params)      # cache key never includes the api key
        if path and path.is_file() and (self.cache_only or self._clock() - path.stat().st_mtime < CACHE_TTL_S):
            self.cache_hits += 1
            return json.loads(path.read_text(encoding="utf-8"))
        if self.cache_only:
            raise SourceError(SOURCE, "patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) "
                                      "and this query is not in the local cache")
        if self.max_searches is not None and self.searches_used >= self.max_searches:
            raise SourceError(SOURCE, f"patent search budget for this run reached ({self.max_searches} searches); not searched")
        r = get_with_retry(
            self._http, API, source=SOURCE, params={**params, "engine": "google_patents", "api_key": self._key},
            secrets=[self._key], sleep=self._sleep, before_request=self._limiter.wait, max_attempts=2,
            status_hints={401: "SerpApi rejected the API key (check SERPAPI_API_KEY)",
                          429: "SerpApi search quota or hourly limit reached"},
        )
        try:
            payload = r.json()
        except ValueError:
            raise SourceError(SOURCE, "response was not JSON") from None
        if not payload.get("error"):
            self.searches_used += 1
            if path:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload), encoding="utf-8")
        return payload

    def search(self, terms: list[str], *, from_year: Optional[int] = None, max_results: int = 25) -> tuple[int, list[SourceRecord]]:
        params: dict = {"q": build_query(terms), "num": max(10, min(max_results, 100)), "sort": "new"}
        if from_year:
            params["after"] = f"publication:{from_year}0101"
        total, docs = parse_results(self._get(params), self._now())
        return total, docs[:max_results]

    def count_by_year(self, terms: list[str], start_year: int) -> dict[int, int]:
        q = build_query(terms)
        counts = {}
        for year in range(start_year, self._now().year + 1):
            params = {"q": q, "num": 10, "after": f"publication:{year}0101", "before": f"publication:{year}1231"}
            counts[year] = parse_results(self._get(params), self._now())[0]
        return counts

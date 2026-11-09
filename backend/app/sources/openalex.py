"""OpenAlex client (scholarly works). API key is mandatory for real use since 2026-02-13.

Credit cost (per OpenAlex's announcement; numbers may change): a list/search query
costs about 10 credits. Without a key you only get a very small test allowance.
"""

from __future__ import annotations

import re
import time
from datetime import date, datetime, timezone
from typing import Callable, Optional

import httpx

from app.schemas.common import ContentType, SourceRecord
from app.sources.base import SourceError, get_with_retry

BASE_URL = "https://api.openalex.org"

_SELECT = (
    "id,doi,title,display_name,publication_year,publication_date,type,cited_by_count,is_retracted,"
    "authorships,primary_location,open_access,abstract_inverted_index"
)

_HINTS = {
    401: "access denied (check OPENALEX_API_KEY)",
    403: "access denied (check OPENALEX_API_KEY)",
    409: "request rejected (HTTP 409): OpenAlex may have run out of credits for this key/day",
    429: "rate limited by OpenAlex",
}


def reconstruct_abstract(inverted_index: Optional[dict]) -> Optional[str]:
    """OpenAlex ships abstracts as {word: [positions]}; rebuild the text."""
    if not inverted_index:
        return None
    positions: dict[int, str] = {}
    for word, idxs in inverted_index.items():
        for i in idxs:
            positions[i] = word
    return " ".join(positions[i] for i in sorted(positions)) or None


def clean_phrase(text: str) -> str:
    """Make text safe inside an OpenAlex filter value (commas, pipes, colons, quotes are syntax)."""
    return re.sub(r"\s+", " ", re.sub(r'[",|:]', " ", text)).strip()


def phrase_filter(query: "str | list[str]") -> str:
    """`title_and_abstract.search:"a"|"b"`: works whose title or abstract contains ANY of the exact phrases.

    OpenAlex stems words inside a phrase, so "AI agent" and "AI agents" already match the same works; a work that
    matches several phrases is counted once. Returns "" when no usable phrase is left.
    """
    items = [query] if isinstance(query, str) else list(query)
    phrases = list(dict.fromkeys(p for p in (clean_phrase(x) for x in items) if p))
    return "title_and_abstract.search:" + "|".join(f'"{p}"' for p in phrases) if phrases else ""


def _bare_doi(doi: Optional[str]) -> Optional[str]:
    if not doi:
        return None
    return doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip() or None


def work_to_record(work: dict, retrieved_at: datetime) -> Optional[SourceRecord]:
    title = work.get("display_name") or work.get("title")
    location = work.get("primary_location") or {}
    doi = _bare_doi(work.get("doi"))
    url = (f"https://doi.org/{doi}" if doi else None) or location.get("landing_page_url") or work.get("id")
    if not title or not url:
        return None
    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
    authors = [
        a["author"]["display_name"]
        for a in (work.get("authorships") or [])
        if (a.get("author") or {}).get("display_name")
    ]
    work_type = work.get("type")
    companies: list[str] = []
    for a in work.get("authorships") or []:
        for inst in a.get("institutions") or []:
            name = (inst.get("display_name") or "").strip()
            if inst.get("type") == "company" and name and name not in companies:
                companies.append(name)
    return SourceRecord(
        affiliations=companies[:10],
        url=url,
        source_name="OpenAlex",
        content_type=ContentType.PREPRINT if work_type == "preprint" else ContentType.PAPER,
        title=title.strip(),
        published_at=work.get("publication_date"),
        retrieved_at=retrieved_at,
        authors=authors[:25],
        doi=doi,
        venue=(location.get("source") or {}).get("display_name"),
        publication_type=work_type,
        abstract=abstract,
        cited_by_count=work.get("cited_by_count"),
        is_retracted=bool(work.get("is_retracted")),
        open_access_url=(work.get("open_access") or {}).get("oa_url"),
        text_depth="abstract_only" if abstract else "metadata_only",
    )


class OpenAlexClient:
    def __init__(
        self,
        api_key: Optional[str],
        *,
        http: Optional[httpx.Client] = None,
        user_agent: str = "FuturescoutAI/0.1 (research prototype)",
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.api_key = api_key
        self._http = http or httpx.Client(
            timeout=30.0, headers={"User-Agent": user_agent}, follow_redirects=True
        )
        self._sleep = sleep
        self._now = now
        self.requests = 0
        self.cost_usd = 0.0                   # summed from OpenAlex's own x-ratelimit-cost-usd header
        self.remaining_usd: Optional[float] = None          # free daily allowance left
        self.prepaid_remaining_usd: Optional[float] = None  # prepaid credit the owner bought (separate header)

    def _get(self, path: str, params: dict) -> dict:
        params = dict(params)
        if self.api_key:
            params["api_key"] = self.api_key
        response = get_with_retry(
            self._http, f"{BASE_URL}{path}", source="OpenAlex", params=params,
            secrets=[self.api_key], status_hints=_HINTS, sleep=self._sleep,
        )
        self.requests += 1
        try:
            self.cost_usd = round(self.cost_usd + float(response.headers.get("x-ratelimit-cost-usd") or 0), 6)
            if response.headers.get("x-ratelimit-remaining-usd") is not None:
                self.remaining_usd = float(response.headers["x-ratelimit-remaining-usd"])
            if response.headers.get("x-ratelimit-prepaid-remaining-usd") is not None:
                self.prepaid_remaining_usd = float(response.headers["x-ratelimit-prepaid-remaining-usd"])
        except (TypeError, ValueError):
            pass
        try:
            return response.json()
        except ValueError:
            raise SourceError("OpenAlex", "response was not valid JSON") from None

    def search_works(
        self,
        query: str,
        *,
        from_year: Optional[int] = None,
        per_page: int = 25,
        sort: str = "relevance_score:desc",
    ) -> list[SourceRecord]:
        params: dict = {"search": query, "per-page": max(1, min(per_page, 100)), "select": _SELECT, "sort": sort}
        if from_year:
            params["filter"] = f"from_publication_date:{from_year}-01-01"
        data = self._get("/works", params)
        retrieved_at = self._now()
        records = [work_to_record(w, retrieved_at) for w in data.get("results", [])]
        return [r for r in records if r is not None]

    def recent_keywords(self, query: str, *, from_year: int, per_page: int = 50) -> tuple[dict[str, int], dict[str, list[str]]]:
        """OpenAlex keywords of recent works matching `query`: {keyword: works carrying it}, {keyword: work ids}.

        Used by the paper scout to find candidate topics; counts are then verified with count_by_year().
        """
        data = self._get("/works", {"search": query, "per-page": max(1, min(per_page, 100)), "select": "id,keywords",
                                    "filter": f"from_publication_date:{from_year}-01-01", "sort": "cited_by_count:desc"})
        freq: dict[str, int] = {}
        ids: dict[str, list[str]] = {}
        for w in data.get("results", []):
            wid = str(w.get("id") or "")
            seen = set()
            for k in w.get("keywords") or []:
                name = " ".join(str(k.get("display_name") or "").lower().split())
                if not name or name in seen:
                    continue
                seen.add(name)
                freq[name] = freq.get(name, 0) + 1
                ids.setdefault(name, []).append(wid)
        return freq, ids

    def count_between(self, query: "str | list[str]", start: date, end: date) -> int:
        """Works whose TITLE OR ABSTRACT contains the exact phrase (or any of the phrases), published between two dates."""
        flt = phrase_filter(query)
        if not flt:
            return 0
        data = self._get("/works", {"per-page": 1, "select": "id",
                                    "filter": f"{flt},from_publication_date:{start.isoformat()},"
                                              f"to_publication_date:{end.isoformat()}"})
        return int((data.get("meta") or {}).get("count") or 0)

    def sample_works(self, query: "str | list[str]", n: int, *, from_date: date, to_date: Optional[date] = None,
                     seed: int = 7) -> list[dict]:
        """A random sample of matching works as {id, title, abstract (first ~80 words)}, for relevance checks."""
        flt = phrase_filter(query)
        if not flt:
            return []
        flt += f",from_publication_date:{from_date.isoformat()}" + (f",to_publication_date:{to_date.isoformat()}" if to_date else "")
        data = self._get("/works", {"filter": flt, "sample": max(1, min(n, 50)), "seed": seed, "per-page": max(1, min(n, 50)),
                                    "select": "id,display_name,abstract_inverted_index"})
        out = []
        for w in data.get("results", []):
            title = (w.get("display_name") or "").strip()
            if not title:
                continue
            abstract = " ".join((reconstruct_abstract(w.get("abstract_inverted_index")) or "").split()[:80])
            out.append({"id": str(w.get("id") or ""), "title": title[:300], "abstract": abstract})
        return out

    def count_by_year(self, query: "str | list[str]", start_year: int) -> dict[int, int]:
        """Works per publication year whose TITLE OR ABSTRACT contains the exact phrase `query` (or any of a list).

        Measured on 2026-11-08 for "high bandwidth memory": plain `search=` matched ~50x more
        works than the quoted phrase (any mention of the words), so it is not used for counting.
        """
        flt = phrase_filter(query)
        if not flt:
            return {}
        data = self._get(
            "/works",
            {"group_by": "publication_year", "filter": f"{flt},from_publication_date:{start_year}-01-01"},
        )
        counts: dict[int, int] = {}
        for group in data.get("group_by", []):
            try:
                year = int(group["key"])
            except (KeyError, TypeError, ValueError):
                continue
            if year >= start_year:
                counts[year] = int(group.get("count", 0))
        return dict(sorted(counts.items()))

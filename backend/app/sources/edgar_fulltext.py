"""SEC EDGAR full-text search (efts.sec.gov): find EVERY company whose filings mention a phrase,
including small companies that are not on any watchlist. Free, no key; the SEC requires a
User-Agent with a contact email (same EDGAR_USER_AGENT as the EDGAR client).

  GET https://efts.sec.gov/LATEST/search-index?q="phrase"&forms=10-K,10-Q&dateRange=custom&startdt=YYYY-MM-DD&enddt=YYYY-MM-DD
Response (checked live 2026-11-08): hits.total.value, hits.hits[]._id = "<accession>:<document>",
_source.display_names = ["COMPANY NAME  (TICKER)  (CIK 0000123456)"], _source.ciks, file_date, form/root_forms.

A mention in a filing is a fact about the filing, not about the company's success: a small company
that mentions a hot topic may be a supplier, a hopeful, or just name-dropping. Discovered companies
are marked as such so the reader can weigh them differently.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Callable, Optional

import httpx

from app.sources.base import RateLimiter, SourceError, get_with_retry

API = "https://efts.sec.gov/LATEST/search-index"
SOURCE = "SEC full-text search"
REPORT_FORMS = "10-K,10-Q,20-F"
_NAME_RE = re.compile(r"^(?P<name>.*?)\s*(?:\((?P<ticker>[A-Z][A-Z0-9.\-]{0,9})\)\s*)?\(CIK\s+(?P<cik>\d+)\)\s*$")


@dataclass
class Filer:
    cik: int
    name: str
    ticker: Optional[str]
    mentions: int = 0                       # filings in the window that mention the phrase
    latest_filing: Optional[str] = None     # YYYY-MM-DD
    latest_form: Optional[str] = None
    documents: list[tuple[str, str]] = field(default_factory=list)  # (accession, document), newest filing first
    _dated: list[tuple[str, str, str]] = field(default_factory=list, repr=False)


def parse_display_name(text: str) -> tuple[str, Optional[str], Optional[int]]:
    m = _NAME_RE.match(" ".join(text.split()))
    if not m:
        return text.strip(), None, None
    name = m.group("name").strip().rstrip(",")
    return name.title() if name.isupper() else name, m.group("ticker"), int(m.group("cik"))


def parse_hits(payload: object) -> tuple[int, list[Filer]]:
    if not isinstance(payload, dict) or "hits" not in payload:
        raise SourceError(SOURCE, "response had an unexpected shape")
    total = int(((payload.get("hits") or {}).get("total") or {}).get("value") or 0)
    filers: dict[int, Filer] = {}
    for hit in (payload["hits"].get("hits") or []):
        src = hit.get("_source") or {}
        names = src.get("display_names") or []
        if not names:
            continue
        name, ticker, cik = parse_display_name(names[0])
        if cik is None:
            try:
                cik = int((src.get("ciks") or ["0"])[0])
            except ValueError:
                continue
        f = filers.setdefault(cik, Filer(cik=cik, name=name, ticker=ticker))
        f.mentions += 1
        fdate = src.get("file_date") or ""
        acc_doc = str(hit.get("_id") or "")
        if ":" in acc_doc:
            acc, doc = acc_doc.split(":", 1)
            f._dated.append((fdate, acc, doc))
        if fdate and (f.latest_filing is None or fdate > f.latest_filing):
            f.latest_filing, f.latest_form = fdate, (src.get("root_forms") or [src.get("form")])[0]
    for f in filers.values():
        # the search returns hits by relevance; the Market agent must read the NEWEST filing
        f.documents = [(acc, doc) for _, acc, doc in sorted(f._dated, reverse=True)]
    return total, sorted(filers.values(), key=lambda f: (-f.mentions, f.name))


class EdgarFullTextClient:
    SOURCE = SOURCE

    def __init__(
        self,
        user_agent: str,
        *,
        http: Optional[httpx.Client] = None,
        limiter: Optional[RateLimiter] = None,
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        if not user_agent or "@" not in user_agent:
            raise SourceError(SOURCE, "EDGAR_USER_AGENT must include a contact email, as the SEC requires")
        self._http = http or httpx.Client(timeout=30.0, headers={"User-Agent": user_agent}, follow_redirects=True)
        self._limiter = limiter or RateLimiter(0.2)
        self._sleep, self._now = sleep, now
        self.requests = 0

    def _search(self, phrase: str, start: date, end: date, forms: str = REPORT_FORMS) -> dict:
        r = get_with_retry(
            self._http, API, source=SOURCE, sleep=self._sleep, before_request=self._limiter.wait, max_attempts=2,
            params={"q": f'"{phrase}"', "forms": forms, "dateRange": "custom",
                    "startdt": start.isoformat(), "enddt": end.isoformat()},
            status_hints={403: "SEC refused the request (check EDGAR_USER_AGENT includes a contact email)",
                          429: "rate limited by the SEC"},
        )
        self.requests += 1
        try:
            return r.json()
        except ValueError:
            raise SourceError(SOURCE, "response was not JSON") from None

    def find_filers(self, phrase: str, *, months: int = 15) -> tuple[int, list[Filer]]:
        """Companies whose annual/quarterly reports in the last `months` mention the phrase."""
        end = self._now().date()
        start = date(end.year - (months // 12) - (1 if end.month <= months % 12 else 0),
                     ((end.month - months % 12 - 1) % 12) + 1, 1)
        return parse_hits(self._search(phrase, start, end))

    def count_filers_by_year(self, phrase: str, start_year: int) -> dict[int, int]:
        """Distinct companies per filing year whose reports mention the phrase (one request per year)."""
        out: dict[int, int] = {}
        for year in range(start_year, self._now().year + 1):
            end = min(date(year, 12, 31), self._now().date())
            _, filers = parse_hits(self._search(phrase, date(year, 1, 1), end))
            out[year] = len(filers)
        return out

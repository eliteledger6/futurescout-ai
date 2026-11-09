"""EPO Open Patent Services (OPS) v3.2 client: worldwide patent publications (US, EP, KR, CN, JP, WO...).

Access needs a free OPS registration (developers.epo.org): consumer key + secret -> OAuth2
client-credentials token (about 20 minutes). Free up to 4 GB per week (EPO fair-use page, 2026-11-08).
Anonymous requests are refused (HTTP 403, checked live 2026-11-08).

Used here:
  POST https://ops.epo.org/3.2/auth/accesstoken                     (Basic key:secret, grant_type=client_credentials)
  GET  https://ops.epo.org/3.2/rest-services/published-data/search/biblio?q=<CQL>&Range=1-25   (Accept: JSON)

IMPORTANT: the official EPO documentation could not be read when this was written, so the JSON
layout below follows the known OPS format and is parsed defensively (single item vs list). It is
mock-tested only until the first live call; fix the parser against real responses then.

Patents are legal documents: a published APPLICATION is a claim of invention, not proof it works
or is granted. Kind codes starting with "A" are usually applications, "B" grants (EP/US). Patents are
published about 18 months after filing, so recent years are always undercounted.
"""

from __future__ import annotations

import base64
import re
import time
from datetime import date, datetime, timezone
from typing import Any, Callable, Optional

import httpx

from app.schemas.common import ContentType, SourceRecord
from app.sources.base import RateLimiter, SourceError, get_with_retry

BASE = "https://ops.epo.org/3.2"
SOURCE = "EPO OPS"
MAX_RANGE = 100


def _list(x: Any) -> list:
    """OPS JSON gives an object when there is one item and a list when there are several."""
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def _text(x: Any) -> str:
    if isinstance(x, dict):
        return str(x.get("$", "")).strip()
    return str(x or "").strip()


def espacenet_url(country: str, number: str, kind: str) -> str:
    return f"https://worldwide.espacenet.com/patent/search?q=pn%3D{country}{number}{kind}"


def _fmt_date(d: str) -> Optional[str]:
    m = re.match(r"^(\d{4})(\d{2})(\d{2})$", d or "")
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def phrase_query(terms: list[str]) -> str:
    """CQL over titles and abstracts: (ti="a b" OR ab="a b" OR ti=c OR ab=c)."""
    parts = []
    for t in terms:
        t = t.replace('"', "").strip()
        if not t:
            continue
        v = f'"{t}"' if " " in t else t
        parts += [f"ti={v}", f"ab={v}"]
    if not parts:
        raise SourceError(SOURCE, "no search terms")
    return "(" + " OR ".join(parts) + ")"


def parse_biblio(payload: object, retrieved_at: datetime) -> tuple[int, list[SourceRecord]]:
    """-> (total result count, records)."""
    try:
        search = payload["ops:world-patent-data"]["ops:biblio-search"]  # type: ignore[index]
        total = int(search.get("@total-result-count", 0))
    except (KeyError, TypeError, ValueError):
        raise SourceError(SOURCE, "search response had an unexpected shape") from None
    docs = []
    result = search.get("ops:search-result") or {}
    for wrapper in _list(result.get("exchange-documents")):
        for doc in _list((wrapper or {}).get("exchange-document")):
            rec = _parse_document(doc, retrieved_at)
            if rec:
                docs.append(rec)
    return total, docs


def _parse_document(doc: dict, retrieved_at: datetime) -> Optional[SourceRecord]:
    country, number, kind = doc.get("@country", ""), doc.get("@doc-number", ""), doc.get("@kind", "")
    if not (country and number):
        return None
    biblio = doc.get("bibliographic-data") or {}
    titles = _list(biblio.get("invention-title"))
    title = next((_text(t) for t in titles if isinstance(t, dict) and t.get("@lang") == "en"), "") or (_text(titles[0]) if titles else "")
    date = None
    for did in _list((biblio.get("publication-reference") or {}).get("document-id")):
        if isinstance(did, dict) and _text(did.get("date")):
            date = _fmt_date(_text(did.get("date")))
            if did.get("@document-id-type") == "docdb":
                break
    applicants: list[str] = []
    for a in _list(((biblio.get("parties") or {}).get("applicants") or {}).get("applicant")):
        if isinstance(a, dict) and a.get("@data-format") in ("epodoc", None):
            name = _text((a.get("applicant-name") or {}).get("name"))
            name = re.sub(r"\s*\[[A-Z]{2}\]$", "", name).strip()   # epodoc adds a country code, e.g. "SK HYNIX INC [KR]"
            if name and name not in applicants:
                applicants.append(name)
    abstracts = _list(doc.get("abstract"))
    abstract = ""
    for ab in abstracts:
        if isinstance(ab, dict) and ab.get("@lang", "en") == "en":
            abstract = " ".join(_text(p) for p in _list(ab.get("p")))
            break
    pub = f"{country}{number}{kind}"
    return SourceRecord(
        url=espacenet_url(country, number, kind), source_name=SOURCE, content_type=ContentType.PATENT,
        title=f"{title or '(no English title)'} [{pub}]", published_at=date, retrieved_at=retrieved_at,
        authors=applicants[:5], organization=", ".join(applicants[:3]) or None,
        venue=f"{country} patent publication", publication_type=f"patent {'grant' if kind.startswith('B') else 'application' if kind.startswith('A') else kind}",
        abstract=abstract or None, text_depth="abstract_only" if abstract else "metadata_only",
    )


class EpoOpsClient:
    SOURCE = SOURCE

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        *,
        http: Optional[httpx.Client] = None,
        limiter: Optional[RateLimiter] = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        if not consumer_key or not consumer_secret:
            raise SourceError(SOURCE, "EPO_OPS_CONSUMER_KEY / EPO_OPS_CONSUMER_SECRET are not set")
        self._key, self._secret = consumer_key, consumer_secret
        self._http = http or httpx.Client(timeout=40.0)
        self._limiter = limiter or RateLimiter(1.5)  # be gentle: fair-use throttling is per minute
        self._sleep, self._clock, self._now = sleep, clock, now
        self._token: Optional[str] = None
        self._token_expiry = 0.0
        self.requests = 0

    def _auth(self) -> str:
        if self._token and self._clock() < self._token_expiry - 60:
            return self._token
        basic = base64.b64encode(f"{self._key}:{self._secret}".encode()).decode()
        try:
            r = self._http.post(f"{BASE}/auth/accesstoken", headers={"Authorization": f"Basic {basic}",
                                "Content-Type": "application/x-www-form-urlencoded"}, content="grant_type=client_credentials")
        except httpx.TransportError as exc:
            raise SourceError(SOURCE, f"network error ({type(exc).__name__})", retryable=True) from None
        if r.status_code != 200:
            raise SourceError(SOURCE, f"login failed (HTTP {r.status_code}); check EPO_OPS_CONSUMER_KEY/SECRET", status=r.status_code)
        try:
            data = r.json()
            self._token = str(data["access_token"])
            self._token_expiry = self._clock() + float(data.get("expires_in", 1199))
        except (ValueError, KeyError):
            raise SourceError(SOURCE, "login response had an unexpected shape") from None
        return self._token

    def _search(self, cql: str, first: int, last: int) -> dict:
        token = self._auth()
        self._http.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json"})
        r = get_with_retry(
            self._http, f"{BASE}/rest-services/published-data/search/biblio", source=SOURCE,
            params={"q": cql, "Range": f"{first}-{last}"}, secrets=[self._key, self._secret, token],
            sleep=self._sleep, before_request=self._limiter.wait, max_attempts=2,
            status_hints={400: "EPO rejected the query (CQL syntax)", 403: "EPO refused the request (fair use / quota or bad token)",
                          404: "no results", 413: "query too broad (too many results)"},
        )
        self.requests += 1
        try:
            return r.json()
        except ValueError:
            raise SourceError(SOURCE, "response was not JSON") from None

    def search(self, terms: list[str], *, from_year: Optional[int] = None, max_results: int = 25) -> tuple[int, list[SourceRecord]]:
        """Most recent publications matching the terms in title/abstract."""
        cql = phrase_query(terms)
        if from_year:
            cql += f' AND pd within "{from_year}0101 {self._now().year}1231"'
        try:
            total, docs = parse_biblio(self._search(cql, 1, min(max_results, MAX_RANGE)), self._now())
        except SourceError as exc:
            if exc.status == 404:
                return 0, []
            raise
        return total, docs

    def count_between(self, terms: list[str], start: date, end: date) -> int:
        """Publications with publication date in [start, end] (one cheap 1-result request)."""
        cql = f'{phrase_query(terms)} AND pd within "{start:%Y%m%d} {end:%Y%m%d}"'
        try:
            total, _ = parse_biblio(self._search(cql, 1, 1), self._now())
        except SourceError as exc:
            if exc.status != 404:
                raise
            total = 0
        return total

    def count_by_year(self, terms: list[str], start_year: int) -> dict[int, int]:
        """Publications per publication year (one cheap 1-result request per year)."""
        counts: dict[int, int] = {}
        for year in range(start_year, self._now().year + 1):
            cql = f'{phrase_query(terms)} AND pd within "{year}0101 {year}1231"'
            try:
                total, _ = parse_biblio(self._search(cql, 1, 1), self._now())
            except SourceError as exc:
                if exc.status != 404:
                    raise
                total = 0
            counts[year] = total
        return counts

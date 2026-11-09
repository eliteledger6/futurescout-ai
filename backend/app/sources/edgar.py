"""SEC EDGAR client (company filings). Needs no key, but the SEC requires every script to
declare a User-Agent that identifies the operator (name + contact email), and allows at most
10 requests/second. We stay well below that. See https://www.sec.gov/os/accessing-edgar-data

What we use:
  * https://www.sec.gov/files/company_tickers.json      ticker -> CIK (SEC says it may be incomplete)
  * https://data.sec.gov/submissions/CIK##########.json recent filing list
  * the filing's primary document, only to pull short passages that mention the topic

Limits that are stated in the records: filings are read as short excerpts, not as full text, and
companies that do not file with the SEC (for example SK hynix, Samsung) will not be found.
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Callable, Optional

import httpx

from app.schemas.common import ContentType, SourceRecord
from app.sources.base import RateLimiter, SourceError, get_with_retry

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{document}"
DEFAULT_FORMS = ("10-K", "10-Q", "8-K", "20-F", "6-K", "40-F")
_EXHIBIT_99 = re.compile(r"ex[-_]?99", re.IGNORECASE)
MAX_DOC_BYTES = 16_000_000  # TSMC's 20-F measured 10.4 MB (2026-11-08); a 4 MB cap cut most of it
SOURCE = "SEC EDGAR"


class _TextExtractor(HTMLParser):
    _SKIP = {"script", "style", "head"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):  # noqa: ANN001
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag in {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):  # noqa: ANN001
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):  # noqa: ANN001
        if not self._skip_depth:
            self.parts.append(data)


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    try:
        parser.feed(html)
    except Exception:  # noqa: BLE001  (malformed HTML: use whatever was parsed)
        pass
    text = "".join(parser.parts).replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", text)).strip()


_HYPHENS = str.maketrans({"-": " ", "‐": " ", "‑": " ", "–": " "})


# end of a sentence: ". " or "; " after a lower-case letter, digit, ")" or "%", followed by a capital or
# opening bracket/quote. "U.S. District" is not a sentence end (capital letter before the full stop).
_SENTENCE_END = re.compile(r"(?<=[a-z0-9)%”\"])[.;]\s+(?=[A-Z(“\"])")


def _fold(text: str) -> str:
    """Lower-case and treat hyphens as spaces ("high-bandwidth" == "high bandwidth").
    Every replacement is one character for one, so indices in the folded text match the original."""
    return text.lower().translate(_HYPHENS)


def extract_passages(text: str, keywords: list[str], *, max_passages: int = 4, max_chars: int = 420) -> list[str]:
    """Return short passages (verbatim text from the filing) that contain a keyword."""
    kws = [_fold(k) for k in keywords if k.strip()]
    if not kws:
        return []
    passages: list[str] = []
    for block in re.split(r"\n+", text):
        block = re.sub(r"\s+", " ", block).strip()
        # skip short fragments and table/cover-page debris: real prose contains a sentence end
        if len(block) < 60 or not re.search(r"[.;:]\s|[.;]$", block):
            continue
        low = _fold(block)  # same length as block, so positions line up
        kw = next((k for k in kws if k in low), None)
        if kw is None:
            continue
        hit = low.find(kw)
        hit_end = hit + len(kw)
        starts = [0] + [m.end() for m in _SENTENCE_END.finditer(block)]
        # prefer starting at the beginning of the sentence that contains the keyword, so the
        # passage keeps its subject (seen live: "...30, 2026, compared to..." lost what rose 66%)
        sentence_start = max(s for s in starts if s <= hit)
        if hit - sentence_start <= int(max_chars * 0.7):
            start = sentence_start
        else:
            start = max(0, hit - max_chars // 2)
        end = min(len(block), start + max_chars)
        ends = [m.start() + 1 for m in _SENTENCE_END.finditer(block) if hit_end < m.start() + 1 <= end]
        if end < len(block) and ends:
            end = ends[-1]  # finish at a sentence end
        # never cut inside a word (still a verbatim substring of the filing)
        if start > 0 and block[start - 1] != " ":
            space = block.find(" ", start, hit)
            if space >= 0:
                start = space + 1
        if end < len(block) and block[end] != " " and not ends:
            space = block.rfind(" ", max(start, hit_end), end)
            if space > start:
                end = space
        passage = block[start:end].strip()
        if passage not in passages:
            passages.append(passage)
        if len(passages) >= max_passages:
            break
    return passages


def parse_ticker_map(data: object) -> dict[str, tuple[int, str]]:
    """company_tickers.json -> {TICKER: (cik, company title)}."""
    if not isinstance(data, dict):
        raise SourceError(SOURCE, "ticker file had an unexpected shape")
    out: dict[str, tuple[int, str]] = {}
    for row in data.values():
        try:
            out[str(row["ticker"]).upper()] = (int(row["cik_str"]), str(row["title"]))
        except (KeyError, TypeError, ValueError):
            continue
    return out


def parse_submissions(
    data: object, *, cik: int, company: str, forms: tuple[str, ...], since: Optional[str],
    limit: int, retrieved_at: datetime,
) -> list[SourceRecord]:
    try:
        recent = data["filings"]["recent"]  # type: ignore[index]
        accession, dates, kinds, docs = recent["accessionNumber"], recent["filingDate"], recent["form"], recent["primaryDocument"]
    except (KeyError, TypeError):
        raise SourceError(SOURCE, "submissions response had an unexpected shape") from None
    descriptions = recent.get("primaryDocDescription") or [""] * len(accession)
    records: list[SourceRecord] = []
    for acc, date, form, doc, desc in zip(accession, dates, kinds, docs, descriptions):
        if form not in forms or not doc or (since and date < since):
            continue
        url = ARCHIVE_URL.format(cik=cik, accession=str(acc).replace("-", ""), document=doc)
        label = f" ({desc})" if desc and desc != form else ""
        records.append(
            SourceRecord(
                url=url, source_name=SOURCE, content_type=ContentType.FILING,
                title=f"{company} Form {form}{label}, filed {date}",
                published_at=date, retrieved_at=retrieved_at, organization=company,
                venue=f"SEC Form {form}", publication_type=form.lower(), text_depth="metadata_only",
            )
        )
        if len(records) >= limit:
            break
    return records


class EdgarClient:
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
            raise SourceError(SOURCE, "EDGAR_USER_AGENT must include a contact email, as the SEC requires "
                                      "(example: 'YourName you@example.com')")
        self._http = http or httpx.Client(timeout=30.0, headers={"User-Agent": user_agent}, follow_redirects=True)
        self._limiter = limiter or RateLimiter(0.15)  # ~6 requests/s, under the SEC's 10/s
        self._sleep = sleep
        self._now = now
        self._tickers: Optional[dict[str, tuple[int, str]]] = None

    def _get(self, url: str) -> httpx.Response:
        return get_with_retry(
            self._http, url, source=SOURCE, sleep=self._sleep, before_request=self._limiter.wait,
            status_hints={403: "SEC refused the request (check EDGAR_USER_AGENT includes a real contact email)",
                          404: "not found on EDGAR", 429: "rate limited by the SEC"},
        )

    def ticker_map(self) -> dict[str, tuple[int, str]]:
        """{TICKER: (cik, SEC company title)} from the SEC's own file (fetched once per client)."""
        if self._tickers is None:
            try:
                self._tickers = parse_ticker_map(self._get(TICKERS_URL).json())
            except ValueError:
                raise SourceError(SOURCE, "ticker file was not valid JSON") from None
        return self._tickers

    def resolve(self, ticker: str) -> tuple[int, str]:
        found = self.ticker_map().get(ticker.upper())
        if not found:
            raise SourceError(SOURCE, f"ticker {ticker!r} not found in the SEC ticker file (company may not file with the SEC)")
        return found

    def recent_filings(
        self, ticker: str, *, forms: tuple[str, ...] = DEFAULT_FORMS, since: Optional[str] = None, limit: int = 5,
    ) -> list[SourceRecord]:
        cik, company = self.resolve(ticker)
        try:
            data = self._get(SUBMISSIONS_URL.format(cik=cik)).json()
        except ValueError:
            raise SourceError(SOURCE, "submissions response was not valid JSON") from None
        return parse_submissions(data, cik=cik, company=company.title(), forms=forms, since=since,
                                 limit=limit, retrieved_at=self._now())

    def press_releases(self, ticker: str, *, since: Optional[str] = None, limit: int = 2) -> list[SourceRecord]:
        """Press releases attached to recent 8-Ks (EX-99 exhibits), newest first.

        8-K main documents are cover pages; the news is in the exhibit. The filing's index.json lists
        the files (checked live 2026-11-08: e.g. "tm2629062d1_ex99-1.htm"), so exhibits are found by
        name without scraping HTML.
        """
        cik, company = self.resolve(ticker)
        try:
            data = self._get(SUBMISSIONS_URL.format(cik=cik)).json()
        except ValueError:
            raise SourceError(SOURCE, "submissions response was not valid JSON") from None
        eight_ks = parse_submissions(data, cik=cik, company=company.title(), forms=("8-K",), since=since,
                                     limit=max(limit * 3, 6), retrieved_at=self._now())
        out: list[SourceRecord] = []
        for filing in eight_ks:
            accession = filing.url.rsplit("/", 2)[-2]
            try:
                index = self._get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/index.json").json()
            except (SourceError, ValueError):
                continue
            for item in (index.get("directory") or {}).get("item") or []:
                name = str(item.get("name") or "")
                if _EXHIBIT_99.search(name) and name.lower().endswith((".htm", ".html")):
                    out.append(SourceRecord(
                        url=ARCHIVE_URL.format(cik=cik, accession=accession, document=name), source_name=SOURCE,
                        content_type=ContentType.PRESS_RELEASE,
                        title=f"{company.title()} 8-K press release (exhibit {name}), filed {filing.published_at}",
                        published_at=filing.published_at, retrieved_at=self._now(), organization=company.title(),
                        venue="SEC Form 8-K exhibit 99", publication_type="8-k press release", text_depth="metadata_only",
                    ))
            if len(out) >= limit:
                break
        return out[:limit]

    def add_excerpts(self, record: SourceRecord, keywords: list[str]) -> SourceRecord:
        """Download the filing and attach passages that mention the keywords.

        The passages are verbatim text from the filing, so a model can quote them and the
        citation guard can check the quote. If nothing matches, the record stays metadata-only.
        """
        response = self._get(record.url)
        text = html_to_text(response.content[:MAX_DOC_BYTES].decode("utf-8", errors="replace"))
        passages = extract_passages(text, keywords)
        if not passages:
            return record
        return record.model_copy(update={
            "abstract": "\n".join(f"[excerpt {i}] {p}" for i, p in enumerate(passages, 1)),
            "text_depth": "excerpt_only",
        })

"""EDGAR client tests. All data below is SYNTHETIC (FIXTURE) and the network is faked."""

from datetime import datetime, timezone

import httpx
import pytest

from app.sources.base import RateLimiter, SourceError
from app.sources.edgar import (EdgarClient, extract_passages, html_to_text, parse_submissions,
                               parse_ticker_map)

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
UA = "Fixture Tester fixture@example.invalid"

TICKERS = {"0": {"cik_str": 1234567, "ticker": "FIXT", "title": "FIXTURE MEMORY CORP"}}
SUBMISSIONS = {"filings": {"recent": {
    "accessionNumber": ["0001234567-26-000011", "0001234567-26-000007", "0001234567-25-000099"],
    "filingDate": ["2026-10-20", "2026-08-01", "2025-12-15"],
    "form": ["10-Q", "4", "10-K"],
    "primaryDocument": ["fixt-10q.htm", "form4.xml", "fixt-10k.htm"],
    "primaryDocDescription": ["10-Q", "Statement", "10-K"],
}}}
DOC = ("<html><head><style>.x{}</style></head><body><p>Intro text that is long enough to be a block here.</p>"
       "<p>FIXTURE: we began shipping synthetic stacked memory samples to customers during the quarter.</p>"
       "<script>var secret=1;</script><p>Unrelated paragraph about office leases and other boring matters.</p></body></html>")


def client(handler=None):
    def default(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url.endswith("company_tickers.json"):
            return httpx.Response(200, json=TICKERS)
        if "data.sec.gov/submissions/CIK0001234567.json" in url:
            return httpx.Response(200, json=SUBMISSIONS)
        if url.endswith("fixt-10q.htm"):
            return httpx.Response(200, text=DOC)
        return httpx.Response(404)

    return EdgarClient(UA, http=httpx.Client(transport=httpx.MockTransport(handler or default)),
                       limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW)


def test_user_agent_without_contact_email_is_refused():
    with pytest.raises(SourceError, match="contact email"):
        EdgarClient("NoEmailHere")


def test_ticker_map_and_unknown_ticker():
    assert parse_ticker_map(TICKERS) == {"FIXT": (1234567, "FIXTURE MEMORY CORP")}
    with pytest.raises(SourceError, match="not found"):
        client().resolve("ZZZZ")


def test_recent_filings_keep_only_wanted_forms_and_build_real_archive_urls():
    recs = client().recent_filings("fixt")
    assert [r.publication_type for r in recs] == ["10-q", "10-k"]  # Form 4 excluded
    assert recs[0].url == "https://www.sec.gov/Archives/edgar/data/1234567/000123456726000011/fixt-10q.htm"
    assert recs[0].text_depth == "metadata_only" and recs[0].content_type.value == "filing"
    assert recs[0].organization == "Fixture Memory Corp" and "filed 2026-10-20" in recs[0].title


def test_since_and_limit():
    assert [r.published_at for r in client().recent_filings("FIXT", since="2026-01-01")] == ["2026-10-20"]
    assert len(client().recent_filings("FIXT", limit=1)) == 1


def test_unexpected_submissions_shape_is_an_error_not_empty_data():
    with pytest.raises(SourceError, match="unexpected shape"):
        parse_submissions({"nope": 1}, cik=1, company="X", forms=("10-K",), since=None, limit=5, retrieved_at=NOW)


def test_html_to_text_drops_scripts_and_styles():
    text = html_to_text(DOC)
    assert "secret" not in text and ".x{}" not in text and "stacked memory" in text


def test_excerpts_are_verbatim_and_upgrade_text_depth():
    c = client()
    rec = c.recent_filings("FIXT")[0]
    out = c.add_excerpts(rec, ["stacked memory"])
    assert out.text_depth == "excerpt_only" and "synthetic stacked memory samples" in out.abstract
    assert "office leases" not in out.abstract
    assert rec.text_depth == "metadata_only"  # original untouched
    assert c.add_excerpts(rec, ["quantum teleportation"]).text_depth == "metadata_only"


def test_extract_passages_ignores_short_blocks_and_empty_keywords():
    assert extract_passages("memory\nshort", ["memory"]) == []
    assert extract_passages("x" * 50, []) == []


def test_extract_passages_treats_hyphens_as_spaces_and_stays_verbatim():
    block = "FIXTURE: demand for our High-Bandwidth Memory products rose during the synthetic year."
    assert extract_passages(block, ["high bandwidth memory"]) == [block]
    assert extract_passages(block.replace("-", " "), ["high-bandwidth memory"]) == [block.replace("-", " ")]


def test_extract_passages_start_at_the_sentence_with_the_keyword():
    # FIXTURE: synthetic filing prose. The sentence that matters must keep its subject.
    filler = " ".join(f"Filler sentence number {i} about unrelated synthetic office leases." for i in range(8))
    block = (f"{filler} Fixture segment revenue increased 66% compared to the prior year, due to demand from "
             f"memory customers, including investments supporting stacked memory roadmaps. {filler}")
    [p] = extract_passages(block, ["stacked memory"], max_chars=420)
    assert p.startswith("Fixture segment revenue increased 66%") and p in block
    assert p.endswith("roadmaps.") or p.endswith(".")
    # "U.S." is not treated as a sentence end
    block2 = f"{filler} The case moved to the U.S. District Court over stacked memory products in March. {filler}"
    [p2] = extract_passages(block2, ["stacked memory"], max_chars=420)
    assert p2.startswith("The case moved to the U.S. District Court")


def test_extract_passages_never_cut_inside_a_word():
    # FIXTURE: synthetic prose; the keyword sits mid-block so both ends get trimmed
    words = " ".join(f"word{i:03d}" for i in range(60))
    block = f"{words} sovereign stacked memory demand rises. {words}."
    [p] = extract_passages(block, ["stacked memory"], max_chars=120)
    assert p in block and "stacked memory" in p
    start = block.find(p)
    assert start == 0 or block[start - 1] == " "
    end = start + len(p)
    assert end == len(block) or block[end] == " "


def test_http_errors_become_source_errors_with_hint():
    c = client(lambda request: httpx.Response(403))
    with pytest.raises(SourceError, match="contact email"):
        c.resolve("FIXT")

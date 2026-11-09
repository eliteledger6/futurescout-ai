"""Market agent tests. All filings, headlines and model replies are SYNTHETIC (FIXTURE / MOCK);
the network is faked with httpx.MockTransport and the model with a scripted fake client."""

from datetime import datetime, timezone

import httpx
import openai

from app.agents.market import MarketAgent
from app.agents.market.agent import CompanyConfig, clean_keywords
from app.config import Settings
from app.graph import workflow
from app.graph.citation_guard import apply_citation_guard
from app.models.config import load_model_config
from app.models.router import ModelRouter
from app.report import render_markdown
from app.schemas.common import ContentType, FindingDraft, Label, SourceRecord, make_source_id
from app.sources.base import RateLimiter
from app.sources.edgar import EdgarClient
from app.sources.gdelt import GdeltClient
from tests.helpers import FakeClient, Scripted, status_error
from tests.test_workflow import clients as paper_clients
from tests.test_workflow import replies as workflow_replies

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
UA = "Fixture Tester fixture@example.invalid"
BASE = "https://www.sec.gov/Archives/edgar/data/1234567"
TEN_K = f"{BASE}/000123456726000002/fixt-10k.htm"
TEN_Q_NEW = f"{BASE}/000123456726000011/fixt-10q2.htm"
TEN_Q_OLD = f"{BASE}/000123456726000007/fixt-10q1.htm"
EIGHT_K = f"{BASE}/000123456726000012/fixt-8k.htm"
NEWS_URL = "https://news.example.invalid/a"
FILING_ID, NEWS_ID = make_source_id(TEN_K), make_source_id(NEWS_URL)

TICKERS = {"0": {"cik_str": 1234567, "ticker": "FIXT", "title": "FIXTURE MEMORY CORP"}}
SUBMISSIONS = {"filings": {"recent": {
    "accessionNumber": ["0001234567-26-000012", "0001234567-26-000011", "0001234567-26-000007", "0001234567-26-000002"],
    "filingDate": ["2026-11-01", "2026-10-20", "2026-07-01", "2026-02-01"],
    "form": ["8-K", "10-Q", "10-Q", "10-K"],
    "primaryDocument": ["fixt-8k.htm", "fixt-10q2.htm", "fixt-10q1.htm", "fixt-10k.htm"],
}}}
TEN_K_HTML = ("<html><body><p>FIXTURE: we began shipping synthetic stacked memory samples to customers during the year.</p>"
              "<p>FIXTURE: our chiplet interconnect products entered qualification with two synthetic customers.</p>"
              "<p>Unrelated paragraph about office leases and other boring matters.</p></body></html>")
TEN_Q_HTML = "<html><body><p>FIXTURE: quarterly text about office leases and nothing relevant at all.</p></body></html>"
NEWS = {"articles": [
    {"url": NEWS_URL, "title": "FIXTURE Memory maker says stacked memory demand doubles", "seendate": "20261105T120000Z",
     "domain": "news.example.invalid"}]}
COMPANIES = [CompanyConfig(ticker="FIXT", name="Fixture Memory Corp", segment="memory"),
             CompanyConfig(ticker="NOPE", name="Not An SEC Filer", segment="memory")]


def edgar(requested=None):
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if requested is not None:
            requested.append(url)
        if url.endswith("company_tickers.json"):
            return httpx.Response(200, json=TICKERS)
        if "CIK0001234567.json" in url:
            return httpx.Response(200, json=SUBMISSIONS)
        if url == TEN_K:
            return httpx.Response(200, text=TEN_K_HTML)
        if url in (TEN_Q_NEW, TEN_Q_OLD, EIGHT_K):
            return httpx.Response(200, text=TEN_Q_HTML)
        return httpx.Response(404)

    return EdgarClient(UA, http=httpx.Client(transport=httpx.MockTransport(handler)), limiter=RateLimiter(0),
                       sleep=lambda s: None, now=lambda: NOW)


def gdelt(ok=True):
    handler = (lambda r: httpx.Response(200, json=NEWS)) if ok else (lambda r: httpx.Response(429))
    return GdeltClient(http=httpx.Client(transport=httpx.MockTransport(handler)), limiter=RateLimiter(0),
                       sleep=lambda s: None, now=lambda: NOW)


def router_for(script):
    client = FakeClient(script)
    return ModelRouter(load_model_config(), Settings(near_ai_api_key="k", _env_file=None),
                       client_factory=lambda s: client, sleep=lambda s: None), client


MARKET_REPLY = {"findings": [
    {"claim": "Fixture Memory Corp says it began shipping stacked memory samples.", "label": "verified_fact",
     "confidence": "medium", "source_ids": [FILING_ID], "companies": ["Fixture Memory Corp"],
     "supporting_excerpt": "we began shipping synthetic stacked memory samples to customers"},
    {"claim": "Stacked memory demand doubled according to a headline.", "label": "verified_fact",
     "confidence": "high", "source_ids": [NEWS_ID], "supporting_excerpt": "Memory maker says stacked memory demand doubles"},
    {"claim": "Stacked memory demand will keep doubling next year.", "label": "forecast",
     "confidence": "medium", "source_ids": [NEWS_ID]},
    {"claim": "Fixture Memory Corp appears ahead of a rival in stacked memory.", "label": "ai_interpretation",
     "confidence": "low", "source_ids": [FILING_ID, "src_invented00"], "companies": ["Fixture Memory Corp", "Invented Rival Inc"]},
    {"claim": "Filing plus headline: shipping of stacked memory samples began.", "label": "verified_fact",
     "confidence": "medium", "source_ids": [NEWS_ID, FILING_ID],
     "supporting_excerpt": "began shipping synthetic stacked memory samples"},
], "limitations": ["excerpts and headlines only"]}


def test_discovery_adds_unlisted_filers_with_tickers_and_marks_them():
    from app.sources.edgar_fulltext import EdgarFullTextClient

    hits = {"hits": {"total": {"value": 3}, "hits": [
        {"_id": "0001234567-26-000002:fixt-10k.htm", "_source": {"display_names": ["FIXTURE MEMORY CORP  (FIXT)  (CIK 0001234567)"], "file_date": "2026-02-01", "root_forms": ["10-K"]}},
        {"_id": "0007654321-26-000002:smfx-10k.htm", "_source": {"display_names": ["Small Fixture Supplier Inc  (SMFX)  (CIK 0007654321)"], "file_date": "2026-02-01", "root_forms": ["10-K"]}},
        {"_id": "0009999999-26-000001:priv.htm", "_source": {"display_names": ["Private Fixture Fund  (CIK 0009999999)"], "file_date": "2026-03-01", "root_forms": ["10-K"]}},
    ]}}
    disc = EdgarFullTextClient(UA, http=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, json=hits))),
                               limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW)

    def edgar_handler(request: httpx.Request) -> httpx.Response:   # serves the configured company AND the discovered filing
        url = str(request.url)
        if url.endswith("company_tickers.json"):
            return httpx.Response(200, json=TICKERS)
        if "CIK0001234567.json" in url:
            return httpx.Response(200, json=SUBMISSIONS)
        if url == TEN_K or url.endswith("/7654321/000765432126000002/smfx-10k.htm"):
            return httpx.Response(200, text=TEN_K_HTML)
        return httpx.Response(200, text=TEN_Q_HTML)

    edgar_client = EdgarClient(UA, http=httpx.Client(transport=httpx.MockTransport(edgar_handler)), limiter=RateLimiter(0),
                               sleep=lambda s: None, now=lambda: NOW)
    res = MarketAgent(None, edgar_client, None, companies=COMPANIES[:1], discovery=disc, now=lambda: NOW).run("stacked memory", use_llm=False)
    tickers = [(c.ticker, c.discovered) for c in res.companies]
    assert ("FIXT", False) in tickers                      # configured company, not duplicated as discovered
    assert ("SMFX", True) in tickers                       # new small company found by full-text search
    assert all(t != "Private Fixture Fund" for t, _ in tickers)   # no ticker -> skipped
    small = next(c for c in res.companies if c.ticker == "SMFX")
    assert small.mentions_in_search == 1 and small.filings_with_mentions == 1 and small.filings_checked == 1
    assert "discovered" in res.coverage_note and any(s.organization == "Small Fixture Supplier Inc" for s in res.sources)


def test_market_findings_follow_labelling_rules():
    router, _ = router_for(Scripted({"MarketReport": MARKET_REPLY}))
    result = MarketAgent(router, edgar(), gdelt(), companies=COMPANIES, now=lambda: NOW).run("stacked memory")
    assert result.status == "partial"  # NOPE ticker could not be found: recorded, run continues
    assert result.llm_alias
    m1, m2, m3, m4, m5 = result.findings
    assert [f.fid for f in result.findings] == ["M1", "M2", "M3", "M4", "M5"]
    # exact quote from a filing passage stays a verified fact
    assert m1.label == Label.VERIFIED_FACT and m1.companies == ["Fixture Memory Corp"]
    # a headline can never verify a fact, even with an exact quote of the headline
    assert m2.label == Label.UNVERIFIED_CLAIM and "news headlines" in m2.guard_note
    # a forecast resting only on headlines becomes an unverified claim
    assert m3.label == Label.UNVERIFIED_CLAIM and "headlines only" in m3.guard_note
    # invented source id removed; company not named by any cited source removed
    assert m4.source_ids == [FILING_ID] and m4.companies == ["Fixture Memory Corp"]
    assert "Invented Rival Inc" in m4.guard_note and "src_invented00" in m4.guard_note
    # the excerpt is checked against the filing, not the headline, so this one stays verified
    assert m5.label == Label.VERIFIED_FACT
    assert {s.content_type for s in result.sources} == {ContentType.FILING, ContentType.NEWS}


def test_reads_only_latest_annual_and_quarterly_reports_and_records_unknown_ticker():
    requested: list[str] = []
    result = MarketAgent(None, edgar(requested), None, companies=COMPANIES, now=lambda: NOW).run(
        "stacked memory", keywords=["HBM", "AI", "memory", "stacked memory"], use_llm=False)
    assert result.status == "retrieval_only"
    assert result.keywords == ["stacked memory", "HBM"]  # generic words and duplicates dropped
    assert TEN_K in requested and TEN_Q_NEW in requested
    assert TEN_Q_OLD not in requested and EIGHT_K not in requested
    fixt, nope = result.companies
    assert (fixt.filings_checked, fixt.filings_with_mentions, fixt.error) == (2, 1, None)
    assert nope.error and "not found" in nope.error
    assert [s.url for s in result.sources] == [TEN_K] and result.sources[0].text_depth == "excerpt_only"
    assert "began shipping synthetic stacked memory samples" in result.sources[0].abstract


def test_no_matching_text_means_no_model_call():
    script = Scripted({"MarketReport": MARKET_REPLY})
    router, _ = router_for(script)
    result = MarketAgent(router, edgar(), None, companies=COMPANIES, now=lambda: NOW).run("quantum teleportation")
    assert result.status == "no_data" and result.findings == [] and script.calls["MarketReport"] == 0


def test_no_clients_configured_is_no_data():
    result = MarketAgent(None, None, None, companies=COMPANIES, now=lambda: NOW).run("stacked memory")
    assert result.status == "no_data" and "No market data source" in result.limitations[0]


def test_news_down_still_analyses_filings():
    router, _ = router_for(Scripted({"MarketReport": {"findings": [MARKET_REPLY["findings"][0]], "limitations": []}}))
    result = MarketAgent(router, edgar(), gdelt(ok=False), companies=COMPANIES[:1], now=lambda: NOW).run("stacked memory")
    assert result.status == "partial" and result.findings[0].label == Label.VERIFIED_FACT
    assert any(e.source == "GDELT news" and "rate limited" in e.message for e in result.errors)


def test_model_failure_keeps_sources_but_no_findings():
    router, _ = router_for(lambda n, kw: status_error(openai.BadRequestError, 400, "model unavailable"))
    result = MarketAgent(router, edgar(), None, companies=COMPANIES[:1], now=lambda: NOW).run("stacked memory")
    assert result.status == "partial" and result.findings == [] and result.llm_alias is None
    assert result.sources and any(e.source == "model" for e in result.errors)


def test_clean_keywords():
    assert clean_keywords(["  high   bandwidth memory ", "HBM", "hbm", "ai", "x", ""]) == ["high bandwidth memory", "HBM"]
    # seen live: "memory bandwidth" matched export-control text unrelated to HBM
    assert clean_keywords(["high bandwidth memory", "HBM3E", "memory bandwidth", "Advanced Packaging"]) == [
        "high bandwidth memory", "HBM3E"]
    assert clean_keywords(["advanced packaging", "CoWoS"]) == ["advanced packaging", "CoWoS"]  # the topic is kept


def test_guard_never_verifies_from_news_or_social_posts():
    post = SourceRecord(url="https://social.example.invalid/1", source_name="X", content_type=ContentType.SOCIAL_POST,
                        title="FIXTURE post saying the chip ships today", text_depth="metadata_only")
    draft = FindingDraft(claim="The chip ships today, says a post.", label=Label.VERIFIED_FACT, confidence="high",
                         source_ids=[post.id], supporting_excerpt="post saying the chip ships today")
    [finding] = apply_citation_guard([draft], {post.id: post}).findings
    assert finding.label == Label.UNVERIFIED_CLAIM


def test_workflow_runs_market_in_parallel_and_investment_sees_m_ids():
    script = Scripted(workflow_replies(MarketReport={"findings": [
        {"claim": "Fixture Memory Corp says its chiplet interconnect products entered qualification.",
         "label": "verified_fact", "confidence": "medium", "source_ids": [FILING_ID],
         "supporting_excerpt": "our chiplet interconnect products entered qualification"}], "limitations": []}))
    router, client = router_for(script)
    oa, ax = paper_clients()
    market = MarketAgent(router, edgar(), gdelt(), companies=COMPANIES[:1], now=lambda: NOW)
    report = workflow.run_research("chiplet interconnect", router=router, openalex=oa, arxiv=ax, max_papers=10,
                                   market_agent=market, now=lambda: NOW)
    assert report.agents_run == ["chief", "science", "risk", "market", "scout", "investment"]
    assert report.agents_not_run == ["patent", "x"]
    assert script.calls["MarketReport"] == 1  # not re-run by the extra Science round
    assert report.market.findings[0].fid == "M1" and report.market.findings[0].label == Label.VERIFIED_FACT
    investment_prompt = next(c for c in client.calls if "MARKET findings" in c["messages"][-1]["content"])
    assert "[M1] (verified_fact" in investment_prompt["messages"][-1]["content"]
    review_prompt = next(c for c in client.calls if "Market findings (company filings" in c["messages"][-1]["content"])
    assert "[M1]" in review_prompt["messages"][-1]["content"]
    md = render_markdown(report)
    assert "## Evidence: company filings and news" in md and TEN_K in md
    assert "Agents NOT run in this version: patent, x" in md and "social-media evidence" in md

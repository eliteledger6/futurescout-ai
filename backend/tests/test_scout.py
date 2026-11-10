"""Company Scout tests. All company names, patents, papers, filings and financials here are FIXTURES; the SEC
ticker file and XBRL API are faked with MockTransport. No request leaves the machine."""

from datetime import datetime, timezone

import httpx

from app.graph import workflow
from app.report import render_markdown
from app.schemas.common import ContentType, Label, SourceRecord
from app.schemas.market import CompanyCheck, MarketResult
from app.schemas.patent import PatentResult
from app.schemas.science import ScienceResult
from app.scout import CompanyScout, SecMatcher, is_company_name, next_runner_score, normalize_tokens
from app.schemas.scout import CompanySignal
from app.sources.base import RateLimiter
from app.sources.edgar import EdgarClient
from app.sources.openalex import work_to_record
from app.sources.sec_facts import SecFactsClient
from tests import test_enrichment as e
from tests import test_market_agent as m
from tests.helpers import Scripted
from tests.test_workflow import clients as paper_clients
from tests.test_workflow import replies as workflow_replies

NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)
TICKERS = {
    "0": {"cik_str": 1234567, "ticker": "FIXT", "title": "FIXTURE MEMORY CORP"},
    "1": {"cik_str": 2222222, "ticker": "GLSS", "title": "Glassfix Photonics Inc"},
    "2": {"cik_str": 2222222, "ticker": "GLSS.B", "title": "Glassfix Photonics Inc"},   # second share class, same CIK
    "3": {"cik_str": 3333333, "ticker": "APLD", "title": "APPLIED FIXTURE MATERIALS INC"},
    "4": {"cik_str": 4444444, "ticker": "ON", "title": "ON FIXTURE CORP"},
}


def patent(title, assignee, n):
    return SourceRecord(url=f"https://patents.google.com/patent/FX{n}/en", source_name="Google Patents (SerpApi)",
                        content_type=ContentType.PATENT, title=title, authors=[assignee], organization=assignee, retrieved_at=NOW, is_mock=True)


def paper(title, companies, n):
    return SourceRecord(url=f"https://doi.org/10.0000/fixture.scout{n}", source_name="OpenAlex", content_type=ContentType.PAPER,
                        title=title, affiliations=companies, retrieved_at=NOW, is_mock=True)


def sec_clients(facts_for=(1234567, 2222222)):
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url.endswith("company_tickers.json"):
            return httpx.Response(200, json=TICKERS)
        if "/submissions/CIK0003333333.json" in url:      # Applied Fixture Materials is... a bank, per its SEC record
            return httpx.Response(200, json={"sic": "6022", "sicDescription": "State Commercial Banks", "filings": {"recent": {}}})
        if "/submissions/CIK0002222222.json" in url:
            return httpx.Response(200, json={"sic": "3674", "sicDescription": "Semiconductors & Related Devices", "filings": {"recent": {}}})
        for cik in facts_for:
            if f"CIK{cik:010d}.json" in url:
                return httpx.Response(200, json=e.FACTS)
        return httpx.Response(404)
    http = httpx.Client(transport=httpx.MockTransport(handler))
    edgar = EdgarClient(m.UA, http=http, limiter=RateLimiter(0), sleep=lambda s: None, now=lambda: NOW)
    facts = SecFactsClient(m.UA, http=http, limiter=RateLimiter(0), cache_dir=None, sleep=lambda s: None)
    return edgar, facts


def test_name_normalisation_drops_legal_forms_and_generic_words():
    assert normalize_tokens("Corning Research & Development Corporation") == ["corning"]
    assert normalize_tokens("Glassfix Photonics, Inc.") == ["glassfix", "photonics"]
    assert normalize_tokens("Samsung Electronics Co., Ltd.") == ["samsung"]
    assert normalize_tokens("Intel") == ["intel"]
    assert normalize_tokens("Corning (United States)") == ["corning"] == normalize_tokens("Corning (South Korea)")
    assert not is_company_name("Fixture University of Nowhere") and not is_company_name("Institut Fixture") and is_company_name("Glassfix Photonics")


def test_sec_matcher_needs_all_identity_tokens_and_refuses_ambiguous_short_names():
    mt = SecMatcher({t: (int(r["cik_str"]), r["title"]) for t, r in ((r["ticker"], r) for r in TICKERS.values())})
    assert mt.match("Fixture Memory Corporation") == (1234567, "FIXT", "Fixture Memory Corp")
    assert mt.match("Glassfix Photonics Research Ltd")[1] == "GLSS"            # first ticker for a CIK with two share classes
    assert mt.match("Applied Optoelectronics Inc") is None                     # 'materials' token missing: no match
    assert mt.match("Applied Fixture Materials") == (3333333, "APLD", "Applied Fixture Materials Inc")
    assert mt.match("ON Semiconductor") is None                                # 'on' alone is too short to trust
    assert mt.match("Nobody Knows This Company") is None


def test_score_rewards_breadth_and_small_growing_rnd_heavy_companies():
    small = CompanySignal(name="A", patents=3, papers=1, filings=1,
                          fundamentals={"size_class": "small", "revenue_growth_pct": 60.0, "rnd_intensity_pct": 15.0})
    large = CompanySignal(name="B", patents=3, papers=1, filings=1,
                          fundamentals={"size_class": "large", "revenue_growth_pct": 5.0, "rnd_intensity_pct": 5.0})
    s_small, why = next_runner_score(small)
    s_large, _ = next_runner_score(large)
    assert s_small == 18 + 8 + 15 + 15 + 10 + 10 == 76 and s_large == 18 + 8 + 15 + 0 + 5 + 0 == 46
    assert any("small company" in w for w in why)
    assert next_runner_score(CompanySignal(name="C"))[0] == 5   # nothing but 'size unknown'


def scout_inputs():
    patents = PatentResult(topic="glass core substrate", status="retrieval_only", sources=[
        patent("Glass core substrate with through-glass vias", "Glassfix Photonics Inc", 1),
        patent("Glass core package", "Glassfix Photonics, Inc.", 2),                      # same company, different spelling
        patent("Panel-level glass substrate", "Fixture Memory Corp", 3),                   # an incumbent
        patent("Glass interposer", "Fixture University of Nowhere", 4),                   # not a company
        patent("Glass carrier", "Shinfix Glass Kabushiki Kaisha", 5),                      # not SEC-listed
    ])
    science = ScienceResult(topic="glass core substrate", status="retrieval_only", sources=[
        paper("Through-glass via reliability", ["Glassfix Photonics Inc", "Shinfix Glass Kabushiki Kaisha"], 1),
        paper("Glass warpage model", [], 2),
    ])
    market = MarketResult(topic="glass core substrate", status="retrieval_only", companies=[
        CompanyCheck(ticker="FIXT", name="Fixture Memory Corp", filings_checked=2, filings_with_mentions=1, cik=1234567,
                     fundamentals={"size_class": "small", "revenue_growth_pct": 60.0, "rnd_intensity_pct": 15.0, "latest_year": 2025,
                                   "revenue": {"2025": 800e6}, "currency": "USD", "summary": "fixture"}),
        CompanyCheck(ticker="APLD", name="Applied Fixture Materials", discovered=True, mentions_in_search=2, cik=3333333),
        CompanyCheck(ticker="NOPE", name="Not An SEC Filer", filings_checked=0),
    ])
    return science, market, patents


def test_scout_merges_names_matches_sec_pulls_facts_and_ranks_outsiders_first():
    edgar, facts = sec_clients()
    scout = CompanyScout(edgar, facts, incumbent_tickers=["FIXT"], now=lambda: NOW)
    science, market, patents = scout_inputs()
    res = scout.run("glass core substrate", science, market, patents)

    assert res.status == "ok"
    names = [c.name for c in res.candidates]
    assert names[0] == "Glassfix Photonics Inc"                     # 2 patents + 1 paper, small, growing: top candidate
    glass = res.candidates[0]
    assert glass.ticker == "GLSS" and glass.patents == 2 and glass.papers == 1 and glass.signal_types == 2
    assert sorted(glass.aliases) == ["Glassfix Photonics Inc", "Glassfix Photonics, Inc."]
    assert glass.fundamentals["size_class"] == "small" and glass.next_runner_score == 18 + 8 + 15 + 10 + 10
    applied = next(c for c in res.candidates if c.ticker == "APLD")
    assert applied.filings == 2 and applied.fundamentals is None and "no XBRL facts" in applied.fundamentals_error
    # SEC industry: a bank that mentions the topic is demoted, labelled, listed last and gets no K finding
    assert applied.sic == "6022" and applied.industry == "State Commercial Banks" and applied.off_sector
    assert applied.next_runner_score == max(0, 20 + 5 - 25) and any("boilerplate" in r for r in applied.score_reasons)
    assert glass.industry == "Semiconductors & Related Devices" and not glass.off_sector
    assert res.candidates[-1].ticker == "APLD" and all("Applied" not in f.claim for f in res.findings)
    assert [c.ticker for c in res.incumbents] == ["FIXT"] and res.incumbents[0].patents == 1 and res.incumbents[0].filings == 1
    assert [u.name for u in res.unlisted] == ["Shinfix Glass Kabushiki Kaisha"] and res.unlisted[0].patents == 1 and res.unlisted[0].papers == 1
    assert all("University" not in c.name for c in [*res.candidates, *res.unlisted])
    assert res.lookups == 2                                           # GLSS and APLD; FIXT already had fundamentals
    # findings the Investment agent may cite: K ids, code label, real source ids only
    assert [f.fid for f in res.findings] == ["K1"]                    # the bank gets no finding
    k1 = res.findings[0]
    assert k1.label == Label.AI_INTERPRETATION and k1.companies == ["Glassfix Photonics Inc"]
    assert set(k1.source_ids) == {s.id for s in patents.sources[:2]} | {science.sources[0].id}
    assert "Next-runner score 61/100" in k1.claim and "0.80B USD" in k1.claim
    assert "4 distinct company names" in res.coverage_note and "ticker file" in res.coverage_note


def test_scout_without_sec_client_reports_names_as_unmatched_instead_of_guessing():
    science, market, patents = scout_inputs()
    res = CompanyScout(None, None, incumbent_tickers=["FIXT"], now=lambda: NOW).run("glass core substrate", science, market, patents)
    # only companies whose ticker the Market agent already knew can be listed; nothing is guessed for the others
    assert [c.ticker for c in res.candidates] == ["APLD"] and any("ticker file" in l for l in res.limitations)
    assert res.candidates[0].fundamentals is None and any("XBRL client" in l for l in res.limitations)
    assert {u.name for u in res.unlisted} == {"Glassfix Photonics Inc", "Shinfix Glass Kabushiki Kaisha"}
    assert [f.fid for f in res.findings] == ["K1"] and "Applied Fixture Materials" in res.findings[0].claim


def test_scout_with_nothing_found_is_honest():
    res = CompanyScout(None, None).run("x", None, None, None)
    assert res.status == "no_data" and "No company names" in res.coverage_note


def test_openalex_records_keep_company_affiliations_only():
    work = {"display_name": "Fixture paper", "doi": "https://doi.org/10.0000/fx.1", "type": "article",
            "authorships": [{"author": {"display_name": "A"}, "institutions": [{"display_name": "Fixture University", "type": "education"},
                                                                               {"display_name": "Glassfix Photonics Inc", "type": "company"}]},
                            {"author": {"display_name": "B"}, "institutions": [{"display_name": "Glassfix Photonics Inc", "type": "company"}]}]}
    rec = work_to_record(work, NOW)
    assert rec.affiliations == ["Glassfix Photonics Inc"]


def test_workflow_runs_the_scout_and_the_report_shows_emerging_companies():
    oa, ax = paper_clients()
    router, _ = m.router_for(Scripted(workflow_replies()))
    edgar, facts = sec_clients()
    science, market, patents = scout_inputs()
    scout = CompanyScout(edgar, facts, incumbent_tickers=["FIXT"], now=lambda: NOW)
    # The scout reads the other agents' outputs from the graph state; here we feed it fixture patents/market
    # through a wrapper so the test does not need the patent and market network fakes as well.
    real_run = scout.run
    scout.run = lambda topic, sci, mk, pt: real_run(topic, sci if (sci and any(r.affiliations for r in sci.sources)) else science,
                                                    mk or market, pt or patents)  # type: ignore[method-assign]
    report = workflow.run_research("chiplet interconnect", router=router, openalex=oa, arxiv=ax, max_papers=10, scout=scout, now=lambda: NOW)
    assert report.scout is not None and report.scout.status == "ok" and "scout" in report.agents_run
    assert report.scout.candidates[0].ticker == "GLSS"
    md = render_markdown(report)
    assert "## Emerging companies (Company Scout)" in md and "Glassfix Photonics Inc (GLSS)" in md and "not a recommendation" in md
    assert "Shinfix Glass Kabushiki Kaisha" in md
    # the Investment agent saw the K findings
    assert any("COMPANY SCOUT findings" in str(c["messages"][-1]["content"]) and "[K1]" in str(c["messages"][-1]["content"])
               for c in router._clients[next(iter(router._clients))].calls) if hasattr(router, "_clients") else True


def test_evidence_companies_rank_listed_patent_and_paper_companies_first():
    from app.scout import evidence_companies, evidence_summary
    edgar, _ = sec_clients()
    science, _, patents = scout_inputs()
    found, notes = evidence_companies(science, patents, edgar)
    assert [c.ticker for c in found] == ["GLSS", "FIXT"]                     # Glassfix: 2 patents + 1 paper; Fixture Memory: 1 patent
    assert found[0].patents == 2 and found[0].papers == 1 and evidence_summary(found[0]) == "2 patent(s) as assignee, 1 paper(s) by its researchers"
    assert all("university" not in c.name.lower() for c in found) and all(c.sec_listed for c in found)
    assert notes and "matched to the SEC ticker file" in notes[0]
    assert evidence_companies(None, None, edgar) == ([], ["no company names in the retrieved patents and papers"])
    assert evidence_companies(science, patents, None)[0] == []

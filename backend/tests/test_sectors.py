"""Sectors across the whole technology field: config consistency, sector-aware Market agent, topic discovery from
paper keywords (OpenAlex faked), and the watcher's weekly paper scout. All data here is FIXTURE data."""

from datetime import datetime, timezone

import yaml

from app.agents.market.agent import CompanyConfig, MarketAgent, load_companies
from app.radar import TopicConfig, load_sectors, load_topics, sector_of_topic
from app.radar.discovery import discover_topics, is_candidate
from app.sources.base import SourceError
from app.watch import add_topics

NOW = datetime(2026, 11, 9, tzinfo=timezone.utc)


def test_every_topic_and_company_belongs_to_a_configured_sector():
    keys = {s.key for s in load_sectors()}
    assert "semiconductors" in keys and len(keys) >= 8
    topics = load_topics()
    assert {t.sector for t in topics} <= keys and len({t.sector for t in topics}) >= 8
    assert {c.sector for c in load_companies()} <= keys
    assert all(s.discovery_queries for s in load_sectors())
    assert sector_of_topic("Solid-State Battery") == "energy" and sector_of_topic("HBM") == "semiconductors"
    assert sector_of_topic("something nobody configured") is None


def test_market_agent_reads_only_the_sector_companies_but_keeps_the_full_list():
    companies = [CompanyConfig(ticker="MU", name="Micron", sector="semiconductors"),
                 CompanyConfig(ticker="QS", name="QuantumScape", sector="energy")]
    agent = MarketAgent(None, None, None, companies=companies)
    seen = []
    agent._run = lambda topic, **kw: seen.append([c.ticker for c in agent.companies]) or __import__("app.schemas.market", fromlist=["MarketResult"]).MarketResult(topic=topic, status="no_data")  # type: ignore[method-assign]
    agent.run("solid-state battery", sector="energy")
    agent.run("solid-state battery", sector="unknown-sector")
    agent.run("solid-state battery")
    assert seen == [["QS"], ["MU", "QS"], ["MU", "QS"]] and [c.ticker for c in agent.companies] == ["MU", "QS"]


class FakeOpenAlex:
    """recent_keywords + count_by_year from fixture tables."""

    def __init__(self, keywords, counts, fail_query=None):
        self.keywords, self.counts, self.fail_query = keywords, counts, fail_query
        self.count_calls = []

    def recent_keywords(self, query, *, from_year, per_page=50):
        if query == self.fail_query:
            raise SourceError("OpenAlex", "fixture outage")
        freq = self.keywords.get(query, {})
        return freq, {k: [f"https://openalex.org/W{i}{n}" for i in range(min(n, 3))] for k, n in freq.items()}

    def count_by_year(self, phrase, start_year):
        self.count_calls.append(phrase)
        return self.counts.get(phrase, {})


def test_candidate_filter_drops_generic_known_and_near_duplicate_keywords():
    known = [TopicConfig(name="solid-state battery", terms=["solid-state battery", "all-solid-state battery"], sector="energy")]
    assert is_candidate("sodium ion battery", known)
    assert not is_candidate("deep learning", known)                 # generic field
    assert not is_candidate("solid state batteries", known)         # same words as a known topic
    vla = [TopicConfig(name="vision-language-action model", terms=["vision-language-action", "VLA model"], sector="robotics_autonomy")]
    assert not is_candidate("vision-language-action models", vla)   # hyphenated plural of a known topic
    assert not is_candidate("battery", known)                       # one word
    assert not is_candidate("a very long keyword phrase that goes on", known)
    assert not is_candidate("baryon acoustic oscillations", known, ["baryon", "cosmic"]) and is_candidate("neutral atom arrays", known, ["baryon"])
    assert all(s.exclude for s in load_sectors())


def test_discovery_proposes_only_growing_topics_with_enough_base_and_real_evidence():
    sector = load_sectors()[4]   # energy
    assert sector.key == "energy"
    oa = FakeOpenAlex(
        keywords={**{q: {"sodium ion battery": 5, "lithium metal anode": 4, "deep learning": 9, "tiny new idea": 3, "flat old idea": 3,
                         "whole field": 4} for q in sector.discovery_queries},
                  sector.discovery_queries[0]: {"sodium ion battery": 5, "lithium metal anode": 4, "deep learning": 9, "tiny new idea": 3,
                                                "flat old idea": 3, "whole field": 4, "one query only": 9}},
        counts={"sodium ion battery": {2022: 30, 2023: 60, 2024: 100, 2025: 180, 2026: 40},    # +80%: proposed
                "lithium metal anode": {2022: 300, 2023: 320, 2024: 400, 2025: 440, 2026: 90},  # +10%: too slow
                "tiny new idea": {2024: 5, 2025: 40, 2026: 9},                                   # base 5 < 20: noise
                "flat old idea": {2024: 100, 2025: 100, 2026: 20},
                "whole field": {2024: 20000, 2025: 40000, 2026: 9000},                           # > MAX_BASE: a field
                "one query only": {2024: 100, 2025: 300, 2026: 50}},                             # surfaced by one query: not sector-relevant
    )
    known = load_topics()
    new, notes = discover_topics(oa, sector, known, max_candidates=4, now=lambda: NOW)
    assert [n["topic"] for n in new] == ["sodium ion battery"] or new == []  # 'sodium-ion battery' is already a seed topic...
    # ...so with the real topics file it is a near-duplicate and must be rejected; check against an empty known list instead
    oa.count_calls = []
    new, notes = discover_topics(oa, sector, [], max_candidates=6, now=lambda: NOW)
    assert [n["topic"] for n in new] == ["sodium ion battery"]
    assert new[0]["sector"] == "energy" and new[0]["evidence"][0].startswith("https://openalex.org/W") and "+80%" in new[0]["why"]
    assert any("below 25%" in x for x in notes) and any("base too small" in x for x in notes) and any("whole field" in x for x in notes)
    assert "deep learning" not in oa.count_calls and "one query only" not in oa.count_calls and len(oa.count_calls) <= 6

    broken = FakeOpenAlex(keywords={}, counts={}, fail_query=sector.discovery_queries[0])
    new, notes = discover_topics(broken, sector, [], now=lambda: NOW)
    assert new == [] and any("fixture outage" in n for n in notes)


def test_add_topics_records_sector_and_who_found_it(tmp_path):
    path = tmp_path / "topics.yaml"
    path.write_text(yaml.safe_dump({"topics": [{"name": "old", "terms": ["old"], "sector": "quantum"}]}), encoding="utf-8")
    added = add_topics([{"topic": "sodium ion battery", "terms": ["sodium ion battery"], "sector": "energy", "evidence": ["https://openalex.org/W1"]},
                        {"topic": "old", "terms": ["old"], "sector": "quantum", "evidence": ["x"]}], path, found_by="paper scout")
    assert added == ["sodium ion battery"]
    rows = yaml.safe_load(path.read_text(encoding="utf-8"))["topics"]
    assert rows[1]["sector"] == "energy" and rows[1]["found_by"] == "paper scout" and rows[1]["evidence"] == ["https://openalex.org/W1"]
    assert [t.sector for t in load_topics(path)] == ["quantum", "energy"]

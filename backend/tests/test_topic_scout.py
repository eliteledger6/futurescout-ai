"""Idle scouting: the Science agent names a candidate from papers it was shown; code decides with OpenAlex counts."""
import json
from datetime import datetime, timezone
from types import SimpleNamespace

from app.agents.science import topic_scout as ts
from app.radar import SectorConfig, TopicConfig
from app.sources.base import SourceError

NOW = lambda: datetime(2026, 11, 11, 13, 0, tzinfo=timezone.utc)  # noqa: E731
SECTORS = [SectorConfig(key="semiconductors", name="Semiconductors", discovery_queries=["advanced packaging", "memory technology"])]
KNOWN = [TopicConfig(name="chiplet", sector="semiconductors", terms=["chiplet"])]
GROWING = {2022: 30, 2023: 45, 2024: 60, 2025: 110, 2026: 90}


def paper(i):
    return {"id": f"W{i}", "title": f"Paper {i} on hybrid bonding", "abstract": "Hybrid bonding of wafers. " * 5}


class Papers:
    def __init__(self, counts=GROWING, records=None, fail=False):
        self.counts, self.records, self.fail, self.searches, self.counted = counts, records or [paper(i) for i in range(1, 9)], fail, [], []

    def sample_works(self, query, n, *, from_date, seed):
        if self.fail:
            raise SourceError("OpenAlex", "down")
        assert from_date.isoformat() == "2026-05-12"          # the last six months only
        self.searches.append(query)
        return self.records

    def count_by_year(self, terms, start):
        self.counted.append(terms)
        return self.counts


class Model:
    def __init__(self, idea):
        self.idea, self.calls = idea, []

    def complete(self, agent, messages, response_model=None):
        self.calls.append((agent, messages))
        return SimpleNamespace(parsed=self.idea, usage=SimpleNamespace(cost_usd=0.0004))


def run(tmp_path, idea, papers=None, known=KNOWN, **kw):
    added, model, papers = [], Model(idea), papers or Papers()
    got = ts.scout_once(router=model, openalex=papers, sectors=SECTORS, known=known, state_path=tmp_path / "scout.json",
                        add_topic=lambda t: added.append(t) or True, now=NOW, log=lambda m: None, **kw)
    return got, added, model, papers, json.loads((tmp_path / "scout.json").read_text(encoding="utf-8"))


def test_a_growing_new_topic_from_shown_papers_is_added_by_the_science_agent(tmp_path):
    idea = ts.TopicIdea(found=True, topic="Hybrid Bonding", paper_ids=["W1", "W3", "W999"], why="Two papers.")
    got, added, model, papers, state = run(tmp_path, idea)
    assert got == "hybrid bonding"
    assert added == [{"topic": "hybrid bonding", "terms": ["hybrid bonding"], "sector": "semiconductors",
                      "evidence": ["W1", "W3"], "found_by": "science agent"}]             # only ids it was shown
    assert model.calls[0][0] == "science" and len(model.calls) == 1                        # the Science agent's own model, one call
    assert "chiplet" in model.calls[0][1][1]["content"] and "W5" in model.calls[0][1][1]["content"] and "W6" not in model.calls[0][1][1]["content"]   # 5 papers
    assert papers.counted == [["hybrid bonding"]]                         # counts come from OpenAlex
    assert state["log"][-1]["outcome"] == "added" and state["seen"] == ["W1", "W2", "W3", "W4", "W5"] and state["turn"] == 1


def test_papers_are_not_read_twice_and_queries_rotate(tmp_path):
    idea = ts.TopicIdea(found=False)
    p = Papers()
    run(tmp_path, idea, p)
    _, _, model, p, state = run(tmp_path, idea, p)
    assert state["seen"][-5:] == ["W6", "W7", "W8"][-5:] or state["seen"][-3:] == ["W6", "W7", "W8"]
    assert p.searches == ["advanced packaging", "memory technology"] and state["log"][-1]["outcome"] == "nothing new"


def test_the_model_cannot_add_a_topic_by_itself(tmp_path):
    good = dict(found=True, topic="hybrid bonding", why="x")
    for idea, papers, why in [
        (ts.TopicIdea(**good, paper_ids=["W77"]), Papers(), "did not point"),                               # invented evidence
        (ts.TopicIdea(found=True, topic="chiplets", paper_ids=["W1"]), Papers(), "already tracked"),
        (ts.TopicIdea(found=True, topic="memory", paper_ids=["W1"]), Papers(), "already tracked, too broad"),
        (ts.TopicIdea(**good, paper_ids=["W1"]), Papers({2022: 2, 2023: 3, 2024: 5, 2025: 12, 2026: 9}), "too few papers"),
        (ts.TopicIdea(**good, paper_ids=["W1"]), Papers({2022: 90, 2023: 95, 2024: 100, 2025: 104, 2026: 80}), "not growing fast enough"),
        (ts.TopicIdea(**good, paper_ids=["W1"]), Papers({2022: 9000, 2023: 9500, 2024: 9000, 2025: 15000, 2026: 9000}), "whole field"),
    ]:
        case = tmp_path / why.replace(" ", "_").replace(",", "")          # a fresh reading record per case
        case.mkdir()
        got, added, _, _, state = run(case, idea, papers)
        assert got is None and added == [] and state["log"][-1]["outcome"] == "rejected" and why in state["log"][-1]["note"], why


def test_daily_cap_and_failures_never_raise(tmp_path):
    idea = ts.TopicIdea(found=True, topic="hybrid bonding", paper_ids=["W1"], why="x")
    assert run(tmp_path, idea, max_new_per_day=1)[0] == "hybrid bonding"
    got, added, model, _, state = run(tmp_path, idea, max_new_per_day=1)
    assert got is None and model.calls == [] and "already added" in state["log"][-1]["note"]            # cap: no model call, no credit spent
    got, _, model, _, state = run(tmp_path / "x", idea, Papers(fail=True)) if (tmp_path / "x").mkdir() is None else None
    assert got is None and model.calls == [] and state["log"][-1]["outcome"] == "source error"

    class Broken:
        def complete(self, *a, **k):
            raise RuntimeError("model down")
    (tmp_path / "y").mkdir()
    assert ts.scout_once(router=Broken(), openalex=Papers(), sectors=SECTORS, known=KNOWN, state_path=tmp_path / "y" / "s.json",
                         add_topic=lambda t: True, now=NOW, log=lambda m: None) is None

"""Phrase check behind paper counts: synonyms kept only when sampled papers are on-topic. Faked OpenAlex and model."""

from datetime import date, datetime, timezone
from types import SimpleNamespace

from app.agents.science import phrases as ph
from app.agents.science.metrics import compute_acceleration, describe_phrases
from app.sources.openalex import phrase_filter

NOW = datetime(2026, 11, 9, tzinfo=timezone.utc)


class FakeOA:
    """'AI agents' and 'agentic AI' match on-topic papers; 'VLA' matches telescope papers; 'tiny phrase' almost nothing."""

    def __init__(self):
        self.requests = 0

    def count_between(self, q, start, end):
        self.requests += 1
        return {"AI agents": 4000, "LLM agents": 1900, "agentic AI": 2400, "VLA": 900, "tiny phrase": 1}.get(q, 0)

    def sample_works(self, q, n, *, from_date, to_date=None, seed=7):
        self.requests += 1
        key = q if isinstance(q, str) else "combined"
        topic = "telescope" if key == "VLA" else "agents"
        return [{"id": f"W{key}{i}", "title": f"{topic} paper {i}", "abstract": topic} for i in range(n)]


class FakeRouter:
    def __init__(self, suggest):
        self.suggest = suggest
        self.calls = []

    def complete(self, agent, messages, response_model=None):
        self.calls.append(agent)
        if response_model is ph._Suggestions:
            return SimpleNamespace(parsed=ph._Suggestions(phrases=self.suggest), llm_alias="fake")
        text = messages[1]["content"]
        # "relevant" = every paper whose title says agents (the telescope ones are not); one combined paper rejected
        ids = [line[1:line.index("]")] for line in text.splitlines() if line.startswith("[") and "agents paper" in line]
        ids = [i for i in ids if i != "p0"] if "[p0]" in text else ids
        return SimpleNamespace(parsed=ph._Verdicts(relevant_ids=ids), llm_alias="fake")


def test_keeps_on_topic_synonyms_and_drops_off_topic_abbreviation(tmp_path, monkeypatch):
    monkeypatch.setattr(ph, "configured_terms", lambda t: ["AI agents", "LLM agents"])
    router = FakeRouter(["agentic AI", "VLA", "tiny phrase", "agents"])  # "agents": single common word, refused
    basis = ph.build_counting_basis(FakeOA(), router, "AI agents", now=lambda: NOW, cache_dir=tmp_path)
    assert basis.phrases == ["AI agents", "LLM agents", "agentic AI"]
    by = {c.phrase: c for c in basis.checks}
    assert not by["VLA"].kept and "0/8" in by["VLA"].reason          # same letters, other field
    assert not by["tiny phrase"].kept and "only 1 matching" in by["tiny phrase"].reason
    assert "agents" not in by                                            # never even searched
    assert basis.precision_sampled == 20 and basis.precision_relevant == 19 and basis.precision_pct == 95.0
    assert "'VLA'" in basis.note and "95%" in basis.note
    # cached: a second call makes no model call
    again = ph.build_counting_basis(FakeOA(), FakeRouter([]), "AI agents", now=lambda: NOW, cache_dir=tmp_path)
    assert again.phrases == basis.phrases


def test_or_filter_and_basis_text():
    assert phrase_filter(["AI agents", "agentic AI", "AI agents", ""]) == 'title_and_abstract.search:"AI agents"|"agentic AI"'
    assert phrase_filter("a, b") == 'title_and_abstract.search:"a b"'
    assert describe_phrases(["x", "y"]) == 'any of the exact phrases "x", "y"'
    m = compute_acceleration({2024: 10, 2025: 20}, 2026, phrase=["AI agents", "agentic AI"])
    assert '"agentic AI"' in m.basis and "AI check" in m.basis and "not counted" not in m.basis
    single = compute_acceleration({2024: 10, 2025: 20}, 2026, phrase="AI agents")
    assert "Synonyms and abbreviations are not counted" in single.basis


def test_no_model_or_no_openalex_means_no_check(tmp_path):
    assert ph.build_counting_basis(None, FakeRouter([]), "x", cache_dir=tmp_path) is None
    assert ph.build_counting_basis(FakeOA(), None, "x", cache_dir=tmp_path) is None
    assert date(2026, 1, 1)  # keeps the import used

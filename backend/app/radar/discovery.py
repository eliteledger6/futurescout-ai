"""Paper scout: find NEW fast-growing topics in a sector from the keywords of recent papers (code only, no model).

How a topic gets onto the radar today:
  1. seed topics in config/topics.yaml (by hand);
  2. the X watch: the Chief model may propose up to 3 topics per scan, each tied to real post ids;
  3. this module: for each sector's broad discovery queries, read the OpenAlex keywords of the most-cited recent
     works, drop keywords that are already topics or too generic, and verify each remaining candidate with a real
     per-year count. A candidate becomes a topic only if it has at least MIN_BASE papers in the earlier year and
     grew at least `min_growth_pct` year over year. Evidence = the OpenAlex work ids that carried the keyword.

Once on the radar, a topic's heat (paper + patent growth) and X mentions decide when it is researched (watch mode).
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Callable, Optional

from app.agents.science.metrics import compute_acceleration
from app.radar import MIN_BASE, SectorConfig, TopicConfig
from app.sources.base import SourceError
from app.sources.openalex import OpenAlexClient

log = logging.getLogger("futurescout.discovery")

MIN_WORKS_WITH_KEYWORD = 3        # a keyword must appear on this many of the recent works to be a candidate
MIN_QUERIES_HIT = 2               # ...and in the results of at least two of the sector's discovery queries (sector relevance)
MAX_CANDIDATES_PER_SECTOR = 4     # per-year counts cost one request each; keep the budget small
MIN_GROWTH_PCT = 25.0
MAX_BASE = 5000                   # more papers than this in the earlier year = a whole field, not an emerging topic
# Keywords that describe whole fields rather than a technology; never proposed as topics.
GENERIC = {
    "deep learning", "machine learning", "artificial intelligence", "neural network", "neural networks", "computer science",
    "engineering", "physics", "materials science", "chemistry", "biology", "medicine", "optimization", "algorithm",
    "simulation", "performance", "efficiency", "scalability", "architecture", "framework", "benchmark", "dataset",
    "sustainability", "innovation", "technology", "internet of things", "big data", "cloud computing", "data science",
    "review", "survey", "state of the art", "case study", "methodology",
    # society / policy themes: real topics, but not technologies a sector agent should research
    "ai ethics", "ai governance", "data privacy", "food security", "public health", "climate change", "education",
    "generative ai", "artificial general intelligence", "large language models", "reinforcement learning",
}


def is_candidate(keyword: str, known: list[TopicConfig], exclude: list[str] = ()) -> bool:
    words = keyword.split()
    if not (2 <= len(words) <= 4) or len(keyword) > 48 or keyword in GENERIC:
        return False
    if any(x and x.lower() in keyword for x in exclude):
        return False
    if not re.fullmatch(r"[a-z0-9][a-z0-9 \-/()]+", keyword):
        return False
    kw = {_stem(w) for w in keyword.replace("-", " ").split()}
    for t in known:
        names = [t.name.lower(), *[x.lower() for x in t.terms]]
        if keyword in names:
            return False
        # mostly the same words as an existing topic ("solid state batteries" vs "solid-state battery")
        for n in names:
            nw = {_stem(w) for w in n.replace("-", " ").split()}
            if nw and len(kw & nw) / max(len(kw | nw), 1) >= 0.5:
                return False
    return True


def _stem(word: str) -> str:
    """Crude plural stripping so 'batteries' ~ 'battery' and 'robots' ~ 'robot'."""
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word


def discover_topics(
    openalex: OpenAlexClient,
    sector: SectorConfig,
    known: list[TopicConfig],
    *,
    max_candidates: int = MAX_CANDIDATES_PER_SECTOR,
    min_growth_pct: float = MIN_GROWTH_PCT,
    now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
) -> tuple[list[dict], list[str]]:
    """-> (new topics [{topic, terms, sector, evidence, why}], notes). Never raises on a source error."""
    year = now().year
    notes: list[str] = []
    freq: dict[str, int] = {}
    ids: dict[str, list[str]] = {}
    hits: dict[str, int] = {}          # how many of the sector's queries surfaced the keyword
    queries_ok = 0
    for q in sector.discovery_queries:
        try:
            f, i = openalex.recent_keywords(q, from_year=year - 1)
        except SourceError as exc:
            notes.append(f"{sector.key}: '{q}': {exc.message}")
            continue
        queries_ok += 1
        for k, n in f.items():
            freq[k] = freq.get(k, 0) + n
            hits[k] = hits.get(k, 0) + 1
            ids.setdefault(k, []).extend(x for x in i.get(k, []) if x not in ids.get(k, []))
    need_hits = min(MIN_QUERIES_HIT, max(queries_ok, 1))
    cands = sorted((k for k, n in freq.items() if n >= MIN_WORKS_WITH_KEYWORD and hits.get(k, 0) >= need_hits and is_candidate(k, known, sector.exclude)),
                   key=lambda k: -freq[k])
    out: list[dict] = []
    checked = 0
    for k in cands:
        if checked >= max_candidates:
            break
        checked += 1
        try:
            counts = openalex.count_by_year(k, year - 4)
        except SourceError as exc:
            notes.append(f"{sector.key}: '{k}': {exc.message}")
            continue
        acc = compute_acceleration(counts, year, phrase=k)
        if not acc or acc.yoy_growth_pct is None:
            notes.append(f"{sector.key}: '{k}': not enough years of data")
            continue
        if acc.previous_year_count < MIN_BASE:
            notes.append(f"{sector.key}: '{k}': only {acc.previous_year_count} papers in {acc.previous_year} (base too small)")
            continue
        if acc.previous_year_count > MAX_BASE:
            notes.append(f"{sector.key}: '{k}': {acc.previous_year_count} papers in {acc.previous_year}: a whole field, not an emerging topic")
            continue
        if acc.yoy_growth_pct < min_growth_pct:
            notes.append(f"{sector.key}: '{k}': {acc.yoy_growth_pct:+.0f}% growth, below {min_growth_pct:.0f}%")
            continue
        out.append({"topic": k, "terms": [k], "sector": sector.key, "evidence": ids.get(k, [])[:3],
                    "why": f"on {freq[k]} recent works; papers {acc.previous_year}->{acc.last_full_year}: "
                           f"{acc.previous_year_count}->{acc.last_full_year_count} ({acc.yoy_growth_pct:+.0f}%)"})
    return out, notes

"""Hot-Topic Radar: which technologies are heating up in research AND patents.

Everything here is computed by code from counts:
  * papers per year  (OpenAlex, exact phrase in title/abstract)  -> Research Acceleration
  * patents per year (Google Patents via SerpApi, title/abstract) -> Patent Acceleration
  * filers per year  (SEC full-text search: companies whose filings mention the topic), optional
Heat = the average of the two accelerations (paper and patent year-over-year growth between the two
most recent complete years). It is an ACTIVITY indicator: it says a topic is being written and
filed about more, not that it is a good investment. No model is involved anywhere in the radar.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import yaml
from pydantic import BaseModel, Field

from app.agents.science.metrics import compute_acceleration, ytd_from_client
from app.config import BACKEND_DIR, CONFIG_DIR
from app.schemas.science import AccelerationMetric, YtdMetric
from app.sources.base import SourceError
from app.sources.openalex import OpenAlexClient

log = logging.getLogger("futurescout.radar")

RADAR_FILE = BACKEND_DIR / "runs" / "radar.json"
COUNT_YEARS = 4   # complete years before the current one
MIN_BASE = 20     # a growth rate from fewer documents than this is not a signal (7 -> 30 papers is +329%)


DEFAULT_SECTOR = "semiconductors"


class SectorConfig(BaseModel):
    key: str
    name: str
    discovery_queries: list[str] = Field(default_factory=list)
    exclude: list[str] = Field(default_factory=list)   # word stems that mark a paper keyword as off-sector
    hints: str = ""


class TopicConfig(BaseModel):
    name: str
    terms: list[str] = Field(min_length=1)
    sector: str = DEFAULT_SECTOR
    found_by: Optional[str] = None


class TopicSignal(BaseModel):
    topic: str
    terms: list[str]
    sector: str = DEFAULT_SECTOR
    paper_counts: dict[int, int] = Field(default_factory=dict)
    paper_acceleration: Optional[AccelerationMetric] = None
    patent_counts: dict[int, int] = Field(default_factory=dict)
    patent_acceleration: Optional[AccelerationMetric] = None
    filer_counts: dict[int, int] = Field(default_factory=dict)   # SEC filers mentioning the topic, per year
    heat: Optional[float] = None       # average of the available YoY growth rates (%): papers and patents, or papers alone
    heat_basis: Optional[str] = None   # which growth rates went into heat, e.g. "papers 2025 + papers YTD + patents 2025"
    paper_ytd: Optional[YtdMetric] = None   # papers 1 Jan-cutoff this year vs the same dates last year
    trend: Optional[str] = None        # rising | flat | cooling (from paper_ytd); None when the base is too small
    small_base: bool = False           # fewer than MIN_BASE papers or patents in the earlier year: growth is noise
    rank: Optional[int] = None         # only topics with a heat value and a sufficient base are ranked
    errors: list[str] = Field(default_factory=list)


class Radar(BaseModel):
    generated_at: datetime
    topics: list[TopicSignal]
    searches_used: int = 0            # SerpApi searches spent by this run
    basis: str = (
        "Heat is the average of the code-computed growth rates available between the two most recent complete years: "
        "papers (OpenAlex works with the exact topic phrase in title or abstract) and patent publications "
        "(Google Patents, topic terms in title or abstract); when patents have not been counted for a topic, heat is the "
        "paper growth alone and is marked 'papers only'. Papers so far this year are also compared with the SAME dates last "
        "year (the last 30 days left out of both, for indexing delay), so a topic that is fading in the current year loses "
        "heat immediately and is marked 'cooling'. It measures how much more is being written and "
        "filed about a topic, not whether it is a good investment. Patent counts for recent years are "
        "undercounted (publication delay); the current partial year is excluded. Topics with fewer than 20 papers "
        "or patents in the earlier year are shown but not ranked (growth from a tiny base is noise). No model is involved."
    )


def load_topics(path: Optional[Path] = None) -> list[TopicConfig]:
    with open(path or (CONFIG_DIR / "topics.yaml"), "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return [TopicConfig.model_validate(t) for t in data.get("topics") or []]


def load_sectors(path: Optional[Path] = None) -> list[SectorConfig]:
    with open(path or (CONFIG_DIR / "sectors.yaml"), "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return [SectorConfig.model_validate(s) for s in data.get("sectors") or []]


def sector_of_topic(topic: str, topics: Optional[list[TopicConfig]] = None) -> Optional[str]:
    """The configured sector of a topic (matched by name or any term, case-insensitively), else None."""
    key = " ".join(topic.lower().split())
    for t in topics if topics is not None else load_topics():
        if key == t.name.lower() or key in {x.lower() for x in t.terms}:
            return t.sector
    return None


def _heat_parts(paper: Optional[AccelerationMetric], patent: Optional[AccelerationMetric],
                ytd: Optional[YtdMetric] = None) -> list[tuple[str, float]]:
    parts: list[tuple[str, float]] = []
    if paper is not None and paper.yoy_growth_pct is not None:
        parts.append((f"papers {paper.last_full_year}", paper.yoy_growth_pct))
    if ytd is not None and ytd.growth_pct is not None and ytd.trend is not None:   # trend None = base too small
        parts.append(("papers YTD", ytd.growth_pct))
    if patent is not None and patent.yoy_growth_pct is not None:
        parts.append((f"patents {patent.last_full_year}", patent.yoy_growth_pct))
    return parts


def heat_of(paper: Optional[AccelerationMetric], patent: Optional[AccelerationMetric],
            ytd: Optional[YtdMetric] = None) -> Optional[float]:
    """Average of the growth rates that exist: last full year's papers, this year's papers so far (same dates as last
    year), and last full year's patents. A topic that was hot in 2025 but is fading in 2026 loses heat right away."""
    parts = _heat_parts(paper, patent, ytd)
    return round(sum(v for _, v in parts) / len(parts), 1) if parts else None


def heat_basis_of(paper: Optional[AccelerationMetric], patent: Optional[AccelerationMetric],
                  ytd: Optional[YtdMetric] = None) -> Optional[str]:
    parts = _heat_parts(paper, patent, ytd)
    return " + ".join(n for n, _ in parts) if parts else None


def rank_topics(topics: list[TopicSignal]) -> list[TopicSignal]:
    """Ranked topics first (hottest first), then small-base and incomplete topics in their original order."""
    with_heat = sorted((t for t in topics if t.heat is not None and not t.small_base), key=lambda t: -t.heat)  # type: ignore[operator]
    without = [t for t in topics if t.heat is None or t.small_base]
    for i, t in enumerate(with_heat, start=1):
        t.rank = i
    return [*with_heat, *without]


def compute_radar(
    topics: list[TopicConfig],
    *,
    openalex: Optional[OpenAlexClient],
    patents,                        # SerpApiPatentsClient | EpoOpsClient | None (count_by_year)
    filers=None,                    # EdgarFullTextClient | None (count_filers_by_year)
    now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
) -> Radar:
    year = now().year
    start = year - COUNT_YEARS
    out: list[TopicSignal] = []
    for t in topics:
        sig = TopicSignal(topic=t.name, terms=t.terms, sector=t.sector)
        if openalex:
            try:
                sig.paper_counts = openalex.count_by_year(t.name, start)
                sig.paper_acceleration = compute_acceleration(sig.paper_counts, year, phrase=t.name)
            except SourceError as exc:
                sig.errors.append(f"papers: {exc.message}")
            try:
                sig.paper_ytd = ytd_from_client(openalex, t.name, now().date())
                sig.trend = sig.paper_ytd.trend if sig.paper_ytd else None
            except SourceError as exc:
                sig.errors.append(f"papers (year to date): {exc.message}")
        if patents:
            try:
                sig.patent_counts = patents.count_by_year(t.terms, start)
                sig.patent_acceleration = compute_acceleration(sig.patent_counts, year)
                if sig.patent_acceleration:
                    sig.patent_acceleration.basis = (
                        f"Patent publications per year with any of {t.terms} in title or abstract "
                        f"({getattr(patents, 'SOURCE', 'patent source')}). Recent years undercounted by publication delay.")
            except SourceError as exc:
                sig.errors.append(f"patents: {exc.message}")
        if filers:
            try:
                sig.filer_counts = filers.count_filers_by_year(t.name, start)
            except SourceError as exc:
                sig.errors.append(f"filers: {exc.message}")
        sig.heat = heat_of(sig.paper_acceleration, sig.patent_acceleration, sig.paper_ytd)
        sig.heat_basis = heat_basis_of(sig.paper_acceleration, sig.patent_acceleration, sig.paper_ytd)
        sig.small_base = any(a is not None and a.previous_year_count < MIN_BASE
                             for a in (sig.paper_acceleration, sig.patent_acceleration))
        out.append(sig)
    return Radar(generated_at=now(), topics=rank_topics(out), searches_used=getattr(patents, "searches_used", 0) or 0)


def save_radar(radar: Radar, path: Path = RADAR_FILE) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(radar.model_dump_json(indent=2), encoding="utf-8")
    return path


SAMPLE_RADAR_FILE = BACKEND_DIR / "samples" / "radar.json"   # shipped with the repo for fresh clones


def load_radar(path: Path = RADAR_FILE) -> Optional[Radar]:
    if not path.is_file():
        path = SAMPLE_RADAR_FILE if path == RADAR_FILE and SAMPLE_RADAR_FILE.is_file() else path
        if not path.is_file():
            return None
    return Radar.model_validate(json.loads(path.read_text(encoding="utf-8")))

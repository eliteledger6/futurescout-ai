"""Shared data structures used by every agent.

Key idea: source URLs only ever come from tools (API clients) and live in a
registry of SourceRecord objects. Models may reference a source by its id but
can never invent one; the citation guard (app/graph/citation_guard.py) enforces it.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Literal, Optional
from urllib.parse import urlsplit, urlunsplit

from pydantic import BaseModel, Field, model_validator


class Label(str, Enum):
    VERIFIED_FACT = "verified_fact"          # directly supported by a cited source passage
    AI_INTERPRETATION = "ai_interpretation"  # the model's reading/comparison of sources
    FORECAST = "forecast"                    # a prediction about the future
    ASSUMPTION = "assumption"                # something taken as given, not evidenced
    UNVERIFIED_CLAIM = "unverified_claim"    # asserted by someone, not independently checked


class Horizon(str, Enum):
    NEAR = "near_0_12m"
    MEDIUM = "medium_1_3y"
    LONG = "long_3_5y"
    NOT_APPLICABLE = "not_applicable"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ContentType(str, Enum):
    PAPER = "paper"
    PREPRINT = "preprint"
    PATENT = "patent"
    FILING = "filing"
    PRESS_RELEASE = "press_release"
    NEWS = "news"
    SOCIAL_POST = "social_post"
    OTHER = "other"


TextDepth = Literal["metadata_only", "abstract_only", "excerpt_only", "full_text"]


def canonical_url(url: str) -> str:
    """Normalise a URL so the same page always gets the same source id."""
    parts = urlsplit(url.strip())
    scheme = (parts.scheme or "https").lower()
    host = parts.netloc.lower()
    path = parts.path.rstrip("/")
    return urlunsplit((scheme, host, path, parts.query, ""))


def make_source_id(url: str) -> str:
    return "src_" + hashlib.sha1(canonical_url(url).encode("utf-8")).hexdigest()[:10]


class SourceRecord(BaseModel):
    """One retrieved item (paper, preprint, later: patent, filing, post)."""

    id: str = ""
    url: str
    source_name: str                       # e.g. "OpenAlex", "arXiv"
    content_type: ContentType
    title: str
    published_at: Optional[str] = None     # ISO date (YYYY-MM-DD) as given by the source
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    authors: list[str] = Field(default_factory=list)
    organization: Optional[str] = None
    affiliations: list[str] = Field(default_factory=list)  # company-type author institutions (OpenAlex), as given
    doi: Optional[str] = None
    venue: Optional[str] = None
    publication_type: Optional[str] = None
    abstract: Optional[str] = None
    cited_by_count: Optional[int] = None
    open_access_url: Optional[str] = None
    text_depth: TextDepth = "abstract_only"  # what we actually have; never claim more
    is_mock: bool = False                    # True only for test data; guard refuses to "verify" mocks
    is_retracted: bool = False               # publisher retracted it (OpenAlex flag); can never verify a fact

    @model_validator(mode="after")
    def _fill_id(self) -> "SourceRecord":
        if not self.id:
            self.id = make_source_id(self.url)
        return self

    def searchable_text(self) -> str:
        """Text that a verified_fact excerpt is allowed to be quoted from."""
        return f"{self.title}\n{self.abstract or ''}"


class FindingDraft(BaseModel):
    """What a model is asked to produce for each finding."""

    claim: str = Field(min_length=10)
    label: Label
    confidence: Confidence
    horizon: Horizon = Horizon.NOT_APPLICABLE
    source_ids: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    companies: list[str] = Field(default_factory=list)
    rationale: Optional[str] = None
    supporting_excerpt: Optional[str] = None  # verbatim passage from the cited source


class Finding(FindingDraft):
    """A finding after the citation guard has checked it."""

    guard_note: Optional[str] = None  # set when the guard downgraded or edited the finding
    fid: Optional[str] = None         # short id (S1, R1, C1...) other agents use to reference this finding


class AgentError(BaseModel):
    """A failure that happened while an agent worked (never silently dropped)."""

    agent: str
    source: str
    message: str
    recoverable: bool = False

"""Citation guard: plain code (no model) that checks every finding against real sources.

Rules for a finding labelled `verified_fact`:
  1. It must cite at least one source id that exists in the registry
     (ids a model invented are removed).
  2. It must include a `supporting_excerpt` that really appears in the cited
     sources' title/abstract (case and whitespace insensitive; "..." may join
     separate passages).
  3. It may not rely on mock (test) sources.
  4. News headlines and social posts can never verify a fact: the excerpt must come from
     a cited source of another kind (paper, filing...).
If any rule fails, the finding is NOT dropped silently: it is downgraded to
`unverified_claim` with low confidence and a `guard_note` explaining why.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Iterable, Optional

from app.schemas.common import Confidence, ContentType, Finding, FindingDraft, Label, SourceRecord

_MIN_EXCERPT_PART = 15  # characters; shorter fragments prove nothing
NEVER_VERIFIES = frozenset({ContentType.NEWS, ContentType.SOCIAL_POST})  # headlines / posts


@dataclass
class GuardIssue:
    claim: str
    action: str   # "removed_unknown_source_ids" | "downgraded"
    reason: str

    def as_dict(self) -> dict:
        return {"claim": self.claim, "action": self.action, "reason": self.reason}


@dataclass
class GuardResult:
    findings: list[Finding] = field(default_factory=list)
    issues: list[GuardIssue] = field(default_factory=list)


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"[‘’“”\"']", "", text)
    return re.sub(r"\s+", " ", text).strip()


def excerpt_supported(excerpt: Optional[str], texts: Iterable[str]) -> bool:
    """True if every meaningful part of the excerpt occurs in at least one source text."""
    if not excerpt or not excerpt.strip():
        return False
    parts = [p.strip(" .,;:") for p in re.split(r"\.\.\.|…", excerpt)]
    parts = [_normalise(p) for p in parts if len(p.strip(" .,;:")) >= _MIN_EXCERPT_PART]
    if not parts:
        return False
    haystacks = [_normalise(t) for t in texts]
    return all(any(part in hay for hay in haystacks) for part in parts)


def _short(text: str, n: int = 120) -> str:
    return text if len(text) <= n else text[: n - 1] + "…"


def apply_citation_guard(
    drafts: Iterable[FindingDraft],
    registry: dict[str, SourceRecord],
    *,
    allow_mock_verified: bool = False,
) -> GuardResult:
    result = GuardResult()

    for draft in drafts:
        finding = Finding(**draft.model_dump())
        notes: list[str] = []

        # Rule 1: drop source ids that do not exist; remove duplicates, keep order.
        seen: set[str] = set()
        valid_ids: list[str] = []
        unknown: list[str] = []
        for sid in finding.source_ids:
            if sid in seen:
                continue
            seen.add(sid)
            (valid_ids if sid in registry else unknown).append(sid)
        if unknown:
            reason = f"unknown source id(s) removed: {', '.join(unknown)}"
            notes.append(reason)
            result.issues.append(GuardIssue(_short(finding.claim), "removed_unknown_source_ids", reason))
        finding.source_ids = valid_ids

        # Rules for verified facts.
        if finding.label == Label.VERIFIED_FACT:
            problem: Optional[str] = None
            evidence_ids = [s for s in valid_ids if registry[s].content_type not in NEVER_VERIFIES]
            if not valid_ids:
                problem = "no valid cited source"
            elif not allow_mock_verified and any(registry[s].is_mock for s in valid_ids):
                problem = "cites mock (test) data, which cannot verify a fact"
            elif not evidence_ids:
                problem = "news headlines and social posts cannot verify a fact"
            elif any(registry[s].is_retracted for s in evidence_ids):
                problem = "cites a RETRACTED paper, which cannot verify a fact"
            elif not excerpt_supported(
                finding.supporting_excerpt, (registry[s].searchable_text() for s in evidence_ids)
            ):
                problem = "supporting excerpt missing or not found in the cited source text"
            if problem:
                finding.label = Label.UNVERIFIED_CLAIM
                finding.confidence = Confidence.LOW
                notes.append(f"downgraded from verified_fact: {problem}")
                result.issues.append(GuardIssue(_short(finding.claim), "downgraded", problem))

        if notes:
            finding.guard_note = "; ".join(notes)
        result.findings.append(finding)

    return result

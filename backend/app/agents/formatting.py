"""Text blocks that give models the evidence they may cite (by id only)."""

from __future__ import annotations

from typing import Iterable

from app.schemas.common import Finding, SourceRecord


def format_findings(findings: Iterable[Finding], titles: dict[str, str] | None = None) -> str:
    """One line per finding: [id] (label | confidence | cites) claim."""
    titles = titles or {}
    lines = []
    for f in findings:
        cites = ", ".join(f"{sid}" + (f" '{titles[sid][:60]}'" if sid in titles else "") for sid in f.source_ids)
        lines.append(
            f"[{f.fid}] ({f.label.value} | {f.confidence.value} | cites: {cites or 'none'}) {f.claim}"
        )
    return "\n".join(lines) if lines else "(none)"


def title_map(*groups: Iterable[SourceRecord]) -> dict[str, str]:
    out: dict[str, str] = {}
    for group in groups:
        for rec in group:
            out[rec.id] = rec.title
    return out

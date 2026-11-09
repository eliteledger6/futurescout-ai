"""Research momentum metrics computed by code (never by a model)."""

from __future__ import annotations

from typing import Optional

from app.schemas.science import AccelerationMetric


def compute_acceleration(
    counts: dict[int, int], current_year: int, phrase: Optional[str] = None
) -> Optional[AccelerationMetric]:
    """Year-over-year change between the two most recent COMPLETE calendar years.

    Returns None if either year is missing. The growth percentage is None when the
    earlier year had zero works (growth from zero is undefined).
    """
    last, previous = current_year - 1, current_year - 2
    if last not in counts or previous not in counts:
        return None
    growth = None
    if counts[previous] > 0:
        growth = round((counts[last] - counts[previous]) / counts[previous] * 100, 1)
    kwargs = {}
    if phrase:
        kwargs["basis"] = (
            f'OpenAlex works whose title or abstract contains the exact phrase "{phrase}", per '
            "publication year. Synonyms and abbreviations are not counted, and the number is not "
            "normalised for overall growth in publishing. The current (partial) year is excluded."
        )
    return AccelerationMetric(
        last_full_year=last,
        last_full_year_count=counts[last],
        previous_year=previous,
        previous_year_count=counts[previous],
        yoy_growth_pct=growth,
        **kwargs,
    )

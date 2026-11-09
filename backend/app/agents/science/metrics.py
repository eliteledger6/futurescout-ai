"""Research momentum metrics computed by code (never by a model)."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from app.schemas.science import AccelerationMetric, YtdMetric

LAG_DAYS = 30          # OpenAlex indexing delay: the last month of the current year is cut from BOTH years
MIN_YTD_BASE = 20      # fewer papers than this in last year's window: growth is noise, no trend label
TREND_BAND_PCT = 10.0  # within +/-10% = flat


def describe_phrases(phrase: "Optional[str | list[str]]") -> str:
    """'the exact phrase "x"' or 'any of the exact phrases "x", "y"' (for basis texts)."""
    if not phrase:
        return ""
    items = [phrase] if isinstance(phrase, str) else [p for p in phrase if p]
    if len(items) == 1:
        return f'the exact phrase "{items[0]}"'
    return "any of the exact phrases " + ", ".join(f'"{p}"' for p in items)


def ytd_window(today: date, lag_days: int = LAG_DAYS) -> Optional[tuple[date, date, date, date]]:
    """(this-year start, this-year cutoff, last-year start, last-year cutoff), or None early in January."""
    cutoff = today - timedelta(days=lag_days)
    if cutoff.year != today.year:
        return None
    try:
        prev_cutoff = cutoff.replace(year=cutoff.year - 1)
    except ValueError:                       # 29 February
        prev_cutoff = (cutoff - timedelta(days=1)).replace(year=cutoff.year - 1)
    return date(cutoff.year, 1, 1), cutoff, date(cutoff.year - 1, 1, 1), prev_cutoff


def compute_ytd(count: int, previous_count: int, cutoff: date, phrase: "Optional[str | list[str]]" = None) -> YtdMetric:
    growth = round((count - previous_count) / previous_count * 100, 1) if previous_count > 0 else None
    trend = None
    if growth is not None and previous_count >= MIN_YTD_BASE:
        trend = "rising" if growth > TREND_BAND_PCT else "cooling" if growth < -TREND_BAND_PCT else "flat"
    return YtdMetric(
        year=cutoff.year, previous_year=cutoff.year - 1, cutoff=cutoff.strftime("%m-%d"), count=count,
        previous_count=previous_count, growth_pct=growth, trend=trend,
        basis=(f'OpenAlex works{" with " + describe_phrases(phrase) + " in title or abstract" if phrase else ""} published '
               f"1 Jan–{cutoff.strftime('%d %b')} {cutoff.year} vs the same dates in {cutoff.year - 1}. The last {LAG_DAYS} days "
               f"are left out of both years because new papers take weeks to be indexed."),
    )


def ytd_from_client(openalex, phrase: "str | list[str]", today: date) -> Optional[YtdMetric]:  # noqa: ANN001
    """Two count requests (this year's window and last year's). None when not applicable or unsupported."""
    win = ytd_window(today)
    if win is None or not hasattr(openalex, "count_between"):
        return None
    s1, e1, s0, e0 = win
    return compute_ytd(openalex.count_between(phrase, s1, e1), openalex.count_between(phrase, s0, e0), e1, phrase=phrase)


def compute_acceleration(
    counts: dict[int, int], current_year: int, phrase: "Optional[str | list[str]]" = None
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
            f"OpenAlex works whose title or abstract contains {describe_phrases(phrase)}, per publication year "
            "(singular and plural forms match; each work counted once). "
            + ("Synonyms and abbreviations are not counted. " if isinstance(phrase, str) or len(phrase) == 1 else
               "The synonyms and abbreviations were kept only after an AI check of sampled papers. ")
            + "The number is not normalised for overall growth in publishing. The current (partial) year is excluded."
        )
    return AccelerationMetric(
        last_full_year=last,
        last_full_year_count=counts[last],
        previous_year=previous,
        previous_year_count=counts[previous],
        yoy_growth_pct=growth,
        **kwargs,
    )

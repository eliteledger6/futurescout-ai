"""Diagnostic: compare three ways of counting OpenAlex works per year for one topic.

Why: the plain `search=` parameter may match loosely (any work mentioning the words),
which would make "Research Acceleration" look too big. This prints the numbers side by
side so we choose the query from evidence. It costs about 30 OpenAlex credits.

Usage (from the backend folder, venv active):
    python scripts\\check_counts.py --topic "high bandwidth memory"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.sources.base import SourceError  # noqa: E402
from app.sources.openalex import OpenAlexClient  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--start-year", type=int, default=2020)
    args = parser.parse_args()

    settings = get_settings()
    http = httpx.Client(timeout=30.0, headers={"User-Agent": settings.http_user_agent}, follow_redirects=True)
    client = OpenAlexClient(settings.openalex_key_value(), http=http)
    start = f"from_publication_date:{args.start_year}-01-01"
    phrase = f'"{args.topic}"'

    variants = {
        "A  search=topic (current)": {"search": args.topic, "filter": start},
        "B  search=\"topic\" (quoted phrase)": {"search": phrase, "filter": start},
        "C  title_and_abstract.search phrase": {"filter": f"title_and_abstract.search:{phrase},{start}"},
    }
    results: dict[str, dict[int, int]] = {}
    for name, extra in variants.items():
        try:
            data = client._get("/works", {"group_by": "publication_year", **extra})
            results[name] = {int(g["key"]): int(g["count"]) for g in data.get("group_by", []) if int(g["key"]) >= args.start_year}
        except (SourceError, KeyError, ValueError) as exc:
            print(f"{name}: FAILED -> {exc}")

    years = sorted({y for r in results.values() for y in r})
    print(f"\nTopic: {args.topic}\n")
    print(f"{'year':6}" + "".join(f"{n.split()[0]:>10}" for n in results))
    for y in years:
        print(f"{y:<6}" + "".join(f"{results[n].get(y, 0):>10}" for n in results))
    print("\nA = current query, B = quoted phrase in search, C = phrase in title/abstract filter.")
    print("A much larger than B/C means A is matching loosely.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

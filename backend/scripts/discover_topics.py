"""Paper scout: find new fast-growing topics per sector from the keywords of recent papers (OpenAlex, free with key).

  python scripts\\discover_topics.py                    all sectors, show candidates, add the qualifying ones to config/topics.yaml
  python scripts\\discover_topics.py --sector quantum   one sector
  python scripts\\discover_topics.py --dry-run          show only; change nothing

A candidate is added only if it has >= 20 papers in the earlier complete year and grew >= 25% year over year
(see app/radar/discovery.py). Evidence = OpenAlex work ids. Remove any entry by hand if you disagree.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import get_settings  # noqa: E402
from app.radar import TopicConfig, load_sectors, load_topics  # noqa: E402
from app.radar.discovery import discover_topics  # noqa: E402
from app.sources.openalex import OpenAlexClient  # noqa: E402
from app.watch import add_topics  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sector", help="sector key (default: all)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-candidates", type=int, default=4, help="per sector; each costs one OpenAlex count request")
    args = ap.parse_args()
    s = get_settings()
    oa = OpenAlexClient(s.openalex_key_value())
    sectors = [x for x in load_sectors() if not args.sector or x.key == args.sector]
    if not sectors:
        print(f"unknown sector {args.sector!r}; keys: {[x.key for x in load_sectors()]}")
        return 1
    known = load_topics()
    found: list[dict] = []
    for sec in sectors:
        new, notes = discover_topics(oa, sec, known + [TopicConfig(name=f["topic"], terms=f["terms"], sector=f["sector"]) for f in found],
                                     max_candidates=args.max_candidates)
        print(f"\n== {sec.name} ({sec.key})")
        for f in new:
            print(f"  NEW   {f['topic']!r}: {f['why']}  evidence={f['evidence']}")
        for n in notes:
            print(f"  -     {n}")
        found += new
    if not found:
        print("\nno new topic qualified")
        return 0
    if args.dry_run:
        print(f"\ndry run: {len(found)} topic(s) would be added")
        return 0
    added = add_topics(found, found_by="paper scout")
    print(f"\nadded to config/topics.yaml: {added}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

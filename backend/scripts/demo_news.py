"""Live check of the GDELT news client (no key, no model, no cost).

  python scripts\\demo_news.py --query "high bandwidth memory" --timespan 1month
"""

from __future__ import annotations

import argparse
import sys

from app.sources.base import SourceError
from app.sources.gdelt import GdeltClient


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--timespan", default="1month", help="e.g. 1week, 1month, 3months")
    ap.add_argument("--max", type=int, default=10)
    args = ap.parse_args()
    try:
        records = GdeltClient().search(args.query, max_results=args.max, timespan=args.timespan)
    except SourceError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"{len(records)} article(s) (headlines only; a headline is not proof of a fact)")
    for r in records:
        print(f"- {r.published_at or 'date unknown'} | {r.organization} | {r.title}\n  {r.url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

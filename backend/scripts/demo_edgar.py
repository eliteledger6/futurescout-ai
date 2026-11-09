"""Live check of the SEC EDGAR client (no model, no cost).

  python scripts\\demo_edgar.py --ticker MU --keywords "high bandwidth memory,HBM"

Needs EDGAR_USER_AGENT in .env (your name + a contact email; the SEC requires it).
Prints real filings and short verbatim passages that mention the keywords.
"""

from __future__ import annotations

import argparse
import sys

from app.config import get_settings
from app.sources.base import SourceError
from app.sources.edgar import EdgarClient


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--keywords", default="", help="comma-separated; passages containing them are shown")
    ap.add_argument("--since", default=None, help="YYYY-MM-DD")
    ap.add_argument("--limit", type=int, default=3)
    args = ap.parse_args()

    ua = get_settings().edgar_user_agent
    if not ua:
        print("EDGAR_USER_AGENT is not set in .env. The SEC requires your name and a contact email, "
              "e.g. EDGAR_USER_AGENT=YourName you@example.com")
        return 1
    try:
        client = EdgarClient(ua)
        records = client.recent_filings(args.ticker, since=args.since, limit=args.limit)
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
        print(f"{len(records)} filing(s) for {args.ticker.upper()}")
        for rec in records:
            if keywords:
                rec = client.add_excerpts(rec, keywords)
            print(f"\n- {rec.title}\n  {rec.url}\n  text depth: {rec.text_depth}")
            if rec.text_depth == "excerpt_only":
                print("  " + (rec.abstract or "").replace("\n", "\n  "))
    except SourceError as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

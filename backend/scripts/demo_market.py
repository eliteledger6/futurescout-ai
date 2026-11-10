"""Live check of the Market agent's retrieval (no model, no cost unless --llm).

  python scripts\\demo_market.py --topic "high bandwidth memory" --keywords "HBM"
  python scripts\\demo_market.py --topic "high bandwidth memory" --keywords "HBM" --tickers MU,NVDA --no-news

Reads the latest annual/quarterly SEC reports of the companies in config/companies.yaml (or
--tickers) and keeps verbatim passages that mention the topic/keywords; optionally searches
GDELT news headlines. With --llm it also runs the model analysis (needs NEAR AI credit).
Needs EDGAR_USER_AGENT in .env (your name + a contact email; the SEC requires it).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.market import CompanyConfig, MarketAgent  # noqa: E402
from app.config import ConfigError, get_settings  # noqa: E402
from app.models.config import load_model_config  # noqa: E402
from app.models.router import ModelRouter  # noqa: E402
from app.sources.base import SourceError  # noqa: E402
from app.sources.edgar import EdgarClient  # noqa: E402
from app.sources.gdelt import GdeltClient  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--keywords", default="", help="extra comma-separated terms, e.g. abbreviations")
    ap.add_argument("--tickers", required=True, help="comma-separated tickers to read (in a real run the companies come from the papers and patents)")
    ap.add_argument("--no-news", action="store_true")
    ap.add_argument("--llm", action="store_true", help="also run the model analysis (costs NEAR AI credit)")
    args = ap.parse_args()

    settings = get_settings()
    if not settings.edgar_user_agent:
        print("EDGAR_USER_AGENT is not set in .env. The SEC requires your name and a contact email, "
              "e.g. EDGAR_USER_AGENT=YourName you@example.com")
        return 1
    companies = [CompanyConfig(ticker=t.strip().upper(), name=t.strip().upper(), evidence="given on the command line")
                 for t in args.tickers.split(",") if t.strip()]
    if not companies:
        return 1

    router = None
    if args.llm:
        try:
            settings.require_near_key()
        except ConfigError as exc:
            print(f"ERROR: {exc}")
            return 1
        router = ModelRouter(load_model_config(), settings)
    try:
        edgar = EdgarClient(settings.edgar_user_agent)
    except SourceError as exc:
        print(f"ERROR: {exc}")
        return 1
    gdelt = None if args.no_news else GdeltClient(user_agent=settings.http_user_agent)
    agent = MarketAgent(router, edgar, gdelt, companies=companies)
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    print(f"Checking {len(companies)} companies for: {args.topic} {keywords or ''} (this reads a few large filings; ~1 minute)\n")
    result = agent.run(args.topic, keywords=keywords, use_llm=args.llm)

    print(f"Status: {result.status}   Keywords used: {', '.join(result.keywords)}\n")
    for c in result.companies:
        print(f"  {c.ticker:5} reports read: {c.filings_checked}  mentioning keywords: {c.filings_with_mentions}"
              + (f"  ERROR: {c.error}" if c.error else ""))
    print(f"\n{len(result.sources)} source(s) kept:")
    for s in result.sources:
        print(f"\n- [{s.id}] {s.title}\n  {s.url}\n  {s.content_type.value}, {s.text_depth}")
        if s.abstract:
            print("  " + s.abstract.replace("\n", "\n  "))
    if result.findings:
        print("\nFindings:")
        for f in result.findings:
            print(f"  [{f.fid}] ({f.label.value}, {f.confidence.value}) {f.claim}" + (f"\n      check: {f.guard_note}" if f.guard_note else ""))
    if result.errors:
        print("\nErrors:")
        for e in result.errors:
            print(f"  [{e.source}] {e.message}")
    print(f"\n{result.coverage_note}")
    return 0 if result.sources else 2


if __name__ == "__main__":
    sys.exit(main())

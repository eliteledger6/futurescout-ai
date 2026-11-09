"""Let the X agent find accounts that post about a topic and suggest them for the watchlist.

  python scripts\\x_discover.py --topic "high bandwidth memory" --keywords "HBM"

Reads up to 50 recent posts about the topic from ALL of X (about $0.25 of X credit), ranks the
authors (on-topic posts, X organisation badge, reach), writes them to the `suggested` list in
config/x_watchlist.yaml and, if `auto_manage: true` there, adds the strong ones to `approved`.
Handles come from real posts only; nothing is invented. No model call.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.market.agent import clean_keywords  # noqa: E402
from app.agents.x import XAgent  # noqa: E402
from app.agents.x import watchlist as wl  # noqa: E402
from app.config import get_settings, quiet_network_logs  # noqa: E402
from app.schemas.xsignals import XResult  # noqa: E402
from app.sources.x import XClient  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--keywords", default="", help="extra comma-separated terms, e.g. abbreviations")
    ap.add_argument("--max-posts", type=int, default=50)
    args = ap.parse_args()
    quiet_network_logs()
    token = get_settings().x_token_value()
    if not token:
        print("X_BEARER_TOKEN is not set in .env")
        return 1
    keywords = clean_keywords([args.topic, *[k.strip() for k in args.keywords.split(",") if k.strip()]])
    agent = XAgent(None, XClient(token))
    result = XResult(topic=args.topic, status="no_data", keywords=keywords, accounts=[a.handle for a in agent.watchlist])
    agent.discover(args.topic, keywords, result, max_posts=args.max_posts)
    data = wl.load()
    print(f"auto_manage is {'ON' if data['auto_manage'] else 'OFF'} (min score {data['auto_add_min_score']}, remove after {data['auto_remove_after_days']} days)")
    for e in result.errors:
        print("ERROR:", e.message)
    print(f"\n{len(result.suggested_accounts)} suggested account(s) not yet on the watchlist (best first):")
    for s in result.suggested_accounts:
        flags = f"  CAUTION: {'; '.join(s['flags'])}" if s["flags"] else ""
        print(f"  {'NEW ' if s['new'] else '    '}@{s['handle']:16} {s['name'][:28]:28} score={s['score']:<5} posts={s['posts_on_topic']} "
              f"followers={s['followers'] if s['followers'] is not None else '?':>8} badge={s['verified_type'] or 'none'}{flags}")
        for url in s["evidence"][:1]:
            print(f"        e.g. {url}")
    if result.watchlist_changes:
        print("\nChanges the agent made to the watchlist:")
        for c in result.watchlist_changes:
            print("  -", c)
    else:
        print("\nNo watchlist changes" + (" (auto_manage is off: approve suggestions by moving them to `approved`, or set auto_manage: true)." if not data["auto_manage"] else "."))
    print(f"\nX API usage: {result.x_usage}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

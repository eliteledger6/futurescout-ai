"""Seed the X read list for sectors that have no watched accounts yet: one account search per sector, on that
sector's hottest radar topic, using the same rules as watch mode (verified only, roles and @mentions count).

  python scripts\\x_seed_sectors.py              all sectors except the one(s) already covered
  python scripts\\x_seed_sectors.py --dry-run    show which topics would be searched; spend nothing

Cost: about $0.25 of X credit per sector searched (50 posts read). Capped by WATCH_X_DAILY_BUDGET_USD.
The agent never follows anyone on X: "added" means added to FUTURESCOUT's read list (config/x_watchlist.yaml).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.x import watchlist as wl  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.radar import load_radar, load_sectors, load_topics  # noqa: E402
from app.sources.x import XClient  # noqa: E402
from app.watch import Watcher, load_state, save_state  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip", nargs="*", default=["semiconductors"], help="sector keys that already have accounts")
    args = ap.parse_args()
    s = get_settings()
    radar = load_radar()
    topics = {t.name: t for t in load_topics()}
    picks = []
    for sec in load_sectors():
        if sec.key in args.skip:
            continue
        ranked = [t for t in (radar.topics if radar else []) if t.sector == sec.key and t.rank]
        best = min(ranked, key=lambda t: t.rank) if ranked else None
        if best and best.topic in topics:
            picks.append({"topic": best.topic, "terms": topics[best.topic].terms, "sector": sec.key})
    for p in picks:
        print(f"  {p['sector']:<18} {p['topic']}  terms={p['terms']}")
    if args.dry_run or not picks:
        return 0
    if not s.x_token_value():
        print("X_BEARER_TOKEN is not set")
        return 1
    x = XClient(s.x_token_value() or "")
    s = s.model_copy(update={"watch_x_discovery_topics_per_day": len(picks) + 10})   # this is an explicit one-off seed
    w = Watcher(s, x_client=x, accounts=[], router=None, openalex=None, patents_cached=None, watchlist_path=wl.WATCHLIST_PATH)
    state = load_state()
    w.discover_accounts_for(state, picks)
    save_state(state)
    for e in state.events[-(len(picks) * 4):]:
        if e["kind"] == "accounts":
            print(f"  [{e['kind']}] {e['detail']}")
    data = wl.load()
    print(f"\nwatched accounts now: {len(data['approved'])}  (agent-added: {sum(1 for a in data['approved'] if a.get('approved_by') == 'agent')})")
    print(f"X spend today (estimate): ${state.x_spent_today(w._now()):.2f}; this run: ${x.usage.cost_usd:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

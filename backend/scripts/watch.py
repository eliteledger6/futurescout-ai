"""Watch mode: keep scanning X, refresh the radar, and research rising topics automatically.

  python scripts\\watch.py --once          one cycle now
  python scripts\\watch.py --loop          run forever, one cycle every WATCH_X_INTERVAL_MINUTES (default 120)
  python scripts\\watch.py --once --no-research   scan and refresh, but start no research run

Costs per cycle: X ~ up to $0.25 (50 posts), papers free, patents from cache (a new topic may get one
live count, at most WATCH_NEW_PATENT_TOPICS_PER_WEEK per week), one research run ~$0.25 when triggered
(capped by WATCH_MAX_RUNS_PER_DAY). Every decision is logged to runs/watch_state.json and shown on the dashboard.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402

from app import service  # noqa: E402
from app.agents.x import load_watchlist  # noqa: E402
from app.config import get_settings, quiet_network_logs  # noqa: E402
from app.models.config import load_model_config  # noqa: E402
from app.models.router import ModelRouter  # noqa: E402
from app.sources.edgar_fulltext import EdgarFullTextClient  # noqa: E402
from app.sources.openalex import OpenAlexClient  # noqa: E402
from app.sources.serpapi_patents import SerpApiPatentsClient  # noqa: E402
from app.sources.x import XClient  # noqa: E402
from app.watch import Watcher  # noqa: E402


def report_ages() -> dict[str, datetime]:
    """Newest report time per topic, from the database if available, else from report files."""
    s = get_settings()
    out: dict[str, datetime] = {}
    try:
        if s.database_url_value():
            from app.db import list_runs, make_engine, make_session_factory
            with make_session_factory(make_engine(settings=s))() as db:
                for r in list_runs(db, limit=200):
                    t = r.generated_at if r.generated_at.tzinfo else r.generated_at.replace(tzinfo=timezone.utc)
                    out[r.topic.lower()] = max(out.get(r.topic.lower(), t), t)
            return out
    except Exception as exc:  # noqa: BLE001
        logging.getLogger("futurescout.watch").warning("database unavailable for report ages (%s); using files", type(exc).__name__)
    import json
    for p in service.RUNS_DIR.glob("report_*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            t = datetime.fromisoformat(d["generated_at"])
            out[d["topic"].lower()] = max(out.get(d["topic"].lower(), t), t)
        except Exception:  # noqa: BLE001
            continue
    return out


def build_watcher(research: bool) -> Watcher:
    s = get_settings()
    http = httpx.Client(timeout=30.0, headers={"User-Agent": s.http_user_agent}, follow_redirects=True)
    router = ModelRouter(load_model_config(), s) if s.near_ai_api_key else None
    x_client = XClient(s.x_token_value()) if s.x_token_value() else None
    patents_cached = SerpApiPatentsClient(s.serpapi_key_value() or "", cache_only=True) if s.serpapi_key_value() else None
    patents_live = (lambda: SerpApiPatentsClient(s.serpapi_key_value() or "", cache_only=False)) if s.serpapi_key_value() else None
    filers = None
    if s.edgar_user_agent:
        try:
            filers = EdgarFullTextClient(s.edgar_user_agent)
        except Exception:  # noqa: BLE001
            filers = None

    def run(topic: str):
        try:
            return service.execute(topic, s, news=False, warn=lambda m: print("   ", m)).run_id or "saved to files"
        except Exception as exc:  # noqa: BLE001
            print(f"    research run failed: {type(exc).__name__}: {str(exc)[:200]}")
            return None

    return Watcher(s, x_client=x_client, accounts=[a.handle for a in load_watchlist()], router=router,
                   openalex=OpenAlexClient(s.openalex_key_value(), http=http) if s.openalex_key_value() else None,
                   patents_cached=patents_cached, patents_live_factory=patents_live, filers=filers,
                   run_research=run if research else None, report_ages=report_ages)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--once", action="store_true")
    g.add_argument("--loop", action="store_true")
    ap.add_argument("--no-research", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.WARNING, format="%(name)s: %(message)s")
    quiet_network_logs()
    s = get_settings()
    while True:
        started = time.time()
        print(f"\n=== watch cycle {datetime.now(timezone.utc).isoformat(timespec='seconds')} ===")
        state = build_watcher(not args.no_research).cycle()
        for e in [e for e in state.events if e["at"] >= datetime.fromtimestamp(started, tz=timezone.utc).isoformat()]:
            print(f"  [{e['kind']:7}] {e['detail']}")
        if args.once:
            return 0
        wait = max(60, s.watch_x_interval_minutes * 60 - (time.time() - started))
        print(f"  next cycle in {wait / 60:.0f} min")
        time.sleep(wait)


if __name__ == "__main__":
    sys.exit(main())

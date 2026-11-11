"""Hot-Topic Radar: rank the topics in config/topics.yaml by growth in papers and patents.

  python scripts\\run_radar.py                 all topics (5 SerpApi searches per topic, cached 24 h)
  python scripts\\run_radar.py --no-patents    papers only (free)

Patents: Google Patents through SerpApi first (saved results only while SERPAPI_CACHE_ONLY=true); a topic it cannot count is
counted by EPO OPS (free) when the EPO keys are set. Each topic records which source counted it.

Writes backend/runs/radar.json, which the dashboard shows at /radar. No model calls.
Needs OPENALEX_API_KEY; patents need SERPAPI_API_KEY (or EPO keys); filer counts need EDGAR_USER_AGENT.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402

from app.config import get_settings, quiet_network_logs  # noqa: E402
from app.radar import carry_over_patents, compute_radar, load_radar, load_topics, save_radar  # noqa: E402
from app.sources.base import SourceError  # noqa: E402
from app.sources.edgar_fulltext import EdgarFullTextClient  # noqa: E402
from app.sources.epo import EpoOpsClient  # noqa: E402
from app.sources.openalex import OpenAlexClient  # noqa: E402
from app.sources.serpapi_patents import SerpApiPatentsClient  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-patents", action="store_true")
    ap.add_argument("--no-filers", action="store_true")
    ap.add_argument("--topic", action="append", help="only these topic names (repeatable)")
    args = ap.parse_args()
    quiet_network_logs()
    s = get_settings()

    topics = load_topics()
    if args.topic:
        wanted = {t.lower() for t in args.topic}
        topics = [t for t in topics if t.name.lower() in wanted]
    http = httpx.Client(timeout=30.0, headers={"User-Agent": s.http_user_agent}, follow_redirects=True)
    openalex = OpenAlexClient(s.openalex_key_value(), http=http) if s.openalex_key_value() else None
    patents = fallback = None
    if not args.no_patents:
        if s.serpapi_key_value():
            patents = SerpApiPatentsClient(s.serpapi_key_value() or "", cache_only=s.serpapi_cache_only)
            if s.epo_credentials():      # free: counts the topics Google Patents has no saved result for (owner 2026-11-11)
                from app.sources.base import RateLimiter
                fallback = EpoOpsClient(*s.epo_credentials(), limiter=RateLimiter(4.0))  # type: ignore[misc]  # EPO fair use: slow and steady
        elif s.epo_credentials():
            patents = EpoOpsClient(*s.epo_credentials())  # type: ignore[misc]
        else:
            print("No patent source configured (SERPAPI_API_KEY or EPO keys): patents skipped.")
    filers = None
    if not args.no_filers and s.edgar_user_agent:
        try:
            filers = EdgarFullTextClient(s.edgar_user_agent)
        except SourceError as exc:
            print(f"Filer counts skipped: {exc}")

    print(f"Radar over {len(topics)} topics (patents: {'yes' if patents else 'no'}, filers: {'yes' if filers else 'no'})...")
    previous = load_radar()
    radar = compute_radar(topics, openalex=openalex, patents=patents, filers=filers, patents_fallback=fallback)
    if not args.topic:
        kept = carry_over_patents(radar, previous)
        if kept:
            print(f"patent numbers kept from the earlier radar for {kept} topic(s) this run could not count")
    path = save_radar(radar)
    print(f"\n{'#':>2}  {'topic':28} {'papers Y-1->Y':>16} {'patents Y-1->Y':>16} {'heat':>7}")
    for t in radar.topics:
        pa, pt = t.paper_acceleration, t.patent_acceleration
        f = lambda a: f"{a.previous_year_count}->{a.last_full_year_count} ({a.yoy_growth_pct:+.0f}%)" if a and a.yoy_growth_pct is not None else "n/a"  # noqa: E731
        print(f"{t.rank if t.rank else '-':>2}  {t.topic:28} {f(pa):>16} {f(pt):>16} {('%+.1f%%' % t.heat) if t.heat is not None else 'n/a':>7}"
              + (f"   errors: {'; '.join(t.errors)}" if t.errors else ""))
    print(f"\nSerpApi searches used by this run: {radar.searches_used}\nSaved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

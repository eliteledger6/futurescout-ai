"""Regenerate as many reports as a set of budgets allows, one topic after another, never exceeding any budget.

  python scripts\\run_batch.py --model-usd 5 --openalex-usd 0.3 --x-usd 1 --serpapi-searches 40
  python scripts\\run_batch.py ... --dry-run          show the topic order and the budget rules; spend nothing

Order: topics that already have a report (newest first), then the hottest radar topic of each sector, then the rest
of the radar by rank. Before each run the script checks every budget against the WORST cost seen so far (or a
conservative estimate before the first run) and stops when the next run might not fit:
  * models (NEAR AI Cloud): stop when remaining < worst run cost x 1.2
  * OpenAlex: metered from OpenAlex's own cost header; stop when remaining < worst run cost x 1.2
  * SerpApi: live patent search while >= 6 searches remain (one topic = 5 yearly counts + 1 document search);
    the client refuses any search beyond the remaining budget, so the cap is hard. Afterwards: cache only.
  * X: the X agent runs while the remaining budget covers a worst case of 60 posts ($0.30); afterwards it is skipped.
Every run is sealed on NEAR testnet and saved like a normal run. A line per run goes to runs/batch_<time>.jsonl.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.config import ConfigError, get_settings, quiet_network_logs  # noqa: E402
from app.radar import load_radar, load_sectors  # noqa: E402

PATENT_SEARCHES_PER_TOPIC = 6
X_WORST_CASE_USD = 0.30
FIRST_RUN_MODEL_USD = 0.35
FIRST_RUN_OPENALEX_USD = 0.06   # 0.04 + ~0.02 for the phrase check (2026-11-09)
MARGIN = 1.2
ALL_AGENTS = ("chief", "science", "risk", "market", "x", "patent", "timing", "scout", "investment")
CHECK_URLS = ("https://api.openalex.org/", "https://cloud-api.near.ai/v1/models")
WAIT_FOR_NETWORK_S = 3600


def online() -> bool:
    """True when the two services every run needs answer at all (any HTTP status means the network is up)."""
    try:
        with httpx.Client(timeout=10.0) as c:
            for u in CHECK_URLS:
                c.get(u)
        return True
    except httpx.HTTPError:
        return False


def wait_until_online() -> bool:
    if online():
        return True
    print("    network is down: waiting (checking every minute, up to 60 minutes)...")
    deadline = time.time() + WAIT_FOR_NETWORK_S
    while time.time() < deadline:
        time.sleep(60)
        if online():
            print("    network is back")
            return True
    return False


def fresh_topics(settings, hours: float) -> set[str]:  # noqa: ANN001
    """Topics with a scored report younger than `hours` (they are not regenerated again)."""
    if hours <= 0:
        return set()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    out = set()
    for row in _default_store(settings).list(limit=200):
        if row.get("score") is not None and datetime.fromisoformat(row["generated_at"]) >= cutoff:
            out.add(row["topic"].lower())
    return out


def openalex_allowance_left(settings) -> "float | None":  # noqa: ANN001
    """OpenAlex's own remaining daily allowance in USD (one ~$0.001 request), or None if unknown."""
    from app.sources.openalex import OpenAlexClient
    try:
        client = OpenAlexClient(settings.openalex_key_value())
        client._get("/works", {"per-page": 1, "select": "id", "filter": "publication_year:2025"})
        return client.remaining_usd
    except Exception:  # noqa: BLE001
        return None


def sleep_until_openalex_reset() -> None:
    now = datetime.now(timezone.utc)
    nxt = (now + timedelta(days=1)).replace(hour=0, minute=10, second=0, microsecond=0)
    print(f"    OpenAlex's free daily allowance is nearly used up; waiting until {nxt:%Y-%m-%d %H:%M} UTC "
          f"(its reset; Alpha Vantage's daily price limit resets too)", flush=True)
    time.sleep(max(60.0, (nxt - now).total_seconds()))


def topic_order(settings) -> list[str]:  # noqa: ANN001
    seen: list[str] = []

    def add(t: str) -> None:
        if t and t.lower() not in {x.lower() for x in seen}:
            seen.append(t)
    for row in _default_store(settings).list(limit=100):
        add(row["topic"])
    radar = load_radar()
    ranked = sorted([t for t in (radar.topics if radar else []) if t.rank], key=lambda t: t.rank)
    for sec in load_sectors():
        best = next((t for t in ranked if t.sector == sec.key), None)
        if best:
            add(best.topic)
    for t in ranked:
        add(t.topic)
    return seen


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-usd", type=float, required=True)
    ap.add_argument("--openalex-usd", type=float, required=True)
    ap.add_argument("--x-usd", type=float, required=True)
    ap.add_argument("--serpapi-searches", type=int, required=True)
    ap.add_argument("--max-runs", type=int, default=50)
    ap.add_argument("--skip-fresh-hours", type=float, default=12.0, help="skip topics with a scored report younger than this")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--topics", help="';'-separated topics to run instead of the automatic order")
    ap.add_argument("--backup-topics", help="';'-separated topics to try when a topic does not get every agent")
    ap.add_argument("--wait-for-openalex-reset", action="store_true",
                    help="when OpenAlex's free daily allowance runs low, wait for its reset (00:00 UTC) instead of stopping")
    ap.add_argument("--margin", type=float, default=MARGIN, help="safety factor on the worst run cost seen (default 1.2)")
    ap.add_argument("--target-complete", type=int, default=0,
                    help="with --backup-topics: stop once this many runs in this batch had every agent")
    args = ap.parse_args()
    margin = args.margin
    quiet_network_logs()
    settings = get_settings()
    fresh = fresh_topics(settings, args.skip_fresh_hours)
    if args.topics:
        topics = [t.strip() for t in args.topics.split(";") if t.strip()][: args.max_runs]
    else:
        topics = [t for t in topic_order(settings) if t.lower() not in fresh][: args.max_runs]
    backups = [t.strip() for t in (args.backup_topics or "").split(";") if t.strip()]
    if fresh:
        print(f"skipping {len(fresh)} topic(s) with a scored report from the last {args.skip_fresh_hours:g} h: {sorted(fresh)}")
    print(f"{len(topics)} topics in order: {topics}")
    if args.dry_run:
        return 0

    left = {"model": args.model_usd, "openalex": args.openalex_usd, "x": args.x_usd, "serpapi": args.serpapi_searches}
    worst = {"model": FIRST_RUN_MODEL_USD, "openalex": FIRST_RUN_OPENALEX_USD}
    log_path = service.RUNS_DIR / f"batch_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.jsonl"
    done = []
    queue = list(topics)
    retried: set[str] = set()
    i = 0
    while queue:
        topic = queue.pop(0)
        i += 1
        if not wait_until_online():
            print("\nstop: the network stayed down for an hour")
            break
        if left["model"] < worst["model"] * margin:
            print(f"\nstop: model budget left ${left['model']:.3f} < next run estimate ${worst['model'] * margin:.3f}")
            break
        if args.wait_for_openalex_reset:
            allowance = openalex_allowance_left(settings)
            if allowance is not None and allowance < worst["openalex"] * margin:
                sleep_until_openalex_reset()
        if left["openalex"] < worst["openalex"] * margin:
            print(f"\nstop: OpenAlex budget left ${left['openalex']:.4f} < next run estimate ${worst['openalex'] * margin:.4f}")
            break
        patents_live = left["serpapi"] >= PATENT_SEARCHES_PER_TOPIC
        use_x = left["x"] >= X_WORST_CASE_USD
        print(f"\n[{i}] {topic}  (patents {'live' if patents_live else 'cache only'}, X {'on' if use_x else 'off'}; "
              f"left: models ${left['model']:.2f}, OpenAlex ${left['openalex']:.3f}, X ${left['x']:.2f}, SerpApi {left['serpapi']})")
        started = time.time()
        try:
            out = service.execute(topic, settings, news=False, use_x=use_x, patents_live=patents_live,
                                  patent_search_budget=left["serpapi"] if patents_live else 0, warn=lambda m: None)
            usage = out.usage or {}
        except ConfigError as exc:
            print(f"    stopped: {exc}")
            break
        except Exception as exc:  # noqa: BLE001  (charge the estimate: the run may have spent before failing)
            print(f"    run failed: {type(exc).__name__}: {str(exc)[:200]}")
            usage = {"model_usd": worst["model"], "openalex_usd": worst["openalex"], "x_usd": X_WORST_CASE_USD if use_x else 0,
                     "serpapi_searches": PATENT_SEARCHES_PER_TOPIC if patents_live else 0}
            out = None
        empty = out is not None and not out.report.agents_run
        if empty:
            # nothing analysed (network or provider outage): do not count it as a report; retry the topic once
            print("    no agent produced output (network or provider problem): not counted"
                  + ("; will retry after the connection check" if topic not in retried else "; skipped"))
            if out.run_id:
                import subprocess
                subprocess.run([sys.executable, str(Path(__file__).with_name("quarantine_runs.py")), "--run", out.run_id],
                               cwd=Path(__file__).resolve().parents[1])
            if topic not in retried:
                retried.add(topic)
                queue.insert(0, topic)
            time.sleep(30)
        left["model"] -= usage.get("model_usd", 0)
        left["openalex"] -= usage.get("openalex_usd", 0)
        left["x"] -= usage.get("x_usd", 0)
        left["serpapi"] -= usage.get("serpapi_searches", 0)
        worst["model"] = max(worst["model"] if not done else 0, usage.get("model_usd", 0), *(d["model_usd"] for d in done))
        worst["openalex"] = max(worst["openalex"] if not done else 0, usage.get("openalex_usd", 0), *(d["openalex_usd"] for d in done))
        row = {"topic": topic, "run_id": out.run_id if out else None, "seconds": round(time.time() - started),
               "score": (out.report.investment.score.score if out and out.report.investment and out.report.investment.score else None),
               "agents_run": out.report.agents_run if out else [], "sealed": bool(out and out.report.chain_record),
               **{k: usage.get(k, 0) for k in ("model_usd", "openalex_usd", "x_usd", "serpapi_searches")},
               "openalex_remaining_today_usd": usage.get("openalex_remaining_usd")}
        if empty:
            continue
        row["missing_agents"] = [a for a in ALL_AGENTS if a not in row["agents_run"]]
        done.append(row)
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        print(f"    done in {row['seconds']}s: score {row['score']}, agents {','.join(row['agents_run'])}; "
              f"models ${row['model_usd']:.3f}, OpenAlex ${row['openalex_usd']:.4f}, X ${row['x_usd']:.3f}, SerpApi {row['serpapi_searches']}"
              + (", sealed on NEAR" if row["sealed"] else ""))
        if row["missing_agents"]:
            print(f"    missing agents: {', '.join(row['missing_agents'])}")
            if backups:
                nxt = backups.pop(0)
                print(f"    adding backup topic: {nxt}")
                queue.append(nxt)
        complete = sum(1 for d in done if not d["missing_agents"])
        if args.target_complete and complete >= args.target_complete:
            print(f"\nstop: {complete} complete report(s) reached the target")
            break
        if (usage.get("openalex_remaining_usd") is not None and usage["openalex_remaining_usd"] < worst["openalex"] * margin
                and not args.wait_for_openalex_reset):
            print("\nstop: OpenAlex's own daily allowance is nearly used up")
            break

    spent = {"model_usd": round(args.model_usd - left["model"], 3), "openalex_usd": round(args.openalex_usd - left["openalex"], 4),
             "x_usd": round(args.x_usd - left["x"], 3), "serpapi_searches": args.serpapi_searches - left["serpapi"]}
    print(f"\n{len(done)} report(s) generated. Spent: {spent} (budgets: models ${args.model_usd}, OpenAlex ${args.openalex_usd}, "
          f"X ${args.x_usd}, SerpApi {args.serpapi_searches}). Log: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

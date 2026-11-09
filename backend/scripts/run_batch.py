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
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.config import ConfigError, get_settings, quiet_network_logs  # noqa: E402
from app.radar import load_radar, load_sectors  # noqa: E402

PATENT_SEARCHES_PER_TOPIC = 6
X_WORST_CASE_USD = 0.30
FIRST_RUN_MODEL_USD = 0.35
FIRST_RUN_OPENALEX_USD = 0.04
MARGIN = 1.2


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
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    quiet_network_logs()
    settings = get_settings()
    topics = topic_order(settings)[: args.max_runs]
    print(f"{len(topics)} topics in order: {topics}")
    if args.dry_run:
        return 0

    left = {"model": args.model_usd, "openalex": args.openalex_usd, "x": args.x_usd, "serpapi": args.serpapi_searches}
    worst = {"model": FIRST_RUN_MODEL_USD, "openalex": FIRST_RUN_OPENALEX_USD}
    log_path = service.RUNS_DIR / f"batch_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.jsonl"
    done = []
    for i, topic in enumerate(topics, 1):
        if left["model"] < worst["model"] * MARGIN:
            print(f"\nstop: model budget left ${left['model']:.3f} < next run estimate ${worst['model'] * MARGIN:.3f}")
            break
        if left["openalex"] < worst["openalex"] * MARGIN:
            print(f"\nstop: OpenAlex budget left ${left['openalex']:.4f} < next run estimate ${worst['openalex'] * MARGIN:.4f}")
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
        done.append(row)
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        print(f"    done in {row['seconds']}s: score {row['score']}, agents {','.join(row['agents_run'])}; "
              f"models ${row['model_usd']:.3f}, OpenAlex ${row['openalex_usd']:.4f}, X ${row['x_usd']:.3f}, SerpApi {row['serpapi_searches']}"
              + (", sealed on NEAR" if row["sealed"] else ""))
        if usage.get("openalex_remaining_usd") is not None and usage["openalex_remaining_usd"] < worst["openalex"] * MARGIN:
            print("\nstop: OpenAlex's own daily allowance is nearly used up")
            break

    spent = {"model_usd": round(args.model_usd - left["model"], 3), "openalex_usd": round(args.openalex_usd - left["openalex"], 4),
             "x_usd": round(args.x_usd - left["x"], 3), "serpapi_searches": args.serpapi_searches - left["serpapi"]}
    print(f"\n{len(done)} report(s) generated. Spent: {spent} (budgets: models ${args.model_usd}, OpenAlex ${args.openalex_usd}, "
          f"X ${args.x_usd}, SerpApi {args.serpapi_searches}). Log: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

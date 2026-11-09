"""Run the Science Research Agent on a real topic with REAL data.

Usage (from the backend folder, venv active):

  # 1) Retrieval only: real OpenAlex + arXiv data, no model call, no NEAR key needed
  python scripts/demo_science.py --topic "high bandwidth memory" --no-llm

  # 2) Full run: retrieval + analysis by the model assigned to "science" in model_config.yaml
  python scripts/demo_science.py --topic "high bandwidth memory" --from-year 2023

OpenAlex needs OPENALEX_API_KEY in .env (free account). Results are saved to backend/runs/.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402

from app.agents.science import ScienceAgent  # noqa: E402
from app.config import BACKEND_DIR, ConfigError, get_settings  # noqa: E402
from app.models.config import load_model_config  # noqa: E402
from app.models.router import ModelRouter  # noqa: E402
from app.sources.arxiv import ArxivClient  # noqa: E402
from app.sources.openalex import OpenAlexClient  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--query", action="append", help="extra search query (repeatable)")
    parser.add_argument("--from-year", type=int, default=None, help="earliest paper year (default: last 3 years)")
    parser.add_argument("--max-papers", type=int, default=12)
    parser.add_argument("--no-llm", action="store_true", help="retrieval only; skips the model call")
    args = parser.parse_args()

    settings = get_settings()
    if not settings.openalex_key_value():
        print("WARNING: OPENALEX_API_KEY is not set. OpenAlex only allows a tiny test allowance without a key.\n")

    http = httpx.Client(timeout=30.0, headers={"User-Agent": settings.http_user_agent}, follow_redirects=True)
    router = None
    if not args.no_llm:
        try:
            settings.require_near_key()
        except ConfigError as exc:
            print(f"ERROR: {exc}\n(Use --no-llm to test data retrieval without a NEAR AI key.)")
            return 1
        router = ModelRouter(load_model_config(), settings)

    agent = ScienceAgent(
        router,
        openalex=OpenAlexClient(settings.openalex_key_value(), http=http),
        arxiv=ArxivClient(http=http),
    )
    queries = [args.topic, *(args.query or [])]
    result = agent.run(args.topic, queries=queries, from_year=args.from_year,
                       max_papers=args.max_papers, use_llm=not args.no_llm)

    print(f"Topic: {result.topic}\nStatus: {result.status}\nPapers retrieved: {len(result.sources)}")
    print(f"Coverage: {result.coverage_note}\n")
    print(f"Papers searched from year: {result.from_year}")
    if result.publication_counts:
        print("OpenAlex works per year (exact phrase in title/abstract):", result.publication_counts)
    if result.acceleration:
        a = result.acceleration
        print(f"Research Acceleration: {a.previous_year}={a.previous_year_count} -> "
              f"{a.last_full_year}={a.last_full_year_count} (YoY {a.yoy_growth_pct}%)")
        print(f"  basis: {a.basis}")
    print("\n--- Sources (real, from the APIs) ---")
    for s in result.sources:
        print(f"[{s.id}] {s.title} ({s.published_at}, {s.source_name}, {s.text_depth})\n    {s.url}")
    if result.findings:
        print("\n--- Findings ---")
        for f in result.findings:
            print(f"* [{f.label.value} | {f.confidence.value}] {f.claim}")
            for sid in f.source_ids:
                print(f"    source: {next((s.url for s in result.sources if s.id == sid), sid)}")
            if f.guard_note:
                print(f"    guard: {f.guard_note}")
        for title, items in (("Emerging directions", result.emerging_directions),
                             ("Open problems", result.open_problems), ("Limitations", result.limitations)):
            if items:
                print(f"\n{title}:")
                for item in items:
                    print(f"  - {item}")
    if result.errors:
        print("\n--- Errors (not hidden) ---")
        for e in result.errors:
            print(f"  {e.source}: {e.message}")
    if router and router.usage:
        print("\n--- Model usage (estimated cost) ---")
        for row in router.usage_summary():
            print(f"  {row['agent']:10} {row['model']:34} calls={row['calls']} "
                  f"tokens={row['prompt_tokens']}/{row['completion_tokens']} cost=${row['cost_usd']:.5f}")

    runs = BACKEND_DIR / "runs"
    runs.mkdir(exist_ok=True)
    out = runs / f"science_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    out.write_text(json.dumps({"result": result.model_dump(mode="json"),
                               "usage": [u.model_dump(mode="json") for u in (router.usage if router else [])]},
                              indent=2), encoding="utf-8")
    print(f"\nSaved: {out}")
    return 0 if result.status != "no_data" else 2


if __name__ == "__main__":
    raise SystemExit(main())

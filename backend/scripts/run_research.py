"""Run the full multi-agent research pipeline on one topic and write a report.

Usage (from the backend folder, venv active):
    python scripts\\run_research.py --topic "high bandwidth memory"

Needs NEAR_AI_API_KEY (models) and OPENALEX_API_KEY (papers) in .env, and NEAR AI credit.
EDGAR_USER_AGENT (your name + contact email) enables the Market agent's SEC filings.
Outputs go to backend/runs/: report_<time>.md (readable) and report_<time>.json (full data).
If DATABASE_URL is set, the run is also saved to PostgreSQL (see scripts/db_check.py).

Which agents run: Chief, Science, Patent, Market (SEC filings + GDELT news headlines; --no-news skips news),
X (--no-x skips it), Risk (independent + challenge, price timing) and Investment. An agent whose source is not
configured or refuses the request is listed in the report as having no analysed evidence.
The report's fingerprint is sealed on NEAR (the network in SEAL_NETWORK) unless --no-near is given.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.config import ConfigError, get_settings, quiet_network_logs  # noqa: E402


def save_to_database(settings, report, markdown: str):
    """Kept for the tests and other callers; the logic lives in app/service.py."""
    return service.save_to_database(settings, report, markdown, print)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--question", help="optional specific question the report should address")
    parser.add_argument("--sector", help="sector key from config/sectors.yaml (default: looked up from topics.yaml, else generic technology)")
    parser.add_argument("--from-year", type=int, default=None, help="earliest paper year (default: last 3 years)")
    parser.add_argument("--max-papers", type=int, default=12)
    parser.add_argument("--no-news", action="store_true", help="skip the GDELT news headline search")
    parser.add_argument("--no-x", action="store_true", help="skip the X agent (saves ~$0.15 of X API credit)")
    parser.add_argument("--no-near", action="store_true", help="do not seal the report fingerprint on NEAR")
    parser.add_argument("--no-fund", action="store_true", help="do not build the topic's paper fund after the report")
    parser.add_argument("--no-db", action="store_true", help="do not save the run to PostgreSQL even if DATABASE_URL is set")
    parser.add_argument("-v", "--verbose", action="store_true", help="log each model call (agent, model, tokens, cost)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING, format="%(name)s: %(message)s")
    quiet_network_logs()
    settings = get_settings()
    print(f"Researching: {args.topic}\n(this makes several model calls and a few API searches; it can take a few minutes)\n")
    try:
        outcome = service.execute(args.topic, settings, question=args.question, sector=args.sector, news=not args.no_news, use_x=not args.no_x, record_on_near=not args.no_near,
                                  from_year=args.from_year, max_papers=args.max_papers, save_db=not args.no_db)
    except ConfigError as exc:
        print(f"ERROR: {exc}")
        return 1
    report, md_path, json_path, run_id = outcome.report, outcome.md_path, outcome.json_path, outcome.run_id

    print(f"Agents that produced output: {', '.join(report.agents_run) or 'none'}")
    print(f"Agents with no analysed evidence: {', '.join(report.agents_not_run)}")
    if report.investment and report.investment.score:
        sc = report.investment.score
        print(f"Score: {sc.score if sc.reportable else 'not reportable'} (evidence coverage {sc.coverage:.0%})")
    print(f"Errors: {len(report.errors)}")
    for e in report.errors:
        print(f"  [{e.agent}/{e.source}] {e.message}")
    print(f"Estimated model cost: ${report.total_cost_usd:.5f}")
    if not args.no_fund and report.investment and report.investment.score:   # every new report gets its paper fund (owner 2026-11-11)
        from app.paper_fund_hook import build_paper_fund
        build_paper_fund(report.topic)
    for u in report.usage:
        print(f"  {u['agent']:11} {u['model']:34} calls={u['calls']} tokens={u['prompt_tokens']}/{u['completion_tokens']} ${u['cost_usd']:.5f}")
    print(f"\nReport: {md_path}\nData:   {json_path}")
    if run_id:
        print(f"Saved to database as run {run_id}")
    if report.chain_record:
        print(f"Fingerprint recorded on NEAR {report.chain_record.get('network', 'testnet')}: {report.chain_record['sha256'][:16]}…  {report.chain_record['explorer_url']}")
    return 0 if report.investment and report.investment.draft else 2


if __name__ == "__main__":
    raise SystemExit(main())

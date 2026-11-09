"""Re-run ONLY the Investment agent (themes, ratings, score) on a saved report and store the result.

  python scripts\\rescore.py --run <id>            re-score one saved run
  python scripts\\rescore.py --run <id> --reseal   ...and record the new fingerprint on NEAR testnet

--recount also redoes the paper counts with the synonym/AI-relevance phrase check (2026-11-09) before re-scoring.

Use after a scoring-prompt change (e.g. the 2026-11-09 risk scale) so an existing report reflects it without
re-collecting papers, patents, filings or prices. Costs one Investment-agent model call (about $0.02); the call is
added to the report's usage as "investment (rescore)". The evidence (findings and sources) is unchanged. The old
NEAR record is stale after any edit, so --reseal records the new fingerprint (testnet only).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.agents.investment.agent import InvestmentAgent  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.models.config import load_model_config  # noqa: E402
from app.models.router import ModelRouter  # noqa: E402
from app.report import render_markdown  # noqa: E402
from app.schemas.research import ResearchReport  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--reseal", action="store_true")
    ap.add_argument("--recount", action="store_true",
                    help="first redo the paper counts with the synonym/AI-relevance phrase check (OpenAlex, ~$0.02)")
    args = ap.parse_args()
    s = get_settings()

    report = None
    sessions = None
    if s.database_url_value():
        from app.db import make_engine, make_session_factory
        from app.db.models import Run
        sessions = make_session_factory(make_engine(settings=s))
        with sessions() as db:
            row = db.get(Run, args.run)
            if row:
                report = ResearchReport.model_validate(row.report_json)
    file_path = service.RUNS_DIR / f"{args.run}.json"
    if report is None and file_path.is_file():
        report = ResearchReport.model_validate(json.loads(file_path.read_text(encoding="utf-8")))
    if report is None:
        print(f"run {args.run} not found")
        return 1

    router = ModelRouter(load_model_config(), s)
    if args.recount and report.science:
        from datetime import datetime, timezone
        from app.agents.science.metrics import compute_acceleration, ytd_from_client
        from app.agents.science.phrases import build_counting_basis
        from app.sources.openalex import OpenAlexClient
        oa = OpenAlexClient(s.openalex_key_value())
        basis = build_counting_basis(oa, router, report.topic)
        if basis is None or not basis.phrases:
            print(f"{report.topic}: phrase check failed; report left unchanged")
            return 1
        year = datetime.now(timezone.utc).year
        sci = report.science
        before = (sci.acceleration.last_full_year_count if sci.acceleration else None)
        sci.counting = basis
        sci.publication_counts = oa.count_by_year(basis.phrases, year - 6)
        sci.acceleration = compute_acceleration(sci.publication_counts, year, phrase=basis.phrases)
        sci.ytd = ytd_from_client(oa, basis.phrases, datetime.now(timezone.utc).date())
        print(f"{report.topic}: counted phrases {basis.phrases}; last full year {before} -> "
              f"{sci.acceleration.last_full_year_count if sci.acceleration else None} works; OpenAlex ${oa.cost_usd:.3f}")
    old = report.investment.score if report.investment else None
    result = InvestmentAgent(router).run(
        report.topic, report.science, report.risk, agents_not_run=report.agents_not_run, question=report.question,
        market=report.market, x=report.x, patent=report.patent, timing=report.timing, scout=report.scout,
    )
    if result.status != "ok" or result.score is None or result.score.score is None:
        print(f"{report.topic}: re-score failed ({result.status}); report left unchanged")
        for e in result.errors:
            print("  ", e.message[:200])
        return 1
    report.investment = result
    added = router.usage_summary()
    for u in added:
        u["agent"] = f"{u.get('agent', 'investment')} (rescore)"
    report.usage.extend(added)
    report.total_cost_usd = round(sum(u.get("cost_usd", 0.0) for u in report.usage), 6)
    new = result.score
    print(f"{report.topic}: score {old.score if old else None} (risk {old.risk_rating if old else None}) -> "
          f"{new.score} (base {new.base_score}, risk {new.risk_rating}); cost ${sum(u.get('cost_usd', 0) for u in added):.4f}")

    md = render_markdown(report)
    if sessions:
        with sessions() as db:
            from app.db.models import Run
            row = db.get(Run, args.run)
            if row:
                row.report_json = report.model_dump(mode="json")
                row.report_markdown = md
                row.score = new.score
                row.score_reportable = new.reportable
                row.score_coverage = new.coverage
                row.total_cost_usd = report.total_cost_usd
                db.commit()
                print("database row updated")
    if file_path.is_file():
        file_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        file_path.with_suffix(".md").write_text(md, encoding="utf-8")
        print(f"files updated: {file_path.name}")
    if args.reseal:
        r = subprocess.run([sys.executable, "scripts/near_record_report.py", "--run", args.run, "--force"],
                           cwd=Path(__file__).resolve().parents[1])
        return r.returncode
    print("note: the stored NEAR record is now stale for this run; re-run with --reseal to record the new fingerprint")
    return 0


if __name__ == "__main__":
    sys.exit(main())

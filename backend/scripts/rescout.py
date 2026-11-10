"""Re-run the Company Scout (code only, no model) on a saved report and store the result.

  python scripts\\rescout.py --run <id>            re-score the companies of one saved run
  python scripts\\rescout.py --run <id> --reseal   ...and record the new fingerprint on NEAR testnet (the old record is stale after any edit)

Use after a scout rule change (e.g. the SEC industry filter) so an existing report reflects it. The Investment
agent's text is NOT regenerated (that would cost model credit), so its themes may still name companies the new
scout demotes; the report's Emerging-companies section is what changes. The report is re-rendered to Markdown and
saved to the database (if configured) and to backend/runs/<file>.json/.md when the run came from a file.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.report import render_markdown  # noqa: E402
from app.scout import CompanyScout  # noqa: E402
from app.sources.edgar import EdgarClient  # noqa: E402
from app.sources.sec_facts import SecFactsClient  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--reseal", action="store_true")
    args = ap.parse_args()
    s = get_settings()
    if not s.edgar_user_agent:
        print("EDGAR_USER_AGENT is not set")
        return 1
    edgar, facts = EdgarClient(s.edgar_user_agent), SecFactsClient(s.edgar_user_agent)
    scout = CompanyScout(edgar, facts)

    report = None
    sessions = None
    if s.database_url_value():
        from app.db import make_engine, make_session_factory
        from app.db.models import Run
        from app.schemas.research import ResearchReport
        sessions = make_session_factory(make_engine(settings=s))
        with sessions() as db:
            row = db.get(Run, args.run)
            if row:
                report = ResearchReport.model_validate(row.report_json)
    file_path = service.RUNS_DIR / f"{args.run}.json"
    if report is None and file_path.is_file():
        from app.schemas.research import ResearchReport
        report = ResearchReport.model_validate(json.loads(file_path.read_text(encoding="utf-8")))
    if report is None:
        print(f"run {args.run} not found")
        return 1

    before = [(c.ticker, c.next_runner_score) for c in (report.scout.candidates if report.scout else [])]
    report.scout = scout.run(report.topic, report.science, report.market, report.patent)
    if "scout" not in report.agents_run and report.scout.status == "ok":
        report.agents_run.append("scout")
    after = [(c.ticker, c.next_runner_score, "OFF" if c.off_sector else "") for c in report.scout.candidates]
    print(f"{report.topic}: candidates before {before}\n  after {after}")
    md = render_markdown(report)
    if sessions:
        with sessions() as db:
            from app.db.models import Run
            row = db.get(Run, args.run)
            if row:
                row.report_json = report.model_dump(mode="json")
                row.report_markdown = md
                db.commit()
                print("database row updated")
    if file_path.is_file():
        file_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        file_path.with_suffix(".md").write_text(md, encoding="utf-8")
        print(f"files updated: {file_path.name}")
    if args.reseal:
        r = subprocess.run([sys.executable, "scripts/near_record_report.py", "--run", args.run, "--force"], cwd=Path(__file__).resolve().parents[1])
        return r.returncode
    print("note: the stored NEAR record is now stale for this run; re-run with --reseal to record the new fingerprint")
    return 0


if __name__ == "__main__":
    sys.exit(main())

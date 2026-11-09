"""Record an existing report's SHA-256 fingerprint on NEAR testnet (for reports made before the
record feature existed, or when the record failed during the run).

  python scripts\\near_record_report.py --run <database run id or report_<time> file name>
  python scripts\\near_record_report.py --latest

Writes the record into the saved report (database row and/or JSON file) so the dashboard badge and
the marketplace show it. Costs 0.01 testnet NEAR (storage). Needs NEAR_TESTNET_ACCOUNT_ID/PRIVATE_KEY.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.chain import NearRecorder, NearRecordError  # noqa: E402
from app.config import get_settings, quiet_network_logs  # noqa: E402
from app.db import list_runs, make_engine, make_session_factory  # noqa: E402
from app.db.models import Run  # noqa: E402
from app.schemas.research import ResearchReport  # noqa: E402
from app.service import RUNS_DIR  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--run")
    g.add_argument("--latest", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="re-record even if a chain record exists (use after a fingerprint-rule change made an old record stale)")
    args = ap.parse_args()
    quiet_network_logs()
    s = get_settings()
    creds = s.near_testnet_credentials()
    if not creds:
        print("NEAR_TESTNET_ACCOUNT_ID / NEAR_TESTNET_PRIVATE_KEY are not set.")
        return 1

    sessions = make_session_factory(make_engine(settings=s)) if s.database_url_value() else None
    run_id = args.run
    if args.latest:
        if not sessions:
            print("--latest needs DATABASE_URL")
            return 1
        with sessions() as db:
            runs = list_runs(db, limit=1)
        if not runs:
            print("no runs in the database")
            return 1
        run_id = runs[0].id

    report = None
    db_row = None
    if sessions:
        with sessions() as db:
            db_row = db.get(Run, run_id)
            if db_row:
                report = ResearchReport.model_validate(db_row.report_json)
    file_path = RUNS_DIR / f"{run_id}.json"
    if report is None and file_path.is_file():
        report = ResearchReport.model_validate(json.loads(file_path.read_text(encoding="utf-8")))
    if report is None:
        print(f"run {run_id} not found in the database or in {RUNS_DIR}")
        return 1
    if report.chain_record and not args.force:
        print(f"already recorded: {report.chain_record.get('explorer_url')}  (use --force to re-record)")
        return 0

    try:
        rec = NearRecorder(*creds).record(run_id, report)
    except NearRecordError as exc:
        print(f"ERROR: {exc}")
        return 1
    report.chain_record = rec.as_dict()
    if sessions and db_row is not None:
        with sessions() as db:
            row = db.get(Run, run_id)
            row.report_json = report.model_dump(mode="json")
            db.commit()
        print("database row updated")
    if file_path.is_file():
        file_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        print(f"file updated: {file_path.name}")
    print(f"Recorded on NEAR testnet: sha256 {rec.sha256}\n{rec.explorer_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

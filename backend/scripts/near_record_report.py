"""Seal an existing report's SHA-256 fingerprint on NEAR (for reports made before sealing existed, when the seal failed
during the run, or to move old testnet seals to mainnet).

  python scripts\\near_record_report.py --run <database run id or report_<time> file name>
  python scripts\\near_record_report.py --latest
  python scripts\\near_record_report.py --all --dry-run    list the reports not yet sealed on the current network
  python scripts\\near_record_report.py --all              seal each of them (one transaction per report)

The network comes from SEAL_NETWORK in .env: "testnet" (default, NEAR_TESTNET_ACCOUNT_ID / NEAR_TESTNET_PRIVATE_KEY) or
"mainnet" (signed by the report agent, REPORT_AGENT_ACCOUNT_ID / REPORT_AGENT_PRIVATE_KEY). On mainnet the first seal
locks a 0.1 NEAR storage deposit in social.near; every seal then costs about 0.004 NEAR of gas and storage. Mainnet
seals are run by the owner only. Writes the new record into the saved report (database row and/or JSON file) so the
website badge and the report market show it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.chain import NearRecordError, make_recorder  # noqa: E402
from app.config import get_settings, quiet_network_logs  # noqa: E402
from app.db import list_runs, make_engine, make_session_factory  # noqa: E402
from app.db.models import Run  # noqa: E402
from app.schemas.research import ResearchReport  # noqa: E402
from app.service import RUNS_DIR  # noqa: E402


def load(run_id: str, sessions):  # noqa: ANN001, ANN201
    if sessions:
        with sessions() as db:
            row = db.get(Run, run_id)
            if row:
                return ResearchReport.model_validate(row.report_json), True
    path = RUNS_DIR / f"{run_id}.json"
    if path.is_file():
        return ResearchReport.model_validate(json.loads(path.read_text(encoding="utf-8"))), False
    return None, False


def save(run_id: str, report: ResearchReport, in_db: bool, sessions) -> None:  # noqa: ANN001
    if sessions and in_db:
        with sessions() as db:
            row = db.get(Run, run_id)
            row.report_json = report.model_dump(mode="json")
            db.commit()
    path = RUNS_DIR / f"{run_id}.json"
    if path.is_file():
        path.write_text(report.model_dump_json(indent=2), encoding="utf-8")


BUSY = re.compile(r"(?i)429|rate limit|not available|timeout|timed out|connect|503|502")
WAITS = (20, 60, 120)          # seconds to wait after a busy RPC before trying the same report again


def seal_with_retry(recorder, run_id: str, report: ResearchReport, sleep=time.sleep, log=print):  # noqa: ANN001, ANN201
    """One seal; when the public RPC is busy (rate limit, not available), wait and try again. Re-sending is safe: the
    seal writes the same fingerprint again, costing only gas (the storage deposit is never paid twice)."""
    for i in range(len(WAITS) + 1):
        try:
            return recorder.record(run_id, report)
        except NearRecordError as exc:
            if i == len(WAITS) or not BUSY.search(str(exc)):
                raise
            log(f"  RPC busy, waiting {WAITS[i]}s then retrying {run_id[:8]}")
            sleep(WAITS[i])
    raise AssertionError("unreachable")


def all_run_ids(sessions) -> list[str]:  # noqa: ANN001
    if sessions:
        with sessions() as db:
            return [r.id for r in list_runs(db, limit=1000)]
    return [p.stem for p in sorted(RUNS_DIR.glob("report_*.json"))]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--run")
    g.add_argument("--latest", action="store_true")
    g.add_argument("--all", action="store_true", help="every report not yet sealed on the current network")
    ap.add_argument("--force", action="store_true", help="re-seal even if a record on this network exists")
    ap.add_argument("--dry-run", action="store_true", help="only list what would be sealed")
    ap.add_argument("--pause", type=float, default=4.0, help="seconds between seals (the free RPC rate-limits bursts)")
    args = ap.parse_args()
    quiet_network_logs()
    s = get_settings()
    network = (s.seal_network or "testnet").lower()
    try:
        recorder = make_recorder(s)
    except NearRecordError as exc:
        print(f"ERROR: {exc}")
        return 1
    if recorder is None:
        print("No seal account set: NEAR_TESTNET_ACCOUNT_ID / NEAR_TESTNET_PRIVATE_KEY (testnet) or SEAL_NETWORK=mainnet "
              "with REPORT_AGENT_ACCOUNT_ID / REPORT_AGENT_PRIVATE_KEY.")
        return 1

    sessions = make_session_factory(make_engine(settings=s)) if s.database_url_value() else None
    ids = all_run_ids(sessions)
    if args.run:
        ids = [args.run]
    elif args.latest:
        ids = ids[:1] if sessions else ids[-1:]
    if not ids:
        print("no reports found")
        return 1

    todo = []
    for run_id in ids:
        report, in_db = load(run_id, sessions)
        if report is None:
            print(f"run {run_id} not found in the database or in {RUNS_DIR}")
            continue
        rec = report.chain_record or {}
        if rec and (rec.get("network") or "testnet") == network and not args.force:
            if not args.all:
                print(f"already sealed on {network}: {rec.get('explorer_url')}  (use --force to re-seal)")
            continue
        todo.append((run_id, report, in_db))
    print(f"{len(todo)} report(s) to seal on NEAR {network} as {recorder.account_id}")
    if args.dry_run:
        for run_id, report, _ in todo:
            print(f"  {run_id}  {report.topic[:60]}")
        return 0

    failed = in_a_row = 0
    n = -1
    for n, (run_id, report, in_db) in enumerate(todo):
        if n:
            time.sleep(args.pause)
        try:
            rec = seal_with_retry(recorder, run_id, report)
        except NearRecordError as exc:
            failed += 1
            in_a_row += 1
            print(f"  ERROR {run_id}: {exc}")
            if in_a_row >= 3:
                print("three failures in a row: stopping. Run the same command later; sealed reports are skipped.")
                break
            continue
        in_a_row = 0
        report.chain_record = rec.as_dict()
        save(run_id, report, in_db, sessions)
        print(f"  sealed {run_id}  {report.topic[:40]}  {rec.explorer_url}")
    print(f"done: {n + 1 - failed} sealed, {failed} failed, {len(todo) - n - 1} not tried")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

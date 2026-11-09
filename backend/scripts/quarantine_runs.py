"""Move broken runs out of the dashboard without losing them.

  python scripts\\quarantine_runs.py --run <id> [--run <id> ...]    move these database runs
  python scripts\\quarantine_runs.py --empty-since 2026-11-09T07:30   move every run since then that has no score and no agent output

Each run's full report JSON (and Markdown) is first written to backend/runs/quarantine/<id>.json/.md, then the
database row is removed (findings, sources and usage rows go with it via ON DELETE CASCADE) and the matching
backend/runs/report_<time>.json/.md files are moved into the same folder. Nothing is lost: a quarantined run can be
restored with scripts/db_import.py or by moving the files back. Runs sealed on NEAR are never touched.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.db import make_engine, make_session_factory  # noqa: E402
from app.db.models import Run  # noqa: E402
from app.schemas.research import ResearchReport  # noqa: E402

QUARANTINE = service.RUNS_DIR / "quarantine"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="append", default=[])
    ap.add_argument("--empty-since", help="ISO time (UTC); runs at or after it with no score and no agent output")
    args = ap.parse_args()
    s = get_settings()
    if not s.database_url_value():
        print("DATABASE_URL is not set")
        return 1
    sessions = make_session_factory(make_engine(settings=s))
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    moved = 0
    with sessions() as db:
        rows = [db.get(Run, rid) for rid in args.run]
        if args.empty_since:
            since = datetime.fromisoformat(args.empty_since)
            for row in db.query(Run).all():
                rep = ResearchReport.model_validate(row.report_json)
                if rep.generated_at.replace(tzinfo=None) >= since and not rep.chain_record and \
                        not (rep.investment and rep.investment.score and rep.investment.score.score is not None):
                    rows.append(row)
        for row in {r.id: r for r in rows if r is not None}.values():
            rep = ResearchReport.model_validate(row.report_json)
            if rep.chain_record:
                print(f"  {row.id}: sealed on NEAR, left alone")
                continue
            (QUARANTINE / f"{row.id}.json").write_text(json.dumps(row.report_json, indent=2), encoding="utf-8")
            if row.report_markdown:
                (QUARANTINE / f"{row.id}.md").write_text(row.report_markdown, encoding="utf-8")
            stamp = rep.generated_at.strftime("%Y%m%dT%H%M%S")
            for f in service.RUNS_DIR.glob(f"report_{stamp}*"):
                shutil.move(str(f), QUARANTINE / f.name)
            db.delete(row)
            moved += 1
            print(f"  quarantined {row.id}: {rep.topic} (agents: {', '.join(rep.agents_run) or 'none'})")
        db.commit()
    print(f"{moved} run(s) moved to {QUARANTINE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

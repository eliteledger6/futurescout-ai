"""Check the database connection and list saved research runs.

  python scripts\\db_check.py              connection, schema version, last 10 runs
  python scripts\\db_check.py --show RUN_ID  print the saved Markdown report of one run

Needs DATABASE_URL in .env. Create the tables first with:  python -m alembic upgrade head
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import inspect, text  # noqa: E402

from app.config import ConfigError, get_settings  # noqa: E402
from app.db import list_runs, make_engine, make_session_factory, safe_url  # noqa: E402
from app.db.models import Run  # noqa: E402
from app.db.session import normalise_url  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--show", metavar="RUN_ID")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    url = get_settings().database_url_value()
    try:
        engine = make_engine(url)
    except ConfigError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Database: {safe_url(normalise_url(url or ''))}")
    try:
        with engine.connect() as conn:
            print(f"Connected. Server: {conn.execute(text('select version()')).scalar()}")
            tables = set(inspect(conn).get_table_names())
            if "alembic_version" not in tables:
                print("No tables yet. Create them with:  python -m alembic upgrade head")
                return 1
            print(f"Schema version: {conn.execute(text('select version_num from alembic_version')).scalar()}")
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: could not connect ({type(exc).__name__}: {str(exc).splitlines()[0][:200]})")
        print("Check that PostgreSQL is running and that DATABASE_URL (user, password, database name) is right.")
        return 1

    with make_session_factory(engine)() as session:
        if args.show:
            run = session.get(Run, args.show)
            if not run:
                print(f"No run with id {args.show}")
                return 1
            print(run.report_markdown or "(no Markdown stored)")
            return 0
        runs = list_runs(session, limit=args.limit)
        print(f"\n{len(runs)} most recent run(s):")
        for r in runs:
            score = (f"{r.score}" if r.score_reportable else "not reportable") if r.score is not None else "none"
            print(f"  {r.id}  {r.generated_at:%Y-%m-%d %H:%M}  {r.topic[:40]:40}  agents={','.join(r.agents_run) or 'none'}  "
                  f"findings={r.findings} sources={r.sources} score={score} cost=${r.total_cost_usd:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

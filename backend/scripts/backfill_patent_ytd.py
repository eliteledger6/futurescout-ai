"""Add the patent year-to-date comparison to saved reports that do not have it yet (added 2026-11-09).

  python scripts\\backfill_patent_ytd.py            latest report of every topic (dry: prints only)
  python scripts\\backfill_patent_ytd.py --apply    save the reports (database + files)
  python scripts\\backfill_patent_ytd.py --apply --reseal   ...and record new fingerprints on NEAR testnet

Counts come from EPO OPS (free) with the report's own patent search terms: patents published 1 Jan -> cutoff this
year vs the same dates last year. For reports whose yearly patent counts came from Google Patents (SerpApi), the
basis text says the year-to-date numbers are EPO's, so the two are not mixed silently. No model is called.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.science.metrics import patent_ytd  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.report import render_markdown  # noqa: E402
from app.schemas.research import ResearchReport  # noqa: E402
from app.sources.base import SourceError  # noqa: E402
from app.sources.epo import EpoOpsClient  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reseal", action="store_true")
    args = ap.parse_args()
    s = get_settings()
    creds = s.epo_credentials()
    if not creds or not s.database_url_value():
        print("needs EPO keys and DATABASE_URL")
        return 1
    from app.db import make_engine, make_session_factory
    from app.db.models import Run
    sessions = make_session_factory(make_engine(settings=s))
    epo = EpoOpsClient(*creds)
    today = datetime.now(timezone.utc).date()
    with sessions() as db:
        rows = db.query(Run).order_by(Run.generated_at.desc()).all()
        seen: set[str] = set()
        changed: list[str] = []
        for row in rows:
            t = row.topic.lower()
            if t in seen or row.score is None:
                continue
            seen.add(t)
            rep = ResearchReport.model_validate(row.report_json)
            if not rep.patent or rep.patent.ytd is not None or not rep.patent.terms:
                continue
            try:
                m = patent_ytd(epo, rep.patent.terms, today)
            except SourceError as exc:
                print(f"{rep.topic}: EPO error {exc.message[:120]}")
                continue
            if m is None:
                continue
            serp = any(src.source_name.startswith("Google Patents") for src in rep.patent.sources)
            if serp:
                m.basis += " (Year-to-date counts from EPO OPS; the yearly counts above are from Google Patents, so compare growth, not numbers.)"
            print(f"{rep.topic}: patents {m.count} by {m.cutoff} {m.year} vs {m.previous_count} ({m.growth_pct}%, {m.trend})")
            if args.apply:
                rep.patent.ytd = m
                row.report_json = rep.model_dump(mode="json")
                row.report_markdown = render_markdown(rep)
                changed.append(row.id)
        if args.apply:
            db.commit()
    print(f"{len(changed)} report(s) updated" if args.apply else "dry run: nothing saved (use --apply)")
    if args.apply and args.reseal:
        for rid in changed:
            subprocess.run([sys.executable, "scripts/near_record_report.py", "--run", rid, "--force"], cwd=Path(__file__).resolve().parents[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())

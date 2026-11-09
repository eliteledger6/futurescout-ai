"""Re-run only the scoring ARITHMETIC on saved reports after a change of method (no model, no data fetch).

  python scripts\\rescore_formula.py                    dry run: old vs new for the latest report of every topic
  python scripts\\rescore_formula.py --apply            save (database row, Markdown)
  python scripts\\rescore_formula.py --apply --reseal   ...and record the new fingerprints on NEAR testnet (paced)

Uses the ratings, risk rating and findings already stored in each report (method v2, 2026-11-09: the opportunity
score is no longer cut by risk; confidence % = evidence confidence x risk multiplier). Older runs of a topic are left
as they were, so their seals stay valid.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import get_settings  # noqa: E402
from app.report import render_markdown  # noqa: E402
from app.report.verdict import build_verdict  # noqa: E402
from app.schemas.research import ResearchReport  # noqa: E402
from app.scoring import load_scoring_config, report_findings, rescore_existing, verified_share_of  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reseal", action="store_true")
    args = ap.parse_args()
    s = get_settings()
    if not s.database_url_value():
        print("needs DATABASE_URL")
        return 1
    from app.db import make_engine, make_session_factory
    from app.db.models import Run
    cfg = load_scoring_config()
    sessions = make_session_factory(make_engine(settings=s))
    changed: list[str] = []
    print(f"{'topic':32} {'old':>5} -> {'score':>5}  {'conf %':>6} = evid x risk   band")
    with sessions() as db:
        seen: set[str] = set()
        for row in db.query(Run).order_by(Run.generated_at.desc()).all():
            t = row.topic.lower()
            if t in seen or row.score is None:
                continue
            seen.add(t)
            rep = ResearchReport.model_validate(row.report_json)
            if not rep.investment or not rep.investment.score:
                continue
            old = rep.investment.score
            new = rescore_existing(old, cfg, verified_share_of(report_findings(rep)))
            rep.investment.score = new
            band = build_verdict(rep).get("band")
            print(f"{rep.topic[:32]:32} {old.score!s:>5} -> {new.score!s:>5}  {new.confidence_pct!s:>6} = {new.evidence_confidence_pct} x {new.risk_multiplier}   {band}"
                  + ("" if old.scoring_version != new.scoring_version else "   (already v2)"))
            if args.apply and old.scoring_version != new.scoring_version:
                row.report_json = rep.model_dump(mode="json")
                row.report_markdown = render_markdown(rep)
                row.score, row.score_reportable, row.score_coverage = new.score, new.reportable, new.coverage
                changed.append(row.id)
        if args.apply:
            db.commit()
    print(f"\n{len(changed)} report(s) updated" if args.apply else "\ndry run: nothing saved (use --apply)")
    if args.apply and args.reseal:
        backend = Path(__file__).resolve().parents[1]
        for rid in changed:
            for attempt in range(5):
                r = subprocess.run([sys.executable, "scripts/near_record_report.py", "--run", rid, "--force"], cwd=backend, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace")
                if "Recorded on NEAR testnet" in (r.stdout or ""):
                    print(f"  sealed {rid}")
                    break
                time.sleep(20)
            else:
                print(f"  NOT sealed {rid} (testnet busy; run scripts\\near_record_report.py --run {rid} --force later)")
            time.sleep(6)
    return 0


if __name__ == "__main__":
    sys.exit(main())

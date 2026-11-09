"""Copy a few saved reports (and the radar) into backend/samples/ so a fresh clone has something to show.

  python scripts\\export_samples.py --run <id> [--run <id> ...]     export these runs from the database / runs folder
  python scripts\\export_samples.py --latest 3                       export the newest N runs

The API falls back to backend/samples/ when there is no database and backend/runs/ holds no reports
(see app/api/main.py _default_store). Samples are real past runs: their NEAR records still verify.
Short quoted excerpts from papers and filings are part of the reports; keep the set small.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.report import render_markdown  # noqa: E402

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="append", default=[])
    ap.add_argument("--latest", type=int, default=0)
    args = ap.parse_args()
    store = _default_store(get_settings())
    ids = list(args.run)
    if args.latest:
        ids += [r["id"] for r in store.list(limit=args.latest)]
    if not ids:
        print("nothing to export: pass --run <id> or --latest N")
        return 1
    SAMPLES.mkdir(exist_ok=True)
    for rid in dict.fromkeys(ids):
        found = store.get(rid)
        if not found:
            print(f"  {rid}: not found")
            continue
        report, md = found
        name = rid if rid.startswith("report_") else f"report_{rid}"
        (SAMPLES / f"{name}.json").write_text(report.model_dump_json(indent=2), encoding="utf-8")
        (SAMPLES / f"{name}.md").write_text(md or render_markdown(report), encoding="utf-8")
        print(f"  {name}: {report.topic} ({'sealed' if report.chain_record else 'not sealed'})")
    radar = service.RUNS_DIR / "radar.json"
    if radar.is_file():
        shutil.copy(radar, SAMPLES / "radar.json")
        print("  radar.json copied")
    print(f"samples in {SAMPLES}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

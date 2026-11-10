"""Copy everything the website shows into backend/site_data/, for the hosted copy (Render) that has no database.

  python scripts\\export_site.py            # all saved reports + radar + funds + trading record + portfolio

Then commit and push: Render redeploys by itself and the public site shows the new snapshot.
The hosted API reads this folder because Render sets FUTURESCOUT_DATA_DIR=site_data (see render.yaml).
Nothing secret is in here: reports, fund decisions and the trading record are what the site shows anyway.
Reports keep their database id in the file name (report_<id>.json), so links between pages keep working.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.report import render_markdown  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "site_data"


def main() -> int:
    src = service.RUNS_DIR
    if OUT.resolve() == src.resolve():
        print("FUTURESCOUT_DATA_DIR points at site_data: unset it before exporting")
        return 1
    store = _default_store(get_settings())
    rows = store.list(limit=10_000)
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("report_*"):
        old.unlink()                                   # a fresh snapshot each time
    n = 0
    for row in rows:
        found = store.get(row["id"])
        if not found:
            continue
        report, md = found
        name = row["id"] if row["id"].startswith("report_") else f"report_{row['id']}"
        (OUT / f"{name}.json").write_text(report.model_dump_json(), encoding="utf-8")
        (OUT / f"{name}.md").write_text(md or render_markdown(report), encoding="utf-8")
        n += 1
    print(f"  {n} reports (from the {store.kind})")
    for rel in ("radar.json", "portfolio.json", "trading/state.json", "economy/state.json", "economy/sales.json"):
        f = src / rel
        if f.is_file():
            (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(f, OUT / rel)
            print(f"  {rel}")
    if (src / "funds").is_dir():
        shutil.rmtree(OUT / "funds", ignore_errors=True)
        shutil.copytree(src / "funds", OUT / "funds")
        print(f"  funds/ ({len(list((OUT / 'funds').glob('*.json')))} topic funds)")
    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()) / 1e6
    print(f"snapshot in {OUT} ({size:.1f} MB). Next: git add backend/site_data, commit, push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

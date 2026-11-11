"""Copy everything the website shows into backend/site_data/, for the hosted copy (Render) that has no database.

  python scripts\\export_site.py            # all saved reports + radar + funds + trading record + portfolio
  python scripts\\export_site.py --prune    # also remove snapshot reports this machine does not have (after deleting one)

The agents may publish from two machines (the report agent on a server, the trading agent on a laptop). So the export
adds to the snapshot and never takes away: a report only the other machine has stays, and a shared file (radar,
trading record, economy, proposals, a paper fund) is replaced only when this machine's copy is not older than the
snapshot's.

Then commit and push: Render redeploys by itself and the public site shows the new snapshot.
The hosted API reads this folder because Render sets FUTURESCOUT_DATA_DIR=site_data (see render.yaml).
Nothing secret is in here: reports, fund decisions and the trading record are what the site shows anyway.
Reports keep their database id in the file name (report_<id>.json), so links between pages keep working.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.report import render_markdown  # noqa: E402
from app.site_publish import copy_unless_older  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "site_data"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prune", action="store_true", help="remove snapshot reports that this machine does not have")
    args = ap.parse_args()
    src = service.RUNS_DIR
    if OUT.resolve() == src.resolve():
        print("FUTURESCOUT_DATA_DIR points at site_data: unset it before exporting")
        return 1
    store = _default_store(get_settings())
    rows = store.list(limit=10_000)
    OUT.mkdir(exist_ok=True)
    before = {p.name for p in OUT.glob("report_*")}
    written: set[str] = set()
    n = 0
    for row in rows:
        found = store.get(row["id"])
        if not found:
            continue
        report, md = found
        name = row["id"] if row["id"].startswith("report_") else f"report_{row['id']}"
        (OUT / f"{name}.json").write_text(report.model_dump_json(), encoding="utf-8")
        (OUT / f"{name}.md").write_text(md or render_markdown(report), encoding="utf-8")
        written.update({f"{name}.json", f"{name}.md"})
        n += 1
    others = sorted(before - written)                  # reports only the other machine (or an earlier export) has
    if args.prune:
        for name in others:
            (OUT / name).unlink()
    print(f"  {n} reports (from the {store.kind})" + ((f"; {len(others) // 2} more in the snapshot "
          + ("removed (--prune)" if args.prune else "kept (not on this machine)")) if others else ""))
    # economy/sales.json is NOT exported: it holds buyers' access tokens, and the snapshot is published (git, hosted copy).
    stale = OUT / "economy" / "sales.json"
    if stale.is_file():
        stale.unlink()
    for rel in ("radar.json", "portfolio.json", "trading/state.json", "economy/state.json", "proposals/state.json"):
        f = src / rel
        if f.is_file():
            print(f"  {rel}" if copy_unless_older(f, OUT / rel) else f"  {rel}: kept the snapshot's copy (it is newer than this machine's)")
    if (src / "funds").is_dir():
        kept = sum(not copy_unless_older(f, OUT / "funds" / f.name) for f in sorted((src / "funds").glob("*.json")))
        print(f"  funds/ ({len(list((OUT / 'funds').glob('*.json')))} topic funds" + (f"; {kept} newer in the snapshot, kept" if kept else "") + ")")
    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()) / 1e6
    print(f"snapshot in {OUT} ({size:.1f} MB). Next: git add backend/site_data, commit, push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

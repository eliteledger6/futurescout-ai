"""The hosted copy (Render) serves an exported snapshot through FileStore: database ids must survive and lists are newest first."""
import json
import shutil
from pathlib import Path

from app.api.store import FileStore

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_filestore_keeps_database_ids_and_sorts_by_date(tmp_path):
    files = sorted(SAMPLES.glob("report_*-*.json"))[:2]
    assert len(files) == 2
    dates = []
    for i, f in enumerate(files):
        data = json.loads(f.read_text(encoding="utf-8"))
        data["generated_at"] = f"2026-11-0{i + 1}T00:00:00Z"        # second file is the newest
        (tmp_path / f.name).write_text(json.dumps(data), encoding="utf-8")
        dates.append(data["generated_at"])
    shutil.copy(SAMPLES / "radar.json", tmp_path / "report_broken.json")  # not a report: skipped, not fatal
    store = FileStore(tmp_path)
    rows = store.list()
    ids = [f.stem[len("report_"):] for f in files]
    assert [r["id"] for r in rows] == [ids[1], ids[0]]                    # bare database ids, newest first
    assert store.get(ids[0]) is not None and store.get(f"report_{ids[0]}") is not None
    assert store.get("../secrets") is None and store.get("nonsense") is None
    assert store.list(limit=1)[0]["id"] == ids[1]



def test_a_copy_without_runs_serves_the_snapshot_radar_before_the_sample(tmp_path, monkeypatch):
    import json
    from app import radar as rd
    real = json.loads((rd.BACKEND_DIR / "samples" / "radar.json").read_text(encoding="utf-8"))
    snap, sample = dict(real, generated_at="2026-11-09T06:53:54Z"), dict(real, generated_at="2026-11-09T05:43:19Z")
    (tmp_path / "snap.json").write_text(json.dumps(snap), encoding="utf-8")
    (tmp_path / "sample.json").write_text(json.dumps(sample), encoding="utf-8")
    monkeypatch.setattr(rd, "RADAR_FILE", tmp_path / "runs_radar.json")           # no runs/ on this copy
    monkeypatch.setattr(rd, "SNAPSHOT_RADAR_FILE", tmp_path / "snap.json")
    monkeypatch.setattr(rd, "SAMPLE_RADAR_FILE", tmp_path / "sample.json")
    assert rd.load_radar(rd.RADAR_FILE).generated_at.isoformat().startswith("2026-11-09T06:53")   # the snapshot wins
    (tmp_path / "snap.json").unlink()
    assert rd.load_radar(rd.RADAR_FILE).generated_at.isoformat().startswith("2026-11-09T05:43")   # then the sample

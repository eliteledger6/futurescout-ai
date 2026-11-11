"""The report agent recounts the Hot-Topic Radar in the background and builds on the newest published radar."""
from app.radar_refresh import RadarRefresh, adopt_newer_snapshot


class FakeProc:
    def __init__(self, codes):
        self.codes = list(codes)

    def poll(self):
        return self.codes.pop(0) if len(self.codes) > 1 else self.codes[0]


def make(tmp_path, codes, calls):
    runs, snap = tmp_path / "runs", tmp_path / "site_data"
    runs.mkdir(); snap.mkdir()

    def popen(cmd, **kw):
        calls.append(cmd)
        assert kw["env"]["SERPAPI_CACHE_ONLY"] == "true"      # an automatic run never buys patent searches
        return FakeProc(codes)

    return RadarRefresh(runs, snap, log=lambda m: None, popen=popen, run=lambda *a, **k: None), runs, snap


def test_refresh_runs_in_the_background_and_reports_once_when_done(tmp_path):
    calls = []
    r, runs, _ = make(tmp_path, [None, 0], calls)
    assert r.finished() is None and not r.running            # nothing started yet
    assert r.start() is True and r.running
    assert r.start() is False                                 # one run at a time
    assert calls[0][-1] == "scripts/run_radar.py" and len(calls) == 1
    assert r.finished() is None                               # still counting: the loop keeps serving jobs
    assert r.finished() is True and not r.running             # done: publish
    assert r.finished() is None                               # reported once
    assert (runs / "radar_refresh.log").is_file()


def test_a_failed_refresh_is_not_published(tmp_path):
    r, _, _ = make(tmp_path, [3], [])
    r.start()
    assert r.finished() is False and not r.running


def test_refresh_builds_on_the_newest_published_radar(tmp_path):
    runs, snap = tmp_path / "runs", tmp_path / "site_data"
    runs.mkdir(); snap.mkdir()
    (runs / "radar.json").write_text('{"generated_at": "2026-11-09T06:53:54Z", "who": "mine"}', encoding="utf-8")
    (snap / "radar.json").write_text('{"generated_at": "2026-11-11T11:47:15Z", "who": "published"}', encoding="utf-8")
    assert adopt_newer_snapshot(runs, snap, log=lambda m: None) is True
    assert "published" in (runs / "radar.json").read_text(encoding="utf-8")
    (runs / "radar.json").write_text('{"generated_at": "2026-11-11T12:00:00Z", "who": "mine"}', encoding="utf-8")
    assert adopt_newer_snapshot(runs, snap, log=lambda m: None) is False      # this machine's is newer: kept
    assert "mine" in (runs / "radar.json").read_text(encoding="utf-8")

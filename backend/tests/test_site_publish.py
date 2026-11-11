"""Publishing the site snapshot: one publish at a time, nothing pushed when nothing changed, and the trading loop only
publishes when a visitor would see something new. git and the export are faked."""
import json
from types import SimpleNamespace

from app import site_publish as sp


def fake_run(calls, fail_at=None, out=""):
    def run(cmd, **kw):
        calls.append(cmd[:2] if cmd[0] == "git" else ["export"])
        bad = fail_at is not None and (cmd[:2] == fail_at)
        return SimpleNamespace(returncode=1 if bad else 0, stdout=out if bad else "", stderr="")
    return run


def test_publish_pulls_exports_commits_pushes_and_releases_the_lock(tmp_path, monkeypatch):
    monkeypatch.setattr(sp, "LOCK", tmp_path / ".publish.lock")
    calls = []
    assert sp.publish("msg", log=lambda _: None, run=fake_run(calls)) is True
    assert calls == [["git", "pull"], ["export"], ["git", "add"], ["git", "commit"], ["git", "push"]]
    assert not sp.LOCK.exists()
    calls.clear()
    assert sp.publish("msg", log=lambda _: None, run=fake_run(calls, ["git", "commit"], "nothing to commit, working tree clean")) is False
    assert ["git", "push"] not in calls and not sp.LOCK.exists()                # nothing changed: nothing pushed


def test_only_one_publish_at_a_time_and_a_dead_one_is_taken_over(tmp_path, monkeypatch):
    import os
    import time
    monkeypatch.setattr(sp, "LOCK", tmp_path / ".publish.lock")
    sp.LOCK.write_text("123")
    calls = []
    assert sp.publish("msg", log=lambda _: None, wait_seconds=0, run=fake_run(calls)) is False and calls == []
    old = time.time() - sp.STALE_SECONDS - 5
    os.utime(sp.LOCK, (old, old))                                                # the other publish died long ago
    assert sp.publish("msg", log=lambda _: None, wait_seconds=0, run=fake_run(calls)) is True


def test_trading_page_fingerprint_ignores_routine_checks(tmp_path):
    (tmp_path / "trading").mkdir()
    (tmp_path / "economy").mkdir()
    t = {"proposals": [{"id": "a", "status": "proposed"}], "checks": [1]}
    e = {"purchases": [], "stakes": [{"id": "s0", "status": "failed"}]}

    def fp():
        (tmp_path / "trading" / "state.json").write_text(json.dumps(t))
        (tmp_path / "economy" / "state.json").write_text(json.dumps(e))
        return sp.trade_fingerprint(tmp_path)
    base = fp()
    t["checks"].append(2)
    t["proposals"].append({"id": "b", "status": "blocked"})
    e["stakes"].append({"id": "s1", "status": "failed"})
    assert fp() == base                                                           # checks, waiting or refused things: no publish
    t["proposals"][0]["status"] = "success"
    after_trade = fp()
    assert after_trade != base
    e["purchases"].append({"id": "p1", "status": "paid"})
    after_buy = fp()
    assert after_buy != after_trade
    e["stakes"].append({"id": "s2", "status": "staked"})
    assert fp() != after_buy


def test_a_changed_near_com_balance_is_published(tmp_path):
    (tmp_path / "trading").mkdir()
    f = tmp_path / "trading" / "state.json"
    f.write_text(json.dumps({"proposals": [], "private_near": 3.4579}))
    before = sp.trade_fingerprint(tmp_path)
    f.write_text(json.dumps({"proposals": [], "private_near": 3.4581}))
    assert sp.trade_fingerprint(tmp_path) == before                               # rounding noise: no publish
    f.write_text(json.dumps({"proposals": [], "private_near": 1.72}))
    assert sp.trade_fingerprint(tmp_path) != before                               # money moved: publish


def test_an_older_copy_never_replaces_a_newer_one_in_the_snapshot(tmp_path):
    """Two machines publish (report agent on a server, trading agent on a laptop): each has a stale copy of the other's files."""
    from app.site_publish import copy_unless_older, newest_stamp
    mine, snap = tmp_path / "runs" / "radar.json", tmp_path / "site_data" / "radar.json"
    mine.parent.mkdir(); snap.parent.mkdir()
    mine.write_text('{"generated_at": "2026-11-09T06:53:54.555Z", "topics": []}', encoding="utf-8")
    snap.write_text('{"generated_at": "2026-11-11T11:47:15.813Z", "topics": [1]}', encoding="utf-8")
    assert newest_stamp(mine) == "2026-11-09T06:53:54" and newest_stamp(tmp_path / "missing.json") == ""
    assert copy_unless_older(mine, snap) is False and '"topics": [1]' in snap.read_text(encoding="utf-8")   # snapshot kept
    mine.write_text('{"generated_at": "2026-11-11T12:00:00Z", "topics": [2]}', encoding="utf-8")
    assert copy_unless_older(mine, snap) is True and '"topics": [2]' in snap.read_text(encoding="utf-8")    # newer: copied
    mine.write_text('{"generated_at": "2026-11-11T12:00:00Z", "topics": []}', encoding="utf-8")             # same time, same number of entries: this machine's copy
    assert copy_unless_older(mine, snap) is True and '"topics": []' in snap.read_text(encoding="utf-8")
    # a deadline in the future is in both copies (an order valid until 2099): it must not make them look equally new
    snap.write_text('{"checks": ["2026-11-11T13:56:48Z"], "deadline": "2099-01-01T00:00:00Z", "who": "server"}', encoding="utf-8")
    mine.write_text('{"checks": ["2026-11-11T12:39:37Z"], "deadline": "2099-01-01T00:00:00Z", "who": "laptop"}', encoding="utf-8")
    assert newest_stamp(mine) == "2026-11-11T12:39:37"
    assert copy_unless_older(mine, snap) is False and "server" in snap.read_text(encoding="utf-8")
    # equally recent: the copy with more dated entries (more history) is kept
    mine.write_text('{"checks": ["2026-11-11T12:39:37Z"], "who": "laptop"}', encoding="utf-8")
    snap.write_text('{"checks": ["2026-11-11T10:00:00Z", "2026-11-11T12:39:37Z"], "who": "server"}', encoding="utf-8")
    assert copy_unless_older(mine, snap) is False and "server" in snap.read_text(encoding="utf-8")
    assert copy_unless_older(mine, snap, force=True) is True and "laptop" in snap.read_text(encoding="utf-8")   # on purpose
    assert copy_unless_older(mine, tmp_path / "site_data" / "funds" / "new.json") is True                   # nothing there yet: copied

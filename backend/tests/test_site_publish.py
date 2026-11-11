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

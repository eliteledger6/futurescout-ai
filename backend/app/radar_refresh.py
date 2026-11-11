"""Automatic refresh of the Hot-Topic Radar from the report agent's loop (owner 2026-11-11).

A full radar run counts papers, patents and SEC filers for every topic. At the European Patent Office's fair-use pace
that takes over an hour, so it runs as a separate process next to the loop: jobs and topic proposals are still served
while it counts. When it has finished, the loop publishes the new radar with the rest of the website data.

No model is involved and nothing is signed or paid: the radar is counts from OpenAlex, the patent source and SEC EDGAR.
The run is started with SERPAPI_CACHE_ONLY=true, so it never buys a Google Patents search; topics without a saved
result are counted by the free EPO database when its keys are set, and otherwise keep their earlier patent numbers.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional

from app.site_publish import newest_stamp

BACKEND = Path(__file__).resolve().parents[1]


def adopt_newer_snapshot(runs_dir: Path, snapshot_dir: Path, log: Callable[[str], None] = print) -> bool:
    """Start from the newest radar there is. Another machine may have published a later radar than this machine's own
    copy; a refresh keeps earlier patent numbers for topics it cannot count, so it must build on the latest one."""
    mine, snap = runs_dir / "radar.json", snapshot_dir / "radar.json"
    if snap.is_file() and newest_stamp(snap) > newest_stamp(mine):
        mine.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(snap, mine)
        log("  radar: starting from the published radar (it is newer than this machine's copy)")
        return True
    return False


class RadarRefresh:
    """Runs `scripts/run_radar.py` in the background, one run at a time."""

    def __init__(self, runs_dir: Path, snapshot_dir: Path, log: Callable[[str], None] = print,
                 popen: Callable[..., subprocess.Popen] = subprocess.Popen,
                 run: Callable[..., subprocess.CompletedProcess] = subprocess.run) -> None:
        self.runs_dir, self.snapshot_dir, self.log = runs_dir, snapshot_dir, log
        self._popen, self._run = popen, run
        self._proc: Optional[subprocess.Popen] = None
        self._out = None

    @property
    def running(self) -> bool:
        return self._proc is not None

    def start(self) -> bool:
        """Begin a refresh. False when one is already running or it could not be started."""
        if self._proc is not None:
            return False
        try:   # the latest published radar first (the publisher pulls anyway; a failure here only means an older base)
            self._run(["git", "pull", "-q", "--rebase", "--autostash"], cwd=str(BACKEND.parent), capture_output=True, text=True, timeout=120)
        except Exception:  # noqa: BLE001
            pass
        adopt_newer_snapshot(self.runs_dir, self.snapshot_dir, self.log)
        try:
            self.runs_dir.mkdir(parents=True, exist_ok=True)
            self._out = open(self.runs_dir / "radar_refresh.log", "w", encoding="utf-8")
            # an automatic run never spends paid patent searches: saved Google Patents results or the free EPO database only
            env = {**os.environ, "SERPAPI_CACHE_ONLY": "true"}
            self._proc = self._popen([sys.executable, "scripts/run_radar.py"], cwd=str(BACKEND), stdout=self._out,
                                     stderr=subprocess.STDOUT, env=env)
        except Exception as exc:  # noqa: BLE001
            self.log(f"  radar refresh could not start: {str(exc)[:120]}")
            self._close()
            return False
        self.log("  radar refresh started in the background (papers, patents, SEC filers for every topic; can take over an hour)")
        return True

    def finished(self) -> Optional[bool]:
        """None while it runs or when nothing was started; True when a run just ended well (publish it); False when it failed."""
        if self._proc is None:
            return None
        code = self._proc.poll()
        if code is None:
            return None
        self._close()
        self.log("  radar refresh finished" if code == 0 else f"  radar refresh failed (exit {code}); see runs/radar_refresh.log. The old radar stays.")
        return code == 0

    def _close(self) -> None:
        self._proc = None
        if self._out:
            try:
                self._out.close()
            except OSError:
                pass
            self._out = None

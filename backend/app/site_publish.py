"""Publish the read-only snapshot to the hosted website: export backend/site_data, commit it and push (the hosts
redeploy from git). Used by the report-agent loop and the trading loop when the owner starts them with --publish.

Two loops may run on the same machine, so one lock file makes sure only one publishes at a time. Every push makes the
hosts rebuild, so the trading loop publishes only when something a visitor would see has changed (a trade, a report
purchase, a stake), never for a routine check.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable

REPO = Path(__file__).resolve().parents[2]
LOCK = REPO / ".publish.lock"
STALE_SECONDS = 15 * 60


def _acquire(wait_seconds: float, sleep: Callable[[float], None] = time.sleep) -> bool:
    deadline = time.time() + wait_seconds
    while True:
        try:
            fd = os.open(str(LOCK), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return True
        except FileExistsError:
            try:
                if time.time() - LOCK.stat().st_mtime > STALE_SECONDS:      # a publish that died: take over
                    LOCK.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.time() >= deadline:
                return False
            sleep(5)


def publish(message: str = "Site data update", log: Callable[[str], None] = print, wait_seconds: float = 300,
            run: Callable[..., subprocess.CompletedProcess] = subprocess.run) -> bool:
    """Export, commit backend/site_data and push. Returns True when something was pushed."""
    if not _acquire(wait_seconds):
        log("  publish skipped: another publish is still running")
        return False
    try:
        steps = [(["git", "pull", "-q", "--rebase", "--autostash"], REPO),      # the owner or the other loop may have pushed
                 ([sys.executable, "scripts/export_site.py"], REPO / "backend"),
                 (["git", "add", "backend/site_data"], REPO),
                 (["git", "commit", "-q", "-m", message], REPO),
                 (["git", "push", "-q"], REPO)]
        for cmd, cwd in steps:
            r = run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
            if r.returncode != 0:
                if cmd[:2] == ["git", "commit"] and "nothing to commit" in ((r.stdout or "") + (r.stderr or "")):
                    log("  publish: nothing new to publish")
                    return False
                log(f"  publish stopped at '{' '.join(cmd[:2])}': {((r.stderr or r.stdout) or '').strip()[-200:]}")
                return False
        log("  published: the hosted site redeploys in a few minutes")
        return True
    finally:
        try:
            LOCK.unlink()
        except FileNotFoundError:
            pass


def trade_fingerprint(runs_dir: Path) -> str:
    """Changes only when a visitor would see something new on the trading page: an order that was sent or finished
    (real or shadow), a report purchase, a stake. Routine checks and waiting proposals do not change it."""
    seen: list = []
    try:
        t = json.loads((runs_dir / "trading" / "state.json").read_text(encoding="utf-8"))
        seen.append(sorted((p.get("id"), p.get("status")) for p in t.get("proposals", [])
                           if p.get("status") not in ("proposed", "rejected", "blocked")))
        seen.append(round(float(t.get("private_near") or 0), 2))          # the near.com balance shown on the trading page
    except (OSError, ValueError):
        pass
    try:
        e = json.loads((runs_dir / "economy" / "state.json").read_text(encoding="utf-8"))
        seen.append(sorted((p.get("id"), p.get("status")) for p in e.get("purchases", [])))
        seen.append(sorted((x.get("id"), x.get("status")) for x in e.get("stakes", []) if x.get("status") == "staked"))
    except (OSError, ValueError):
        pass
    return hashlib.sha1(json.dumps(seen, sort_keys=True, default=str).encode()).hexdigest()

"""Every new report gets its paper fund (owner 2026-11-11: "the paper fund should always be created when there is a new
report").

Right after a research run, `scripts/funds.py --topic <topic>` builds or updates that topic's paper fund: pretend money in
the companies the report's patents and papers name, at real daily closes; tokenized versions get a NEAR Intents dry-run
quote. That fund is also what makes the topic tradable for the trading agent, which then sees a "new report" trigger.

It runs as a separate process so a fund problem can never break the research run, and it is called from the places that
produce reports in the owner's loops (the report agent and `scripts/run_research.py`). The fund decision is sealed on NEAR
like every decision (SEAL_NETWORK), so this only runs where the owner's keys are.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional

BACKEND = Path(__file__).resolve().parents[1]
MAX_PRICE_REQUESTS = 6          # fresh Alpha Vantage lookups per new fund (free plan: 25 a day); the rest comes from cache


def _run_funds(args: list[str], label: str, log: Callable[[str], None], run: Callable[..., subprocess.CompletedProcess],
               timeout: int) -> bool:
    cmd = [sys.executable, "scripts/funds.py", *args]
    try:
        r = run(cmd, cwd=str(BACKEND), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        log(f"  {label}: did not finish in {timeout // 60} min; it is tried again later")
        return False
    lines = [ln for ln in ((r.stdout or "") + (r.stderr or "")).splitlines()
             if ln.strip() and not any(x in ln for x in ("aiohttp", "Unclosed", "connector", "client_session", "Traceback"))]
    if r.returncode != 0:
        log(f"  {label}: failed ({(lines[-1] if lines else 'no output')[:160]})")
        return False
    log(f"  {label}: " + (lines[-1][:160] if lines else "done"))
    return True


def update_all_funds(log: Callable[[str], None] = print, run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
                     timeout: int = 1800) -> bool:
    """Every topic with a scored report: create a missing fund, decide again when a newer report exists or the weekly
    review is due, otherwise revalue at the latest closes. Run once a day by the report agent."""
    return _run_funds(["--max-price-requests", "10"], "paper funds (daily update)", log, run, timeout)


def funds_due(last_iso: Optional[str], now: datetime, every_hours: float = 24.0) -> bool:
    """True when the daily paper-fund update has not run in the last `every_hours` (or never)."""
    if not last_iso:
        return True
    try:
        last = datetime.fromisoformat(last_iso)
    except ValueError:
        return True
    last = last if last.tzinfo else last.replace(tzinfo=timezone.utc)
    return now - last >= timedelta(hours=every_hours)


def build_paper_fund(topic: str, log: Callable[[str], None] = print, run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
                     timeout: int = 900) -> bool:
    """Build or update the paper fund of `topic`. Returns True when funds.py finished without an error."""
    if not (topic or "").strip():
        return False
    return _run_funds(["--topic", topic.strip(), "--max-price-requests", str(MAX_PRICE_REQUESTS)], f"paper fund for '{topic}'",
                      log, run, timeout)

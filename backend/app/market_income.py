"""What the report agent earns on NEAR Agent Market, so it joins the same split as report sales: 70% staked with
NEAR AI, 30% kept (owner 2026-11-11).

The marketplace holds each hire's fee in escrow (in USD) and releases it when the buyer accepts the delivery. This
file keeps one line per accepted, paid hire: the fee in USD and what it was worth in NEAR at the live price when it was
recorded. Test hires carry a fee of 0 and are not income.

The fee stays in the agent's marketplace balance until the owner withdraws it. The staking step counts it as received,
but it can only stake NEAR that is really in the report agent's wallet: until the fee is withdrawn there, the 70% stays owed.

The report agent writes the file (it holds the marketplace token); it is published with the website data, so the
trading agent's staking step can read it on another machine. It holds assignment ids, amounts and dates only.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from pydantic import BaseModel, Field

FILE = "agent_market/income.json"


class Fee(BaseModel):
    assignment_id: str
    usd: float
    near: float                     # the fee in NEAR at the live price when it was recorded
    near_usd: float
    accepted_at: Optional[str] = None
    recorded_at: datetime


class Income(BaseModel):
    fees: list[Fee] = Field(default_factory=list)

    def usd(self) -> float:
        return round(sum(f.usd for f in self.fees), 2)

    def near(self) -> float:
        return round(sum(f.near for f in self.fees), 6)


def load(path: Path) -> Income:
    try:
        return Income.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return Income()


def best(*files: Path) -> Income:
    """The record with the most fees among this machine's copy and the published snapshot."""
    return max((load(f) for f in files), key=lambda i: len(i.fees), default=Income())


def collect(rows: list[dict], path: Path, near_usd: Callable[[], float], now: datetime,
            log: Callable[[str], None] = print) -> int:
    """Record every accepted hire that paid a fee and is not recorded yet. `rows` = all of the agent's assignments.
    Returns how many were added. The NEAR price is read only when there is something to add."""
    income = load(path)
    have = {f.assignment_id for f in income.fees}
    added = 0
    price: Optional[float] = None
    for row in rows:
        a = row.get("assignment") or {}
        aid = a.get("assignmentId")
        if not aid or aid in have or a.get("status") != "accepted":
            continue
        try:
            usd = float(a.get("escrowAmount") or 0)
        except (TypeError, ValueError):
            continue
        if usd <= 0 or str(a.get("escrowToken") or "USD").upper() not in ("USD", "USDC"):
            continue                                      # a free test hire, or a token this split does not price
        if price is None:
            price = float(near_usd())
        if price <= 0:
            return added
        income.fees.append(Fee(assignment_id=aid, usd=round(usd, 2), near=round(usd / price, 6), near_usd=round(price, 4),
                               accepted_at=a.get("finalizedAt"), recorded_at=now))
        have.add(aid)
        added += 1
        log(f"  Agent Market fee recorded: ${usd:.2f} for hire {aid[:8]} = {usd / price:.3f} NEAR at ${price:.2f}; "
            f"70% is staked once it is in the report agent's wallet")
    if added:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(income.model_dump_json(indent=1), encoding="utf-8")
    return added

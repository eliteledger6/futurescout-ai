"""Check the candidate X accounts in config/x_watchlist.yaml through the X API (read-only).

  python scripts\\x_lookup.py

Prints, for each candidate, whether it exists and its real display name, description, verification
type and follower count, so the owner can decide which accounts to approve. It changes nothing.
Cost: about $0.010 per account found (X pay-per-use user read), so ~19 candidates is about $0.19.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml  # noqa: E402

from app.config import CONFIG_DIR, get_settings  # noqa: E402
from app.sources.base import SourceError  # noqa: E402
from app.sources.x import XClient  # noqa: E402


def main() -> int:
    token = get_settings().x_token_value()
    if not token:
        print("X_BEARER_TOKEN is not set in .env")
        return 1
    data = yaml.safe_load((CONFIG_DIR / "x_watchlist.yaml").read_text(encoding="utf-8"))
    approved = {a["handle"].lower() for a in data.get("approved") or []}
    candidates = [c for c in (data.get("candidates") or []) if c["handle"].lower() not in approved]
    if not candidates:
        print("Every candidate is already approved; nothing to look up.")
        return 0
    print(f"Looking up {len(candidates)} candidate(s) not yet approved (about ${0.01 * len(candidates):.2f})...")
    client = XClient(token)
    try:
        found, missing = client.lookup_users([c["handle"] for c in candidates])
    except SourceError as exc:
        print(f"ERROR: {exc}")
        return 1
    by_handle = {u.username.lower(): u for u in found}
    print(f"{len(found)} of {len(candidates)} candidate accounts exist on X.\n")
    for c in candidates:
        u = by_handle.get(c["handle"].lower())
        if u is None:
            print(f"  NOT FOUND  @{c['handle']}  (expected: {c['expected']})")
            continue
        badge = u.verified_type or ("verified" if u.verified else "not verified")
        desc = " ".join(u.description.split())[:110]
        print(f"  @{u.username:16} id={u.id:20} {badge:12} followers={u.followers if u.followers is not None else '?':>10}")
        print(f"      name: {u.name}   (expected: {c['expected']})")
        print(f"      bio:  {desc}")
    if missing:
        print(f"\nX reported as unavailable: {', '.join(missing)}")
    print(f"\nX API usage: {client.usage.as_dict()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

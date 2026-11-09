"""Re-apply the current add rules to accounts the AGENT added (never the owner's), without any X request.

  python scripts\\x_recheck.py              move agent-added accounts that no longer qualify back to `suggested`
  python scripts\\x_recheck.py --dry-run    show what would move

Uses the facts stored when each account was added (verification, followers, role, on-topic posts, score), or,
for older rows that lack them, the facts written in the change log. Nothing is deleted: failing accounts go back to
`suggested` with the reason, so the owner can still approve them by hand.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.x import watchlist as wl  # noqa: E402
from app.sources.x import PROMO_WORDS  # noqa: E402

ADD_RE = re.compile(r"added @(?P<h>\w+) \(score (?P<score>[\d.]+), (?P<vt>\w+) verified, (?P<f>\d+|None) followers(?P<rest>.*)\)$")


def facts_from_log(data: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for c in data.get("changes", []):
        m = ADD_RE.match(str(c.get("change", "")))
        if not m:
            continue
        rest = m.group("rest")
        posts = re.search(r"(\d+) on-topic posts", rest)
        role = re.search(r", (CEO|CTO|COO|CFO|VP|Vice President|President|Co-?founder|Founder|Head of \w+|Fellow|Chief \w+ Officer)\b", rest, re.I)
        out[m.group("h").lower()] = {"verified_type": m.group("vt"), "followers": None if m.group("f") == "None" else int(m.group("f")),
                                     "score": float(m.group("score")), "posts_on_topic": int(posts.group(1)) if posts else 0,
                                     "role": role.group(1) if role else None}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    data = wl.load()
    logged = facts_from_log(data)
    keep, moved = [], []
    for a in list(data["approved"]):
        if a.get("approved_by") != "agent":
            continue
        facts = {k: a.get(k) for k in ("verified_type", "followers", "role", "posts_on_topic", "score")}
        if facts.get("verified_type") is None and a["handle"].lower() in logged:
            facts = logged[a["handle"].lower()]
        text = f"{a['handle']} {a.get('name', '')}".lower()
        flags = list(a.get("flags") or []) + (["trading-tip, promotional or parody wording in the profile"] if any(w in text for w in PROMO_WORDS) else [])
        row = {"handle": a["handle"], "id": a.get("id"), "name": a.get("name", ""), "flags": flags, **facts}
        ok, eff, why = wl.qualifies(data, row)
        if ok:
            keep.append(a["handle"])
            continue
        moved.append((a["handle"], why))
        if not args.dry_run:
            data["approved"].remove(a)
            data["suggested"].append({**row, "topics": a.get("topics", []), "evidence": [], "suggested_on": a.get("added_on"),
                                      "description": "", "rechecked": f"{date.today().isoformat()}: {why}"})
    print(f"agent-added accounts kept: {len(keep)}  -> {', '.join('@' + h for h in keep)}")
    print(f"moved back to suggested: {len(moved)}")
    for h, why in moved:
        print(f"  @{h}: {why}")
    if not args.dry_run and moved:
        data["changes"].append({"date": date.today().isoformat(),
                                "change": f"re-check under stricter rules: {len(moved)} agent-added account(s) moved back to suggested"})
        wl.save(data)
    print(f"watched accounts now: {len(data['approved'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

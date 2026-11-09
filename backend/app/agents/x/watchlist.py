"""The X watchlist file (config/x_watchlist.yaml) and the agent's power to change it.

Three lists live in the file:
  approved   : accounts that are searched. Each has `approved_by: owner` or `approved_by: agent`.
  suggested  : accounts the agent found posting about a topic (real posts, ranked), waiting for a decision.
  candidates : handles typed by a human, verified by scripts/x_lookup.py.

`auto_manage` (default false): when true the agent may ADD a suggestion that scores at least
`auto_add_min_score` and has no caution flags, and may REMOVE an account IT added that has posted
nothing on any topic for `auto_remove_after_days`. Accounts approved by the owner are never removed
by the agent. Every change is written to the file with a date and a reason, so it can be undone.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional

import yaml

from app.config import CONFIG_DIR
from app.sources.x import AccountSuggestion

WATCHLIST_PATH = CONFIG_DIR / "x_watchlist.yaml"
DEFAULTS = {"auto_manage": False, "auto_add_min_score": 8.0, "auto_remove_after_days": 90, "max_accounts": 60,
            "require_verified": True, "endorse_min_watchers": 2}
ENDORSE_POINTS = 2.0      # per distinct watched account that @mentioned the handle
ENDORSE_MAX = 6.0
ENDORSE_WINDOW_DAYS = 60  # mentions older than this stop counting


def load(path: Path = WATCHLIST_PATH) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for k, v in DEFAULTS.items():
        data.setdefault(k, v)
    data.setdefault("approved", [])
    data.setdefault("suggested", [])
    data.setdefault("changes", [])
    data.setdefault("endorsements", {})
    return data


def record_endorsements(data: dict[str, Any], mentions: dict[str, set[str]], today: Optional[date] = None) -> list[str]:
    """Remember which watched accounts @mentioned which handles. Returns handles now endorsed by enough watchers
    (`endorse_min_watchers`) that are neither watched nor suggested yet: worth a profile lookup."""
    today = today or datetime.now(timezone.utc).date()
    store: dict[str, dict] = data["endorsements"]
    for h, by in mentions.items():
        row = store.setdefault(h, {"by": [], "last": today.isoformat()})
        row["by"] = sorted({*row.get("by", []), *by})
        row["last"] = today.isoformat()
    cutoff = today - timedelta(days=ENDORSE_WINDOW_DAYS)
    for h in [h for h, r in store.items() if date.fromisoformat(str(r.get("last"))) < cutoff]:
        del store[h]
    known = {a["handle"].lower() for a in data["approved"]} | {s["handle"].lower() for s in data["suggested"]}
    need = int(data.get("endorse_min_watchers") or 2)
    return sorted((h for h, r in store.items() if h not in known and len(r.get("by", [])) >= need),
                  key=lambda h: -len(store[h]["by"]))


VERIFIED_TYPES = {"blue", "business", "government"}   # X sends verified_type "none" for unverified accounts


def qualifies(data: dict[str, Any], s: dict) -> tuple[bool, float, str]:
    """The agent's add rule (owner 2026-11-09): verified, no caution flags, score at least `auto_add_min_score`
    (endorsements by watched accounts included), and real substance: 2+ on-topic posts, a senior role, a mention by
    a watched account, or a business badge. One post plus a paid tick or a government badge is not enough."""
    vt = str(s.get("verified_type") or "").lower()
    if data.get("require_verified", True) and vt not in VERIFIED_TYPES:
        return False, 0.0, f"not verified ({vt or 'no badge'})"
    if s.get("flags"):
        return False, 0.0, "caution flags: " + "; ".join(s["flags"])
    bonus = endorsement_bonus(data, s["handle"])
    effective = float(s.get("score") or 0) + bonus
    if effective < float(data["auto_add_min_score"]):
        return False, effective, f"score {effective:.1f} below {data['auto_add_min_score']}"
    substance = int(s.get("posts_on_topic") or 0) >= 2 or bool(s.get("role")) or bonus > 0 or vt == "business"
    if not substance:
        return False, effective, "one post and a badge only (needs 2+ topic posts, a senior role, a mention by a watched account, or a business badge)"
    return True, effective, "ok"


def endorsement_bonus(data: dict[str, Any], handle: str) -> float:
    by = (data.get("endorsements") or {}).get(handle.lower(), {}).get("by", [])
    return min(ENDORSE_MAX, ENDORSE_POINTS * len(by))


def save(data: dict[str, Any], path: Path = WATCHLIST_PATH) -> None:
    header = (
        "# X watchlist for the X Intelligence agent (read-only; the agent never follows, likes or posts).\n"
        "# Only `approved` accounts are searched. `suggested` = found by the agent from real posts, awaiting\n"
        "# a decision. `auto_manage: true` lets the agent add high-scoring suggestions and remove accounts IT added\n"
        "# that stayed silent; accounts with approved_by: owner are never removed automatically.\n"
        "# Every change is logged under `changes`. Edit freely; the file is rewritten by the agent.\n\n"
    )
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)
    path.write_text(header + body, encoding="utf-8")


def record_suggestions(data: dict[str, Any], suggestions: list[AccountSuggestion], topic: str,
                       today: Optional[date] = None) -> list[dict]:
    """Merge new suggestions into `suggested` (keyed by handle, keeping the best score). Returns the new rows."""
    today = today or datetime.now(timezone.utc).date()
    approved = {a["handle"].lower() for a in data["approved"]}
    existing = {s["handle"].lower(): s for s in data["suggested"]}
    new_rows = []
    for s in suggestions:
        if s.handle.lower() in approved:
            continue
        row = {"handle": s.handle, "id": s.id, "name": s.name, "score": s.score, "posts_on_topic": s.posts_on_topic,
               "followers": s.followers, "verified_type": s.verified_type, "flags": list(s.flags),
               "topics": sorted({topic, *existing.get(s.handle.lower(), {}).get("topics", [])}),
               "evidence": s.sample_post_urls[:3], "suggested_on": today.isoformat(),
               "description": s.description[:160], "role": s.role}
        if s.handle.lower() in existing:
            if s.score > float(existing[s.handle.lower()].get("score") or 0):
                existing[s.handle.lower()].update(row)
        else:
            data["suggested"].append(row)
            new_rows.append(row)
    return new_rows


def note_activity(data: dict[str, Any], handles_seen: set[str], today: Optional[date] = None) -> None:
    """Remember when each approved account last posted on a topic (used for auto-removal)."""
    today = (today or datetime.now(timezone.utc).date()).isoformat()
    for a in data["approved"]:
        a.setdefault("approved_by", "owner")
        if a["handle"].lower() in handles_seen:
            a["last_on_topic"] = today
        a.setdefault("first_checked", today)


def auto_manage(data: dict[str, Any], today: Optional[date] = None) -> list[str]:
    """Apply the agent's add/remove rules if auto_manage is on. Returns plain-language change notes."""
    if not data.get("auto_manage"):
        return []
    today = today or datetime.now(timezone.utc).date()
    changes: list[str] = []
    approved = {a["handle"].lower() for a in data["approved"]}
    # add
    for s in list(data["suggested"]):
        if s["handle"].lower() in approved or len(data["approved"]) >= data["max_accounts"]:
            continue
        ok, effective, _why = qualifies(data, s)
        if not ok:
            continue
        data["approved"].append({"handle": s["handle"], "id": s["id"], "group": "agent", "name": s["name"],
                                 "approved_by": "agent", "added_on": today.isoformat(), "topics": s.get("topics", []),
                                 "first_checked": today.isoformat(),
                                 # kept so the rules can be re-applied later without another X lookup
                                 "verified_type": s.get("verified_type"), "followers": s.get("followers"), "role": s.get("role"),
                                 "posts_on_topic": s.get("posts_on_topic"), "score": s.get("score"), "flags": list(s.get("flags") or [])})
        data["suggested"].remove(s)
        approved.add(s["handle"].lower())
        endorsed = (data.get("endorsements") or {}).get(s["handle"].lower(), {}).get("by", [])
        changes.append(f"added @{s['handle']} (score {effective:.1f}, {s.get('verified_type')} verified, {s.get('followers')} followers"
                       + (f", {s['role']}" if s.get("role") else "") + (f", {s['posts_on_topic']} on-topic posts" if s.get("posts_on_topic") else "")
                       + (f", mentioned by @{', @'.join(endorsed[:3])}" if endorsed else "") + ")")
    # remove (agent-added only)
    cutoff = today - timedelta(days=int(data["auto_remove_after_days"]))
    for a in list(data["approved"]):
        if a.get("approved_by") != "agent":
            continue
        last = a.get("last_on_topic") or a.get("added_on") or a.get("first_checked")
        if last and date.fromisoformat(str(last)) < cutoff:
            data["approved"].remove(a)
            changes.append(f"removed @{a['handle']}: no on-topic post since {last}")
    for c in changes:
        data["changes"].append({"date": today.isoformat(), "change": c})
    return changes

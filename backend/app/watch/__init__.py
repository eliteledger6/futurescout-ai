"""Watch mode: the platform keeps working on its own.

Each cycle (scripts/watch.py, every WATCH_X_INTERVAL_MINUTES):
  1. SCAN: the X agent reads the newest posts from the owner-approved accounts (no topic filter).
  2. DETECT: code counts which radar topics the posts mention (terms from config/topics.yaml);
     the Chief model may additionally name up to 3 new technology topics it sees, each with the post
     ids as evidence (new topics join the radar; they are never invented without a post).
  3. RADAR: papers are recounted (free). Patent counts come from the cache; only a NEW topic gets a live
     patent count, at most WATCH_NEW_PATENT_TOPICS_PER_WEEK per week (SerpApi quota).
  4. TRIGGER: a topic gets a full research run when (heat >= threshold OR mentions this scan >= threshold)
     AND it has no report younger than WATCH_REPORT_MAX_AGE_DAYS AND the daily run cap is not reached.
  5. PUBLISH: the run is saved, sealed on NEAR testnet (if configured) and listed on the market.
Every decision (scan, detect, skip, trigger, run) is appended to runs/watch_state.json with its reason.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from pydantic import BaseModel, Field

from app.config import BACKEND_DIR, Settings
from app.models.router import ModelRouter, ModelRouterError
from app.radar import DEFAULT_SECTOR, load_sectors, Radar, TopicConfig, compute_radar, load_radar, load_topics, save_radar
from app.schemas.common import SourceRecord
from app.sources.base import SourceError

log = logging.getLogger("futurescout.watch")
STATE_PATH = BACKEND_DIR / "runs" / "watch_state.json"
MAX_EVENTS = 400
MAX_NEW_TOPICS_PER_SCAN = 3


class TopicScout(BaseModel):
    """Model output: new technology topics named in the scanned posts."""
    class Candidate(BaseModel):
        topic: str = Field(min_length=3, max_length=60)
        terms: list[str] = Field(default_factory=list, max_length=4)
        post_ids: list[str] = Field(min_length=1)
        why: str = ""
        sector: str = ""                 # key from config/sectors.yaml, chosen from the list given in the prompt
    candidates: list[Candidate] = Field(default_factory=list, max_length=MAX_NEW_TOPICS_PER_SCAN)


@dataclass
class Scan:
    at: datetime
    posts: int
    newest_id: Optional[str]
    mentions: dict[str, int]          # radar topic -> posts mentioning it
    new_topics: list[dict]            # model-proposed, with evidence
    x_cost_usd: float


class WatchState(BaseModel):
    last_scan_at: Optional[datetime] = None
    last_post_id: Optional[str] = None
    last_patent_refresh: dict[str, str] = Field(default_factory=dict)   # topic -> date of last live patent count
    runs_started: list[dict] = Field(default_factory=list)              # {at, topic, run_id}
    events: list[dict] = Field(default_factory=list)
    mention_history: list[dict] = Field(default_factory=list)          # {at, mentions}
    last_paper_discovery_at: Optional[datetime] = None                 # paper scout (keywords of recent papers) last run

    def log(self, kind: str, detail: str, now: datetime, **extra: Any) -> None:
        self.events.append({"at": now.isoformat(), "kind": kind, "detail": detail, **extra})
        self.events = self.events[-MAX_EVENTS:]

    def runs_today(self, now: datetime) -> int:
        day = now.date().isoformat()
        return sum(1 for r in self.runs_started if r["at"][:10] == day)

    def new_patent_topics_this_week(self, now: datetime) -> int:
        cutoff = (now - timedelta(days=7)).date().isoformat()
        return sum(1 for d in self.last_patent_refresh.values() if d >= cutoff)


def load_state(path: Path = STATE_PATH) -> WatchState:
    return WatchState.model_validate_json(path.read_text(encoding="utf-8")) if path.is_file() else WatchState()


def save_state(state: WatchState, path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(state.model_dump_json(indent=2), encoding="utf-8")


def count_mentions(posts: list[SourceRecord], topics: list[TopicConfig]) -> dict[str, int]:
    """Posts that contain any of a topic's terms (case-insensitive, hyphen = space)."""
    out: dict[str, int] = {}
    texts = [re.sub(r"[-‐‑–]", " ", (p.abstract or p.title).lower()) for p in posts]
    for t in topics:
        terms = [re.sub(r"[-‐‑–]", " ", x.lower()) for x in [t.name, *t.terms]]
        n = sum(1 for text in texts if any(re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) for term in terms))
        if n:
            out[t.name] = n
    return out


_SCOUT_PROMPT = (
    "You read posts by technology companies, industry bodies and specialist press. List up to 3 specific TECHNOLOGY "
    "topics that these posts discuss and that are NOT in the known-topics list. Each must be a technology or technique "
    "(e.g. a packaging method, battery chemistry, model architecture, qubit type), not a company, product name, event or "
    "stock. Cite the post ids that mention it. Give 1-3 short search terms (the phrase and a common abbreviation) and the "
    "sector key that fits best from the sector list given. Return {\"candidates\": []} if nothing qualifies. Never invent a "
    "topic that the posts do not mention."
)


def scout_new_topics(router: Optional[ModelRouter], posts: list[SourceRecord], known: list[TopicConfig],
                     sectors: Optional[list[str]] = None) -> list[dict]:
    if router is None or not posts:
        return []
    ids = {p.id for p in posts}
    sector_keys = sectors or [DEFAULT_SECTOR]
    body = "\n\n".join(f"id: {p.id}\nauthor: {p.authors[0] if p.authors else ''}\ntext: {(p.abstract or '')[:400]}" for p in posts)
    messages = [{"role": "system", "content": _SCOUT_PROMPT},
                {"role": "user", "content": f"Known topics: {', '.join(t.name for t in known)}\nSector keys: {', '.join(sector_keys)}"
                                            f"\n\nPosts ({len(posts)}):\n\n{body}"}]
    try:
        reply = router.complete("chief", messages, response_model=TopicScout)
    except ModelRouterError as exc:
        log.warning("topic scout failed: %s", exc)
        return []
    out = []
    for c in reply.parsed.candidates:  # type: ignore[union-attr]
        evidence = [i for i in c.post_ids if i in ids]
        if not evidence:
            continue  # claimed without a real post: dropped
        name = " ".join(c.topic.lower().split())
        if any(name == k.name.lower() for k in known):
            continue
        sector = c.sector if c.sector in sector_keys else sector_keys[0]
        out.append({"topic": name, "terms": [name, *[t for t in c.terms if t and t.lower() != name]][:4], "evidence": evidence,
                    "why": c.why[:200], "sector": sector})
    return out[:MAX_NEW_TOPICS_PER_SCAN]


def topics_path() -> Path:
    from app.config import CONFIG_DIR
    return CONFIG_DIR / "topics.yaml"


def add_topics(new: list[dict], path: Optional[Path] = None, found_by: str = "x watch") -> list[str]:
    """Append found topics (with evidence) to config/topics.yaml. Returns the names added."""
    import yaml
    path = path or topics_path()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    existing = {t["name"].lower() for t in data.get("topics", [])}
    added = []
    for n in new:
        if n["topic"].lower() in existing:
            continue
        data.setdefault("topics", []).append({"name": n["topic"], "sector": n.get("sector") or DEFAULT_SECTOR, "terms": n["terms"],
                                              "found_by": n.get("found_by") or found_by, "evidence": n["evidence"][:3],
                                              "added_on": datetime.now(timezone.utc).date().isoformat()})
        added.append(n["topic"])
    if added:
        header = ("# Topics watched by the Hot-Topic Radar (scripts/run_radar.py) and watch mode (scripts/watch.py).\n"
                  "# `terms` are matched literally in paper/patent titles and abstracts and in X posts; keep them specific.\n"
                  "# `sector` must be a key from sectors.yaml. Entries with `found_by: x watch` were proposed by the Chief model\n"
                  "# from real posts (`evidence` = post ids); `found_by: paper scout` were found from growing paper keywords\n"
                  "# (`evidence` = OpenAlex work ids). Both can be removed by hand at any time. The file is rewritten by the watcher.\n\n")
        path.write_text(header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    return added


class Watcher:
    def __init__(
        self,
        settings: Settings,
        *,
        x_client,                                   # XClient | None
        accounts: list[str],
        router: Optional[ModelRouter],
        openalex,                                   # OpenAlexClient | None
        patents_cached,                             # patent client in cache-only mode | None
        patents_live_factory: Optional[Callable[[], Any]] = None,   # makes a live patent client (quota) | None
        filers=None,
        run_research: Optional[Callable[[str], Optional[str]]] = None,  # topic -> run id (None = not run)
        report_ages: Optional[Callable[[], dict[str, datetime]]] = None,  # topic -> newest report time
        state_path: Path = STATE_PATH,
        topics_file: Optional[Path] = None,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.s = settings
        self.x, self.accounts, self.router = x_client, accounts, router
        self.openalex, self.patents_cached, self.patents_live_factory, self.filers = openalex, patents_cached, patents_live_factory, filers
        self.run_research = run_research
        self.report_ages = report_ages or (lambda: {})
        self.state_path, self.topics_file, self._now = state_path, topics_file, now

    # ---- steps --------------------------------------------------------
    def scan(self, state: WatchState) -> Optional[Scan]:
        now = self._now()
        if self.x is None or not self.accounts:
            state.log("scan", "skipped: X not configured or no approved accounts", now)
            return None
        try:
            posts = self.x.recent_from_accounts(self.accounts, max_posts=50, since_id=state.last_post_id)
        except SourceError as exc:
            state.log("scan", f"X scan failed: {exc.message}", now)
            return None
        topics = load_topics(self.topics_file)
        mentions = count_mentions(posts, topics)
        new_topics = scout_new_topics(self.router, posts, topics, sectors=self._sector_keys()) if posts else []
        newest = max((p.url.rsplit("/", 1)[-1] for p in posts), key=lambda x: int(x) if x.isdigit() else 0, default=state.last_post_id)
        cost = self.x.usage.cost_usd
        state.last_scan_at, state.last_post_id = now, newest
        state.mention_history.append({"at": now.isoformat(), "mentions": mentions})
        state.mention_history = state.mention_history[-200:]
        state.log("scan", f"{len(posts)} new post(s) from {len(self.accounts)} accounts; topics mentioned: {mentions or 'none'}"
                  + (f"; new topics proposed: {[n['topic'] for n in new_topics]}" if new_topics else ""), now, posts=len(posts), mentions=mentions)
        return Scan(now, len(posts), newest, mentions, new_topics, cost)

    def _sector_keys(self) -> list[str]:
        try:
            return [s.key for s in load_sectors()] or [DEFAULT_SECTOR]
        except Exception:  # noqa: BLE001
            return [DEFAULT_SECTOR]

    def paper_discovery(self, state: WatchState) -> list[str]:
        """Every WATCH_PAPER_DISCOVERY_DAYS: find growing paper keywords per sector and add them as topics."""
        now = self._now()
        if self.openalex is None or self.s.watch_paper_discovery_days <= 0 or not hasattr(self.openalex, "recent_keywords"):
            return []
        if state.last_paper_discovery_at and now - state.last_paper_discovery_at < timedelta(days=self.s.watch_paper_discovery_days):
            return []
        from app.radar.discovery import discover_topics
        known = load_topics(self.topics_file)
        found: list[dict] = []
        notes: list[str] = []
        try:
            sectors = load_sectors()
        except Exception as exc:  # noqa: BLE001
            state.log("topics", f"paper scout skipped: sectors.yaml unreadable ({type(exc).__name__})", now)
            return []
        for sector in sectors:
            new, n = discover_topics(self.openalex, sector,
                                     known + [TopicConfig(name=f["topic"], terms=f["terms"], sector=f["sector"]) for f in found], now=self._now)
            found += new
            notes += n
        state.last_paper_discovery_at = now
        added = add_topics(found, self.topics_file, found_by="paper scout") if found else []
        state.log("topics", f"paper scout: {len(added)} new topic(s) from growing paper keywords across {len(sectors)} sectors"
                  + (f": {[(f['topic'], f['sector']) for f in found if f['topic'] in added]}" if added else "")
                  + (f"; {len(notes)} candidate(s) rejected" if notes else ""), now, topics=added)
        return added

    def refresh_radar(self, state: WatchState, scan: Optional[Scan]) -> Optional[Radar]:
        now = self._now()
        added = add_topics(scan.new_topics, self.topics_file) if scan and scan.new_topics else []
        if added:
            state.log("topics", f"added to the radar from X posts: {added}", now, topics=added)
        self.paper_discovery(state)
        topics = load_topics(self.topics_file)
        # patents: cache for everyone; a live count only for a new topic, within the weekly allowance
        live_for: set[str] = set()
        if self.patents_live_factory:
            for t in topics:
                if t.name in state.last_patent_refresh:
                    continue
                if state.new_patent_topics_this_week(now) + len(live_for) >= self.s.watch_new_patent_topics_per_week:
                    break
                live_for.add(t.name)
        try:
            radar = compute_radar([t for t in topics if t.name not in live_for], openalex=self.openalex, patents=self.patents_cached,
                                  filers=self.filers, now=self._now)
            if live_for:
                live = compute_radar([t for t in topics if t.name in live_for], openalex=self.openalex, patents=self.patents_live_factory(),
                                     filers=self.filers, now=self._now)
                for t in live.topics:
                    state.last_patent_refresh[t.topic] = now.date().isoformat()
                from app.radar import rank_topics
                radar.topics = rank_topics([*radar.topics, *live.topics])
                radar.searches_used += live.searches_used
        except SourceError as exc:
            state.log("radar", f"radar refresh failed: {exc.message}", now)
            return load_radar()
        save_radar(radar)
        state.log("radar", f"radar refreshed: {len(radar.topics)} topics", now)
        return radar

    def decide(self, state: WatchState, radar: Optional[Radar], scan: Optional[Scan]) -> list[tuple[str, str]]:
        """-> [(topic, reason)] to research now, honouring caps and report freshness."""
        now = self._now()
        ages = self.report_ages()
        candidates: list[tuple[float, str, str]] = []
        heat = {t.topic: (t.heat or 0.0) for t in (radar.topics if radar else []) if t.rank}
        mentions = scan.mentions if scan else {}
        for topic in {*heat, *mentions}:
            reasons = []
            if heat.get(topic, 0) >= self.s.watch_heat_threshold:
                reasons.append(f"radar heat {heat[topic]:+.0f}% >= {self.s.watch_heat_threshold:.0f}%")
            if mentions.get(topic, 0) >= self.s.watch_x_mentions_threshold:
                reasons.append(f"{mentions[topic]} approved-account posts mention it in this scan")
            if not reasons:
                continue
            newest = ages.get(topic.lower())
            if newest and now - newest < timedelta(days=self.s.watch_report_max_age_days):
                state.log("skip", f"{topic}: report from {newest.date()} is still fresh", now, topic=topic)
                continue
            candidates.append((heat.get(topic, 0) + 10 * mentions.get(topic, 0), topic, "; ".join(reasons)))
        candidates.sort(reverse=True)
        chosen: list[tuple[str, str]] = []
        for _, topic, reason in candidates:
            if state.runs_today(now) + len(chosen) >= self.s.watch_max_runs_per_day:
                state.log("skip", f"{topic}: daily cap of {self.s.watch_max_runs_per_day} research run(s) reached", now, topic=topic)
                continue
            chosen.append((topic, reason))
        return chosen

    def cycle(self) -> WatchState:
        state = load_state(self.state_path)
        scan = self.scan(state)
        radar = self.refresh_radar(state, scan)
        for topic, reason in self.decide(state, radar, scan):
            now = self._now()
            state.log("trigger", f"researching '{topic}': {reason}", now, topic=topic)
            save_state(state, self.state_path)
            run_id = self.run_research(topic) if self.run_research else None
            state.runs_started.append({"at": now.isoformat(), "topic": topic, "run_id": run_id})
            state.log("run", f"'{topic}' -> {'report ' + str(run_id) if run_id else 'run failed or disabled'}", self._now(), topic=topic, run_id=run_id)
        save_state(state, self.state_path)
        return state

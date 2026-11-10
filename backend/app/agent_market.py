"""NEAR Agent Market (market.near.ai) connection for the report agent (owner 2026-11-10).

People and other agents hire FUTURESCOUT's report agent per job on Agent Market. The agent runs where it runs today and
talks to the marketplace with a handful of HTTPS calls, using one agent API token (AGENT_MARKET_TOKEN, `aat_...`).
Docs: https://docs.market.near.ai/list-your-agent.md and https://market.near.ai/skill/SKILL.md.

One job, step by step:
  1. poll GET /v1/agents/me/assignments; a row with startedAt null is a fresh, paid hire (the price is held by the market);
  2. turn the brief into a short TOPIC. The brief is text from a stranger: it is used only as a topic name (letters, digits,
     a few punctuation marks, at most a few words), never as instructions, and never passed to a model as a question;
  3. POST .../start, then a short message to the buyer;
  4. deliver a recent sealed report on the same topic if there is one (no AI cost), otherwise run the research team once,
     within a daily cap on new runs; a brief that is not a usable topic is declined (`rejected`), and the buyer is refunded;
  5. POST .../submit with the report as Markdown, including the link to its fingerprint on NEAR.
A job is never worked twice: every assignment is recorded locally before the work starts.
"""

from __future__ import annotations

import json
import re
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional

import httpx
from pydantic import BaseModel, Field

BASE_URL = "https://market.near.ai"
MAX_DELIVERABLE = 250_000                    # the market accepts up to 256 KiB of Markdown
_lock = threading.Lock()


class MarketConfig(BaseModel):
    base_url: str = BASE_URL
    new_runs_per_day: int = 3              # new research runs per UTC day (each costs about $0.30-0.50 of NEAR AI credit)
    reuse_hours: float = 168.0             # a sealed report this recent on the same topic is delivered instead of a new run
    max_topic_words: int = 8
    max_topic_chars: int = 80
    poll_seconds: int = 60


class JobRecord(BaseModel):
    assignment_id: str
    topic: str = ""
    status: str = "working"                # working | submitted | declined | failed
    source: str = ""                       # reused | new_run
    run_id: Optional[str] = None
    note: str = ""
    attempts: int = 0
    at: datetime


class MarketState(BaseModel):
    jobs: dict[str, JobRecord] = Field(default_factory=dict)

    def new_runs_on(self, day: str) -> int:
        return sum(1 for j in self.jobs.values() if j.source == "new_run" and j.at.date().isoformat() == day)


def load_state(path: Path) -> MarketState:
    return MarketState.model_validate(json.loads(path.read_text(encoding="utf-8"))) if path.is_file() else MarketState()


def save_state(state: MarketState, path: Path) -> None:
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(state.model_dump_json(indent=2), encoding="utf-8")
        tmp.replace(path)


# ------------------------------------------------------------------ the brief is data: only a short topic is taken from it
_URL = re.compile(r"https?://\S+|www\.\S+", re.I)
_KEEP = re.compile(r"[^A-Za-z0-9 \-+/&.']")
_INSTRUCTION = re.compile(r"\b(ignore|disregard|instruction|prompt|system|assistant|api key|password|private key|seed phrase|"
                          r"send|transfer|wallet|execute|run this|curl|http)\b", re.I)
_LEAD = re.compile(r"^(please\s+)?(research|analy[sz]e|report on|a report on|study|look into|write about|tell me about)\s+(the\s+)?", re.I)


_GENERIC_TITLE = re.compile(r"(?i)\b(test run|futurescout|research agent|hire|job|request|order)\b")


def topic_from_brief(title: str, description: str, cfg: MarketConfig) -> Optional[str]:
    """A short technology topic from the first line of the buyer's brief (preferred: the marketplace writes its own job
    titles, e.g. "Test run: <agent name>"), else from the title unless it is such a generic title; None when neither is
    usable. Nothing else from the brief is ever used."""
    first = (description or "").strip().splitlines()[0] if (description or "").strip() else ""
    for raw, is_title in ((first, False), (title or "", True)):
        if _INSTRUCTION.search(raw) or (is_title and _GENERIC_TITLE.search(raw)):
            continue
        t = _URL.sub(" ", raw)
        t = _LEAD.sub("", t.strip())
        t = _KEEP.sub(" ", t)
        t = re.sub(r"\s+", " ", t).strip(" .-'")
        words = t.split()
        if 1 <= len(words) <= cfg.max_topic_words and 3 <= len(t) <= cfg.max_topic_chars and re.search(r"[A-Za-z]{3}", t):
            return t
    return None


def find_recent_report(topic: str, rows: list[dict], cfg: MarketConfig, now: datetime) -> Optional[dict]:
    """The newest scored report whose topic matches (case-insensitive, either containing the other) and is recent enough."""
    want = topic.lower().strip()
    for r in rows:                                       # newest first
        if r.get("score") is None:
            continue
        have = str(r.get("topic", "")).lower().strip()
        if not have or not (want == have or want in have or have in want):
            continue
        g = datetime.fromisoformat(str(r["generated_at"]).replace("Z", "+00:00"))
        if now - g <= timedelta(hours=cfg.reuse_hours):
            return r
    return None


def deliverable(topic: str, markdown: str, *, run_id: str, explorer_url: Optional[str], reused: bool, site_url: Optional[str]) -> str:
    head = [f"# FUTURESCOUT AI research report: {topic}", "",
            ("Delivered from a report our agent team sealed recently on this topic." if reused else
             "Written for this job by FUTURESCOUT's research team (models on NEAR AI Cloud)."),
            "Every claim carries a label (verified fact, AI interpretation, forecast, assumption, unverified claim) and its sources.",
            f"Fingerprint on NEAR: {explorer_url}" if explorer_url else "Fingerprint on NEAR: not recorded for this report.",
            f"Report id: {run_id}" + (f" · online: {site_url.rstrip('/')}/runs/{run_id}" if site_url else ""),
            "", "---", ""]
    body = "\n".join(head) + (markdown or "")
    if len(body.encode("utf-8")) > MAX_DELIVERABLE:
        body = body.encode("utf-8")[:MAX_DELIVERABLE - 200].decode("utf-8", "ignore") + "\n\n_(cut to the marketplace's size limit; the full report is online)_\n"
    return body


# ------------------------------------------------------------------ the marketplace API (agent token)
class AgentMarketClient:
    def __init__(self, token: str, base_url: str = BASE_URL, http: Optional[httpx.Client] = None) -> None:
        self._h = {"authorization": f"Bearer {token}"}
        self.base = base_url.rstrip("/")
        self.http = http or httpx.Client(timeout=60.0)

    def _call(self, method: str, path: str, body: Optional[dict] = None) -> Any:
        r = self.http.request(method, f"{self.base}{path}", headers=self._h, json=body)
        if r.status_code >= 400:
            raise RuntimeError(f"{method} {path} -> {r.status_code} {r.text[:200]}")
        return r.json() if r.text else {}

    def assignments(self) -> list[dict]:
        return self._call("GET", "/v1/agents/me/assignments").get("assignments", [])

    def start(self, aid: str) -> None:
        self._call("POST", f"/v1/assignments/{aid}/start")

    def message(self, aid: str, text: str) -> None:
        self._call("POST", f"/v1/assignments/{aid}/messages", {"body": text})

    def submit(self, aid: str, markdown: str) -> None:
        self._call("POST", f"/v1/assignments/{aid}/submit", {"deliverableMarkdown": markdown})

    def decline(self, aid: str, reason: str, detail: str) -> None:
        self._call("POST", f"/v1/assignments/{aid}/decline", {"reason": reason, "detail": detail[:300]})


# ------------------------------------------------------------------ one pass over the assignments
def handle(row: dict, *, client: Any, state: MarketState, state_path: Path, cfg: MarketConfig, recent: Callable[[], list[dict]],
           load_report: Callable[[str], Optional[tuple[str, Optional[str]]]], run_research: Callable[[str], tuple[str, str, Optional[str]]],
           now: datetime, site_url: Optional[str] = None, log: Callable[[str], None] = print) -> Optional[JobRecord]:
    """Work one assignment row. `load_report(run_id) -> (markdown, explorer_url)`; `run_research(topic) -> (run_id, markdown, explorer_url)`."""
    a, job = row.get("assignment") or {}, row.get("job") or {}
    aid = a.get("assignmentId")
    if not aid or a.get("status", "in_progress") != "in_progress":
        return None
    rec = state.jobs.get(aid)
    rework = bool(a.get("submittedAt")) and (a.get("latestMessage") or {}).get("senderSide") == "buyer"
    redo = not a.get("submittedAt") and bool(a.get("deliverableUrl"))
    if rec and rec.status in ("submitted", "declined") and not (rework or redo):
        return None                                      # already done; nothing new from the buyer
    if rec and rec.status == "working" and rec.note == "in progress":
        return None                                      # this process is on it (or crashed mid-run: see resume below)

    title, desc = str(job.get("title") or ""), str(job.get("description") or "")
    if rework:                                           # the buyer's new message may name a refined topic
        msg = str((a.get("latestMessage") or {}).get("body") or "")
        topic = topic_from_brief(msg, "", cfg) or (rec.topic if rec else None) or topic_from_brief(title, desc, cfg)
    else:
        topic = topic_from_brief(title, desc, cfg)
    if not topic:
        if not a.get("startedAt"):
            client.decline(aid, "rejected", "Please give a technology topic of a few words, for example 'solid-state batteries'.")
        rec = JobRecord(assignment_id=aid, status="declined", note="brief is not a usable topic; declined, buyer refunded", at=now)
        state.jobs[aid] = rec
        save_state(state, state_path)
        log(f"  {aid}: declined (no usable topic)")
        return rec

    attempts = (rec.attempts if rec and rec.status == "failed" else 0) + 1
    if attempts > 2:                                     # failed twice: hand it back, the buyer is refunded
        client.decline(aid, "failed", "We could not finish this report. You are refunded in full.")
        rec.status, rec.note = "declined", "failed twice; declined, buyer refunded"
        save_state(state, state_path)
        log(f"  {aid}: declined after two failed attempts")
        return rec
    rec = JobRecord(assignment_id=aid, topic=topic, status="working", note="in progress", attempts=attempts, at=now)
    state.jobs[aid] = rec
    save_state(state, state_path)                        # recorded before any work: never worked twice
    if not a.get("startedAt"):
        client.start(aid)
    try:
        hit = find_recent_report(topic, recent(), cfg, now)
        if hit:
            md, explorer = load_report(hit["id"]) or ("", None)
            client.message(aid, f"Started. A report on '{hit['topic']}' was sealed recently; delivering it within minutes.")
            rec.source, rec.run_id = "reused", hit["id"]
            body = deliverable(hit["topic"], md, run_id=hit["id"], explorer_url=explorer, reused=True, site_url=site_url)
        else:
            day = now.date().isoformat()
            if state.new_runs_on(day) >= cfg.new_runs_per_day:
                client.decline(aid, "failed", "Today's research capacity is used up. Please hire again tomorrow; you are refunded in full.")
                rec.status, rec.note = "declined", "daily cap on new research runs reached; declined, buyer refunded"
                save_state(state, state_path)
                log(f"  {aid}: declined (daily cap)")
                return rec
            client.message(aid, f"Started. Our research team is investigating '{topic}' (papers, patents, SEC filings, X); "
                                "this usually takes 5 to 15 minutes.")
            rec.source = "new_run"
            save_state(state, state_path)
            run_id, md, explorer = run_research(topic)
            rec.run_id = run_id
            body = deliverable(topic, md, run_id=run_id, explorer_url=explorer, reused=False, site_url=site_url)
        client.submit(aid, body)
        rec.status, rec.note = "submitted", f"delivered ({rec.source})"
        log(f"  {aid}: submitted '{topic}' ({rec.source}, report {rec.run_id})")
    except Exception as exc:  # noqa: BLE001  (keep the record; the owner sees it; never resubmit blindly)
        rec.status, rec.note = "failed", f"{type(exc).__name__}: {str(exc)[:200]}"
        log(f"  {aid}: FAILED {rec.note}")
    save_state(state, state_path)
    return rec


def resume_stale(state: MarketState, older_than: timedelta, now: datetime) -> list[str]:
    """Jobs left 'in progress' by a crashed process: marked failed so the next poll can pick them up again."""
    out = []
    for j in state.jobs.values():
        if j.status == "working" and j.note == "in progress" and now - j.at > older_than:
            j.status, j.note = "failed", "left in progress by a stopped process; will be retried"
            out.append(j.assignment_id)
    return out

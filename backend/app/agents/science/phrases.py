"""Which phrases count as "papers about this topic" (code + an AI relevance check).

Exact-phrase counting misses synonyms ("agentic AI", "LLM agents" for "AI agents") and abbreviations, while a loose
synonym can pull in a different field ("VLA" is also the Very Large Array telescope). So:

  1. candidates = topic name + the topic's configured terms (config/topics.yaml) + up to 4 synonyms or abbreviations
     suggested by a model (they are only search phrases; nothing is counted on the model's word)
  2. for each candidate, a random sample of recent matching works (title + start of abstract) from OpenAlex
  3. one model call judges, paper by paper, whether each sampled work is about the topic
  4. a phrase is kept when at least MIN_SHARE of its sample is on-topic (the topic name is always kept)
  5. the counts use ANY of the kept phrases (one OpenAlex OR query, each work counted once)
  6. a final random sample of the combined matches gives the share that is on-topic (precision), shown next to
     the counts so a reader sees roughly how many counted works are really about the topic

All numbers are OpenAlex counts or plain shares of a sample; the AI only answers "on-topic or not" per paper,
which is an ai_interpretation. The result is cached per topic for CACHE_DAYS so the radar and repeat runs reuse it.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Optional

from pydantic import BaseModel, Field

from app.config import BACKEND_DIR
from app.schemas.science import CountingBasis, PhraseCheck
from app.sources.base import SourceError
from app.sources.openalex import clean_phrase

log = logging.getLogger("futurescout.science.phrases")

AGENT = "relevance"              # model alias in config/model_config.yaml
SAMPLE_PER_PHRASE = 8
PRECISION_SAMPLE = 20
MIN_SAMPLE = 3                   # a phrase with fewer matching works than this is not worth a separate check
MIN_SHARE = 0.75               # 6 of 8 sampled works on-topic (5/8 let broader phrases like 'autonomous agents' in)
MAX_SUGGESTED = 4
MAX_PHRASES = 6
LOOKBACK_YEARS = 3
CACHE_DAYS = 7
CACHE_DIR = BACKEND_DIR / "cache" / "phrases"


class _Suggestions(BaseModel):
    phrases: list[str] = Field(default_factory=list)


class _Verdicts(BaseModel):
    relevant_ids: list[str] = Field(default_factory=list)


def _slug(topic: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:80] or "topic"


def _norm(p: str) -> str:
    return " ".join(clean_phrase(p).lower().split())


def configured_terms(topic: str) -> list[str]:
    from app.radar import load_topics
    key = _norm(topic)
    for t in load_topics():
        if key == _norm(t.name) or key in {_norm(x) for x in t.terms}:
            return list(t.terms)
    return []


def load_cached(topic: str, *, now: Optional[datetime] = None, cache_dir: Path = CACHE_DIR) -> Optional[CountingBasis]:
    path = cache_dir / f"{_slug(topic)}.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        made = datetime.fromisoformat(data["made_at"])
        if (now or datetime.now(timezone.utc)) - made > timedelta(days=CACHE_DAYS):
            return None
        return CountingBasis.model_validate(data["basis"])
    except (KeyError, ValueError, TypeError):
        return None


def _save(topic: str, basis: CountingBasis, now: datetime, cache_dir: Path) -> None:
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / f"{_slug(topic)}.json").write_text(
            json.dumps({"made_at": now.isoformat(), "basis": basis.model_dump(mode="json")}, indent=1), encoding="utf-8")
    except OSError:
        pass


def _suggest(router, topic: str, known: list[str]) -> list[str]:  # noqa: ANN001
    reply = router.complete(AGENT, [
        {"role": "system", "content": (
            "You help count research papers about a technology topic. Give up to 4 alternative phrases that "
            "researchers use in paper TITLES or ABSTRACTS for exactly this topic: synonyms, common abbreviations "
            "written as they appear (e.g. 'LLM agents'), and closely equivalent names. Each must be 2-5 words or a "
            "distinctive abbreviation phrase; never a single common word, never a broader field, never a narrower "
            "sub-technique. Do not repeat phrases already listed. Answer as JSON {\"phrases\": [...]}.")},
        {"role": "user", "content": f"Topic: {topic}\nAlready used: {', '.join(known)}"},
    ], response_model=_Suggestions)
    out = []
    for p in reply.parsed.phrases:  # type: ignore[union-attr]
        c = clean_phrase(p)
        if c and (len(c.split()) >= 2 or re.search(r"[A-Z]{2,}", c)) and len(c) <= 60:
            out.append(c)
    return out[:MAX_SUGGESTED]


def _judge(router, topic: str, papers: list[dict]) -> tuple[set[str], Optional[str]]:  # noqa: ANN001
    if not papers:
        return set(), None
    listing = "\n\n".join(f"[{p['id']}] {p['title']}\n{p['abstract'] or '(no abstract)'}" for p in papers)
    reply = router.complete(AGENT, [
        {"role": "system", "content": (
            "Decide, for each paper, whether it is mainly ABOUT the given technology topic (studies, builds, "
            "evaluates or applies it as a central subject). A paper that only mentions the words in passing, or uses "
            "the same words for something else (another field, another meaning of an abbreviation), is NOT relevant. "
            "Judge only from the title and abstract shown. Answer as JSON {\"relevant_ids\": [ids of relevant papers]}.")},
        {"role": "user", "content": f"Topic: {topic}\n\nPapers:\n\n{listing}"},
    ], response_model=_Verdicts)
    ids = {p["id"] for p in papers}
    return {i for i in reply.parsed.relevant_ids if i in ids}, reply.llm_alias  # type: ignore[union-attr]


def build_counting_basis(
    openalex, router, topic: str, *,  # noqa: ANN001
    today: Optional[date] = None,
    now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    cache_dir: Path = CACHE_DIR,
    use_cache: bool = True,
) -> Optional[CountingBasis]:
    """Kept phrases + relevance checks for `topic`, or None if OpenAlex or the model is unavailable."""
    if openalex is None or router is None or not hasattr(openalex, "sample_works"):
        return None
    if use_cache and (cached := load_cached(topic, now=now(), cache_dir=cache_dir)):
        return cached
    today = today or now().date()
    since = date(today.year - LOOKBACK_YEARS, 1, 1)
    name = clean_phrase(topic)

    candidates: list[tuple[str, str]] = [(name, "topic")]
    seen = {_norm(name)}
    for t in configured_terms(topic):
        if _norm(t) not in seen:
            seen.add(_norm(t))
            candidates.append((clean_phrase(t), "config"))
    try:
        for t in _suggest(router, topic, [c for c, _ in candidates]):
            if _norm(t) not in seen:
                seen.add(_norm(t))
                candidates.append((t, "ai_suggested"))
    except Exception as exc:  # noqa: BLE001  (suggestions are optional)
        log.warning("phrase suggestions failed: %s", type(exc).__name__)
    candidates = candidates[:MAX_PHRASES + 2]

    checks: list[PhraseCheck] = []
    samples: dict[str, list[dict]] = {}
    try:
        for phrase, source in candidates:
            matches = openalex.count_between(phrase, since, today)
            check = PhraseCheck(phrase=phrase, source=source, matches=matches)
            if matches >= MIN_SAMPLE:
                samples[phrase] = openalex.sample_works(phrase, SAMPLE_PER_PHRASE, from_date=since)
            checks.append(check)
    except SourceError as exc:
        log.warning("OpenAlex during phrase check: %s", exc.message)
        return None

    # one judging call for all phrase samples (ids are made unique per phrase)
    tagged = [{**p, "id": f"{i}.{j}"} for i, (ph, ps) in enumerate(samples.items()) for j, p in enumerate(ps)]
    alias = None
    try:
        relevant, alias = _judge(router, topic, tagged)
    except Exception as exc:  # noqa: BLE001
        log.warning("relevance judging failed: %s", type(exc).__name__)
        return None
    for i, (ph, ps) in enumerate(samples.items()):
        check = next(c for c in checks if c.phrase == ph)
        check.sampled = len(ps)
        check.relevant = sum(1 for j in range(len(ps)) if f"{i}.{j}" in relevant)
    for c in checks:
        share = c.relevant / c.sampled if c.sampled else 0.0
        if c.source == "topic":
            c.kept, c.reason = True, f"the topic name itself ({c.relevant}/{c.sampled} sampled works on-topic)"
        elif c.matches < MIN_SAMPLE:
            c.reason = f"only {c.matches} matching works"
        elif share >= MIN_SHARE:
            c.kept, c.reason = True, f"{c.relevant}/{c.sampled} sampled works on-topic"
        else:
            c.reason = f"only {c.relevant}/{c.sampled} sampled works on-topic (needs {MIN_SHARE:.0%})"
    # best first: the topic name, then configured terms, then by on-topic share; the cap drops the weakest
    rank = {"topic": 0, "config": 1, "ai_suggested": 2}
    ordered = sorted((c for c in checks if c.kept),
                     key=lambda c: (rank[c.source] if c.source == "topic" else 1, -(c.relevant / c.sampled if c.sampled else 0), rank[c.source]))
    kept = [c.phrase for c in ordered][:MAX_PHRASES]
    for c in ordered[MAX_PHRASES:]:
        c.kept, c.reason = False, c.reason + f" (left out: at most {MAX_PHRASES} phrases)"

    basis = CountingBasis(phrases=kept, checks=checks, llm_alias=alias)
    try:
        sample = [{**w, "id": f"p{i}"} for i, w in enumerate(openalex.sample_works(kept, PRECISION_SAMPLE, from_date=since, seed=11))]
        rel, _ = _judge(router, topic, sample)   # short ids: models echo them back reliably (long OpenAlex URLs got shortened)
        basis.precision_sampled, basis.precision_relevant = len(sample), len(rel)
        basis.precision_pct = round(len(rel) / len(sample) * 100, 1) if sample else None
    except Exception as exc:  # noqa: BLE001
        log.warning("precision check failed: %s", type(exc).__name__)
    dropped = [c.phrase for c in checks if not c.kept]
    basis.note = (
        f"Counted: works whose title or abstract contains any of {', '.join(repr(p) for p in kept)} (singular and "
        f"plural forms match automatically; a work matching several phrases is counted once)."
        + (f" Not counted, because too few sampled works were about this topic: {', '.join(repr(p) for p in dropped)}." if dropped else "")
        + (f" An AI check of {basis.precision_sampled} random counted works found {basis.precision_relevant} "
           f"({basis.precision_pct:.0f}%) mainly about the topic." if basis.precision_pct is not None else "")
    )
    _save(topic, basis, now(), cache_dir)
    return basis

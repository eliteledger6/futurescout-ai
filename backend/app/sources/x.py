"""X (Twitter) API v2 client. READ-ONLY by construction: it has no method that posts, likes,
reposts, follows or sends messages, and the project rules forbid adding one.

Endpoints used (checked against docs.x.com on 2026-11-08):
  GET /2/users/by?usernames=...        look up accounts (to verify watchlist handles)
  GET /2/tweets/search/recent?query=   posts from the last 7 days, 10-100 per page
Pricing (pay-per-use, docs.x.com/x-api/getting-started/pricing, 2026-11-08): $0.005 per post read,
$0.010 per user read; failed requests are not billed; the same resource within 24 h is billed once.
This client counts what each call returned so a report can show the X cost.

Posts are SOCIAL SIGNALS: stored with content_type social_post, and the citation guard never lets
them verify a fact. The bearer token is sent only in the Authorization header and never logged.
"""

from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional

import httpx

from app.schemas.common import ContentType, SourceRecord
from app.sources.base import RateLimiter, SourceError, get_with_retry

API = "https://api.x.com/2"
SOURCE = "X API"
PRICE_PER_POST_READ = 0.005
PRICE_PER_USER_READ = 0.010
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")


@dataclass
class XUser:
    id: str
    username: str
    name: str
    description: str
    verified: bool
    verified_type: Optional[str]
    followers: Optional[int]
    created_at: Optional[str]


@dataclass
class XUsage:
    posts_read: int = 0
    users_read: int = 0
    requests: int = 0

    @property
    def cost_usd(self) -> float:
        # upper bound: X does not bill the same resource twice within 24 h
        return round(self.posts_read * PRICE_PER_POST_READ + self.users_read * PRICE_PER_USER_READ, 4)

    def as_dict(self) -> dict:
        return {"posts_read": self.posts_read, "users_read": self.users_read, "requests": self.requests,
                "cost_usd": self.cost_usd}


def post_url(username: str, post_id: str) -> str:
    return f"https://x.com/{username}/status/{post_id}"


def parse_users(payload: object) -> tuple[list[XUser], list[str]]:
    """-> (found users, usernames X reported as not found/suspended)."""
    if not isinstance(payload, dict):
        raise SourceError(SOURCE, "user lookup response had an unexpected shape")
    users = []
    for u in payload.get("data") or []:
        metrics = u.get("public_metrics") or {}
        users.append(XUser(
            id=str(u["id"]), username=u["username"], name=u.get("name", ""), description=u.get("description", ""),
            verified=bool(u.get("verified")), verified_type=u.get("verified_type"),
            followers=metrics.get("followers_count"), created_at=u.get("created_at"),
        ))
    missing = [str(e.get("value") or e.get("resource_id") or "") for e in payload.get("errors") or []]
    return users, [m for m in missing if m]


def parse_posts(payload: object, retrieved_at: datetime) -> list[SourceRecord]:
    if not isinstance(payload, dict):
        raise SourceError(SOURCE, "search response had an unexpected shape")
    authors = {u["id"]: u for u in (payload.get("includes") or {}).get("users") or []}
    records = []
    for p in payload.get("data") or []:
        author = authors.get(p.get("author_id"))
        text = re.sub(r"\s+", " ", p.get("text") or "").strip()
        if not author or not text or not p.get("id"):
            continue
        created = (p.get("created_at") or "")[:10] or None
        metrics = p.get("public_metrics") or {}
        engagement = sum(int(metrics.get(k) or 0) for k in ("like_count", "retweet_count", "reply_count", "quote_count")) if metrics else None
        records.append(SourceRecord(
            cited_by_count=engagement,   # for a post: likes + reposts + replies + quotes at retrieval time
            url=post_url(author["username"], str(p["id"])), source_name=SOURCE, content_type=ContentType.SOCIAL_POST,
            title=f"@{author['username']}: {text[:90]}{'…' if len(text) > 90 else ''}",
            published_at=created, retrieved_at=retrieved_at,
            authors=[f"@{author['username']}"], organization=author.get("name"),
            publication_type="x post", abstract=text,   # full post text: posts are short
            text_depth="full_text",
        ))
    return records


class XClient:
    def __init__(
        self,
        bearer_token: str,
        *,
        http: Optional[httpx.Client] = None,
        limiter: Optional[RateLimiter] = None,
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        if not bearer_token:
            raise SourceError(SOURCE, "X_BEARER_TOKEN is not set")
        self._token = bearer_token
        self._http = http or httpx.Client(timeout=30.0, headers={"Authorization": f"Bearer {bearer_token}"})
        self._limiter = limiter or RateLimiter(1.0)
        self._sleep = sleep
        self._now = now
        self.usage = XUsage()

    def _get(self, path: str, params: dict) -> dict:
        response = get_with_retry(
            self._http, f"{API}{path}", source=SOURCE, params=params, secrets=[self._token], sleep=self._sleep,
            before_request=self._limiter.wait, max_attempts=2,
            status_hints={401: "X rejected the bearer token (check X_BEARER_TOKEN)",
                          402: "X API credit is exhausted or billing is not set up",
                          403: "X refused this request for this app (check the app's access level)",
                          429: "X rate limit reached; try again later"},
        )
        self.usage.requests += 1
        try:
            return response.json()
        except ValueError:
            raise SourceError(SOURCE, "response was not valid JSON") from None

    def lookup_users(self, usernames: list[str]) -> tuple[list[XUser], list[str]]:
        """Verify handles. Invalid-looking handles are rejected locally (not sent, not billed)."""
        clean = [u.lstrip("@") for u in usernames]
        bad = [u for u in clean if not USERNAME_RE.match(u)]
        if bad:
            raise SourceError(SOURCE, f"not valid X usernames: {', '.join(bad)}")
        found: list[XUser] = []
        missing: list[str] = []
        for i in range(0, len(clean), 100):
            payload = self._get("/users/by", {
                "usernames": ",".join(clean[i:i + 100]),
                "user.fields": "name,description,verified,verified_type,public_metrics,created_at",
            })
            users, gone = parse_users(payload)
            self.usage.users_read += len(users)
            found += users
            missing += gone
        return found, missing

    def discover_accounts(self, keywords: list[str], *, exclude: set[str], max_posts: int = 50,
                          min_followers: int = 1000) -> list[AccountSuggestion]:
        """Who posts about the topic? One recent search over all of X (cost: posts read), authors come with
        the response (no extra user lookups). Returns ranked suggestions, excluding `exclude` handles."""
        max_posts = max(10, min(max_posts, 100))
        payload = self._get("/tweets/search/recent", {
            "query": build_topic_query(keywords), "max_results": max_posts, "sort_order": "relevancy",
            "tweet.fields": "created_at,author_id,public_metrics", "expansions": "author_id",
            "user.fields": "username,name,description,verified_type,public_metrics,created_at",
        })
        if not isinstance(payload, dict):
            raise SourceError(SOURCE, "search response had an unexpected shape")
        posts = payload.get("data") or []
        self.usage.posts_read += len(posts)
        users = {u["id"]: u for u in (payload.get("includes") or {}).get("users") or []}
        by_author: dict[str, AccountSuggestion] = {}
        for p in posts:
            u = users.get(p.get("author_id"))
            if not u or u["username"].lower() in exclude:
                continue
            m = p.get("public_metrics") or {}
            s = by_author.get(u["id"])
            if s is None:
                s = by_author[u["id"]] = AccountSuggestion(
                    handle=u["username"], id=str(u["id"]), name=u.get("name", ""), description=" ".join((u.get("description") or "").split()),
                    verified_type=u.get("verified_type"), followers=(u.get("public_metrics") or {}).get("followers_count"),
                    posts_on_topic=0, engagement=0, sample_post_urls=[], role=exec_role(u.get("description") or ""))
            s.posts_on_topic += 1
            s.engagement += sum(int(m.get(k) or 0) for k in ("like_count", "retweet_count", "reply_count", "quote_count"))
            if len(s.sample_post_urls) < 3:
                s.sample_post_urls.append(post_url(u["username"], str(p["id"])))
        out = []
        for s in by_author.values():
            text = f"{s.handle} {s.name} {s.description}".lower()
            if any(w in text for w in PROMO_WORDS):
                s.flags.append("trading-tip, promotional or parody wording in the profile")
            if (s.followers or 0) < min_followers:
                s.flags.append(f"fewer than {min_followers} followers")
            if not s.description:
                s.flags.append("empty profile description")
            s.score = suggestion_score(s)
            out.append(s)
        return sorted(out, key=lambda s: -s.score)

    def recent_from_accounts(self, usernames: list[str], *, max_posts: int = 30, since_id: Optional[str] = None) -> list[SourceRecord]:
        """Newest posts by the approved accounts on ANY subject (watch mode scan). `since_id` skips posts
        already seen, so a quiet period costs nothing but the request."""
        records: dict[str, SourceRecord] = {}
        per_chunk = max(10, min(max_posts, 100))
        for query in account_chunks(usernames, ""):
            params: dict = {
                "query": query, "max_results": per_chunk, "sort_order": "recency",
                "tweet.fields": "created_at,author_id,lang,public_metrics", "expansions": "author_id", "user.fields": "username,name",
            }
            if since_id:
                params["since_id"] = since_id
            payload = self._get("/tweets/search/recent", params)
            self.usage.posts_read += len(payload.get("data") or []) if isinstance(payload, dict) else 0
            for r in parse_posts(payload, self._now()):
                records[r.id] = r
        newest_first = sorted(records.values(), key=lambda r: r.published_at or "", reverse=True)
        return newest_first[:max_posts]

    def search_watchlist(self, keywords: list[str], usernames: list[str], *, max_posts: int = 30) -> list[SourceRecord]:
        """Topic posts by the approved accounts; the account list is chunked to respect the query length limit."""
        records: dict[str, SourceRecord] = {}
        for query in watchlist_queries(keywords, usernames):
            for r in self.search_recent(query, max_posts=max_posts):
                records[r.id] = r
        return sorted(records.values(), key=lambda r: r.published_at or "", reverse=True)[:max_posts]

    def search_recent(self, query: str, *, max_posts: int = 30) -> list[SourceRecord]:
        """Posts from the last 7 days matching the query, newest first, at most max_posts (cost cap)."""
        max_posts = max(10, min(max_posts, 100))
        params = {
            "query": query, "max_results": max_posts, "sort_order": "recency",
            "tweet.fields": "created_at,author_id,lang,public_metrics", "expansions": "author_id", "user.fields": "username,name",
        }
        payload = self._get("/tweets/search/recent", params)
        records = parse_posts(payload, self._now())
        self.usage.posts_read += len(payload.get("data") or []) if isinstance(payload, dict) else 0
        return records


@dataclass
class AccountSuggestion:
    """An account the X agent found posting about the topic (from real posts, never invented)."""
    handle: str
    id: str
    name: str
    description: str
    verified_type: Optional[str]
    followers: Optional[int]
    posts_on_topic: int
    engagement: int
    sample_post_urls: list[str]
    score: float = 0.0
    flags: list[str] = field(default_factory=list)   # reasons for caution, shown to the owner
    role: Optional[str] = None                        # senior role found in the bio (CEO, CTO, VP, founder...)


# Words typical of stock-tip, trading-signal and parody accounts. First live discovery run (HBM, 2026-11-08)
# ranked "Seaside Trader", "ETF Tracker", "Trade Whisperer" and a "US Army" spoof account near the top, so
# these are flagged (shown to the owner, never auto-added) and pushed down the ranking.
PROMO_WORDS = ("signal", "alert", "options", "100x", "pump", "airdrop", "crypto", "forex", "discord", "telegram", "join my",
               "trader", "trading", "trade ", "trades", "stocks", "stock ", "ticker", "etf", "markets", "invest", "portfolio",
               "swing", "calls", "puts", "spoof", "parody", "fan account", "not affiliated", "memes",
               "stockpick", "picker", "giveaway", "free droid", "apk", "jester")


# Senior roles in a profile bio. A CEO/CTO/VP/founder posting about a technology is usually closer to the work than
# a commentator; matched on whole words, case-insensitive.
EXEC_ROLE_RE = re.compile(
    r"\b(ceo|cto|coo|cfo|cso|cpo|chief [a-z]+ officer|chief scientist|co-?founder|founder|president|"
    r"vice president|svp|evp|vp|head of [a-z]+|managing director|general manager|fellow)\b", re.I)


def exec_role(description: str) -> Optional[str]:
    m = EXEC_ROLE_RE.search(description or "")
    return m.group(1) if m else None


def suggestion_score(s: AccountSuggestion) -> float:
    """Transparent ranking: on-topic posts, whether X marks it as an organisation (a paid blue tick counts
    little), reach, a senior role in the bio, minus a penalty per caution flag. Endorsement by watched accounts
    (@mentions) is added later by the watchlist rules (watchlist.endorsement_bonus), from fresher data."""
    badge = {"business": 3.0, "government": 3.0, "blue": 0.5}.get(s.verified_type or "", 0.0)
    reach = math.log10(max(s.followers or 0, 1))
    role = (2.0 if (s.followers or 0) >= 5000 else 1.0) if s.role else 0.0
    return round(s.posts_on_topic * 2.0 + badge + reach + role - 4.0 * len(s.flags), 2)


MENTION_RE = re.compile(r"(?<![A-Za-z0-9_])@([A-Za-z0-9_]{1,15})\b")


def mentioned_handles(records: list[SourceRecord], watched: set[str]) -> dict[str, set[str]]:
    """{mentioned handle (lower case): {watched authors who @mentioned it}}, from posts already read (no cost).
    Self-mentions and mentions of accounts already watched are left out."""
    out: dict[str, set[str]] = {}
    for r in records:
        author = (r.authors[0] if r.authors else "").lstrip("@").lower()
        if author not in watched:
            continue
        for h in MENTION_RE.findall(r.abstract or ""):
            h = h.lower()
            if h == author or h in watched:
                continue
            out.setdefault(h, set()).add(author)
    return out


def suggestion_from_user(u: "XUser", *, reason: str, min_followers: int = 1000) -> AccountSuggestion:
    """An AccountSuggestion for a looked-up user (e.g. one that watched accounts keep mentioning)."""
    s = AccountSuggestion(handle=u.username, id=u.id, name=u.name, description=" ".join((u.description or "").split()),
                          verified_type=u.verified_type, followers=u.followers, posts_on_topic=0, engagement=0,
                          sample_post_urls=[], role=exec_role(u.description or ""))
    text = f"{s.handle} {s.name} {s.description}".lower()
    if any(w in text for w in PROMO_WORDS):
        s.flags.append("trading-tip, promotional or parody wording in the profile")
    if (s.followers or 0) < min_followers:
        s.flags.append(f"fewer than {min_followers} followers")
    if not s.description:
        s.flags.append("empty profile description")
    s.score = suggestion_score(s)
    return s


def build_topic_query(keywords: list[str]) -> str:
    """Topic posts from ANY account (for discovering who posts about it): English, no retweets/replies."""
    terms = " OR ".join(f'"{k}"' if " " in k else k for k in keywords)
    return f"({terms}) lang:en -is:retweet -is:reply"


# X rejected a 37-account query with HTTP 400 (live 2026-11-09): this access level allows about 512 characters
# per query, so account lists are split into chunks and the results merged (each request bills only the posts it returns).
MAX_QUERY_CHARS = 500
_TAIL = " -is:retweet -is:reply"


def account_chunks(usernames: list[str], prefix: str, *, max_chars: int = MAX_QUERY_CHARS) -> list[str]:
    """Queries of the form '<prefix>(from:a OR from:b)<tail>', each within the length limit, no account dropped."""
    if not usernames:
        raise SourceError(SOURCE, "watchlist is empty: no accounts approved yet")
    chunks: list[str] = []
    froms: list[str] = []
    for u in usernames:
        candidate = " OR ".join([*froms, f"from:{u}"])
        if froms and len(f"{prefix}({candidate}){_TAIL}") > max_chars:
            chunks.append(f"{prefix}({' OR '.join(froms)}){_TAIL}")
            froms = []
        froms.append(f"from:{u}")
    chunks.append(f"{prefix}({' OR '.join(froms)}){_TAIL}")
    return chunks


def build_accounts_query(usernames: list[str], *, max_chars: int = MAX_QUERY_CHARS) -> str:
    """First chunk of the no-topic account query (clients use account_chunks for all of them)."""
    return account_chunks(usernames, "", max_chars=max_chars)[0]


def watchlist_queries(keywords: list[str], usernames: list[str], *, max_chars: int = MAX_QUERY_CHARS) -> list[str]:
    """'("high bandwidth memory" OR HBM) (from:a OR from:b) -is:retweet -is:reply', chunked by account."""
    terms = " OR ".join(f'"{k}"' if " " in k else k for k in keywords)
    return account_chunks(usernames, f"({terms}) ", max_chars=max_chars)


def build_watchlist_query(keywords: list[str], usernames: list[str], *, max_chars: int = MAX_QUERY_CHARS) -> str:
    """First chunk of the topic + accounts query (kept for the record in results)."""
    return watchlist_queries(keywords, usernames, max_chars=max_chars)[0]

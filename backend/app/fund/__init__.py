"""Topic funds: one PAPER fund per research topic, split into low / medium / high risk tiers (SIMULATION).

Owner decision 2026-11-09: build stages 1-2 of an "ETF per topic" with a decision agent that decides when to invest.
  Stage 1  paper trades at real daily closes (no money moves, nothing is traded)
  Stage 2  real NEAR Intents 1Click DRY-RUN quotes for holdings that have a tokenized version (nothing is sent)
Real trades (stage 3+) need the owner's explicit go-ahead and new rules in CLAUDE.md; this module has no wallet code.

Basket (code): the latest report's companies with a ticker and a size class. Market-agent companies count when their
filings mention the topic; Company Scout candidates count unless flagged off-sector. Tiers by revenue size class
(config/funds.yaml), at most N per tier, ranked by topic mentions / next-runner score. Equal weight inside a tier.

Decision agent (code rules, every reason logged and sealed on NEAR testnet):
  target invested share = exposure_by_band[verdict band]
  score fell >= score_drop_points since the last decision -> target halved ("signal weakening")
  a tier whose priced stocks mostly carry timing risk "high" -> only stretched_stage_factor of that tier now; the rest
    waits for the next review ("staged entry")
  trades smaller than min_trade_share of the fund are skipped; every trade pays the assumed fee_pct
Trades fill at the latest available daily close on or before the decision day (no look-ahead).
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import threading
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Optional

import yaml
from pydantic import BaseModel, Field

from app.config import CONFIG_DIR
from app.fund.intents import OneClickClient, QuoteCheck, TokenRoute
from app.fund.live import LiveConfig
from app.report.verdict import build_verdict
from app.schemas.research import ResearchReport
from app.sources.base import SourceError
from app.sources.prices import CACHE_DIR as PRICE_CACHE_DIR, Bar, parse_daily

log = logging.getLogger("futurescout.fund")

DISCLAIMER = ("Simulation with pretend money at real closing prices. No money moves and nothing is traded. "
              "NEAR Intents quotes are dry runs. Not investment advice.")


# ------------------------------------------------------------------ config
class TierConfig(BaseModel):
    label: str
    weight: float
    size_classes: list[str]


class IntentsConfig(BaseModel):
    api: str = "https://1click.chaindefuser.com"
    pay_asset: str
    pay_decimals: int = 6
    quote_account: str = "intents.near"
    price_tolerance_pct: float = 15.0


class FundConfig(BaseModel):
    start_cash_usd: float = 10_000
    benchmark: str = "SPY"
    tiers: dict[str, TierConfig]
    max_holdings_per_tier: int = 4
    exposure_by_band: dict[str, float]
    score_drop_points: float = 8
    full_confidence_pct: float = 70.0     # confidence needed to invest the band's full share; below it, proportionally less
    stretched_stage_factor: float = 0.5
    min_trade_share: float = 0.02
    review_days: int = 7
    fee_pct: float = 0.30
    intents: IntentsConfig
    live: LiveConfig = LiveConfig()


def load_fund_config(path: Optional[Path] = None) -> FundConfig:
    with open(path or (CONFIG_DIR / "funds.yaml"), "r", encoding="utf-8") as fh:
        return FundConfig.model_validate(yaml.safe_load(fh))


# ------------------------------------------------------------------ state
class Holding(BaseModel):
    ticker: str
    company: str
    tier: str
    shares: float = 0.0
    cost_usd: float = 0.0
    last_close: Optional[float] = None
    last_date: Optional[str] = None
    timing_risk: Optional[str] = None
    why: str = ""
    route: Optional[TokenRoute] = None
    quote: Optional[QuoteCheck] = None

    @property
    def value_usd(self) -> float:
        return round(self.shares * (self.last_close or 0.0), 2)


class Trade(BaseModel):
    day: str
    ticker: str
    tier: str
    side: str                     # buy | sell
    shares: float
    price: float
    usd: float
    fee_usd: float


class Decision(BaseModel):
    at: datetime
    run_id: str
    report_date: str
    band: str
    score: Optional[float] = None
    previous_score: Optional[float] = None
    confidence_pct: Optional[float] = None
    target_invested_pct: float
    tier_targets_usd: dict[str, float] = Field(default_factory=dict)
    staged_tiers: list[str] = Field(default_factory=list)
    waiting_for_price: list[str] = Field(default_factory=list)   # basket companies left out: no daily close yet
    trades: list[Trade] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
    value_before_usd: float
    sha256: Optional[str] = None
    chain: Optional[dict] = None   # NEAR testnet record of the decision fingerprint


class ValuePoint(BaseModel):
    day: str
    value_usd: float
    benchmark_value_usd: Optional[float] = None


class TopicFund(BaseModel):
    kind: str = "simulation"
    topic: str
    slug: str
    sector: Optional[str] = None
    created_at: datetime
    start_cash_usd: float
    cash_usd: float
    holdings: list[Holding] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    history: list[ValuePoint] = Field(default_factory=list)
    benchmark: str = "SPY"
    benchmark_start_close: Optional[float] = None
    benchmark_start_date: Optional[str] = None
    updated_at: Optional[datetime] = None
    notes: list[str] = Field(default_factory=list)

    def value(self) -> float:
        return round(self.cash_usd + sum(h.value_usd for h in self.holdings), 2)

    def summary(self) -> dict:
        v = self.value()
        tiers: dict[str, float] = {}
        for h in self.holdings:
            tiers[h.tier] = round(tiers.get(h.tier, 0.0) + h.value_usd, 2)
        last = self.decisions[-1] if self.decisions else None
        bench = self.history[-1].benchmark_value_usd if self.history else None
        return {
            "value_usd": v, "return_pct": round((v / self.start_cash_usd - 1) * 100, 2),
            "cash_usd": round(self.cash_usd, 2), "invested_pct": round((1 - self.cash_usd / v) * 100, 1) if v else 0.0,
            "tiers_usd": tiers, "holdings": len([h for h in self.holdings if h.shares > 0]),
            "benchmark_return_pct": round((bench / self.start_cash_usd - 1) * 100, 2) if bench else None,
            "decisions": len(self.decisions), "last_band": last.band if last else None,
            "last_score": last.score if last else None, "last_decision_at": last.at.isoformat() if last else None,
            "tradable_via_intents": sum(1 for h in self.holdings if h.route and h.route.available),
        }


def slug_of(topic: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:60] or "topic"


_lock = threading.Lock()


def load_fund(path: Path) -> Optional[TopicFund]:
    if not path.is_file():
        return None
    try:
        return TopicFund.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except Exception as exc:  # noqa: BLE001
        log.warning("fund file %s unreadable (%s)", path.name, type(exc).__name__)
        return None


def save_fund(fund: TopicFund, funds_dir: Path) -> Path:
    with _lock:
        funds_dir.mkdir(parents=True, exist_ok=True)
        path = funds_dir / f"{fund.slug}.json"
        path.write_text(fund.model_dump_json(indent=2), encoding="utf-8")
        return path


def list_funds(funds_dir: Path) -> list[TopicFund]:
    out = []
    for p in sorted(funds_dir.glob("*.json")) if funds_dir.is_dir() else []:
        f = load_fund(p)
        if f:
            out.append(f)
    return out


# ------------------------------------------------------------------ prices
class PriceBook:
    """Daily closes: fresh Alpha Vantage data while the request budget lasts, else the on-disk cache (any age)."""

    def __init__(self, prices=None, *, max_requests: int = 10, cache_dir: Path = PRICE_CACHE_DIR) -> None:  # noqa: ANN001
        self.prices, self.max_requests, self.cache_dir = prices, max_requests, cache_dir
        self.requests = 0
        self.notes: list[str] = []
        self._memo: dict[str, list[Bar]] = {}

    def bars(self, ticker: str) -> list[Bar]:
        t = ticker.upper()
        if t in self._memo:
            return self._memo[t]
        bars: list[Bar] = []
        if self.prices is not None and self.requests < self.max_requests:
            before = getattr(self.prices, "requests", 0)
            try:
                bars = self.prices.daily(t)
            except SourceError as exc:
                self.notes.append(f"{t}: {exc.message[:120]}")
            self.requests += getattr(self.prices, "requests", 0) - before
        if not bars:
            path = self.cache_dir / f"{t}.json"
            if path.is_file():
                try:
                    bars = parse_daily(json.loads(path.read_text(encoding="utf-8")), t)
                except (SourceError, ValueError):
                    bars = []
        self._memo[t] = bars
        return bars

    def close_on_or_before(self, ticker: str, day: date) -> Optional[Bar]:
        found = None
        for b in self.bars(ticker):
            if b.day <= day:
                found = b
        return found


# ------------------------------------------------------------------ basket
class Candidate(BaseModel):
    ticker: str
    company: str
    tier: str
    rank: float
    why: str
    timing_risk: Optional[str] = None


def build_basket(report: ResearchReport, cfg: FundConfig) -> list[Candidate]:
    tier_of = {sc: key for key, t in cfg.tiers.items() for sc in t.size_classes}
    timing = {m.ticker.upper(): m.timing_risk for m in (report.timing.metrics if report.timing else [])}
    seen: set[str] = set()
    cands: list[Candidate] = []
    for c in (report.market.companies if report.market else []):
        size = (c.fundamentals or {}).get("size_class")
        if not c.ticker or c.filings_with_mentions <= 0 or size not in tier_of or c.ticker.upper() in seen:
            continue
        seen.add(c.ticker.upper())
        cands.append(Candidate(ticker=c.ticker.upper(), company=c.name, tier=tier_of[size], rank=float(c.filings_with_mentions) + 100,
                               why=f"{c.filings_with_mentions} SEC report(s) mention the topic; {size} by revenue",
                               timing_risk=timing.get(c.ticker.upper())))
    for c in (report.scout.candidates if report.scout else []):
        size = (c.fundamentals or {}).get("size_class")
        if not c.ticker or not c.sec_listed or c.off_sector or size not in tier_of or c.ticker.upper() in seen:
            continue
        seen.add(c.ticker.upper())
        parts = [f"{c.patents} patent(s)" if c.patents else "", f"{c.papers} paper(s)" if c.papers else "",
                 f"{c.filings} filing(s)" if c.filings else ""]
        cands.append(Candidate(ticker=c.ticker.upper(), company=c.name, tier=tier_of[size], rank=float(c.next_runner_score or 0),
                               why=f"Company Scout: {', '.join(p for p in parts if p) or 'topic activity'}; {size} by revenue",
                               timing_risk=timing.get(c.ticker.upper())))
    out: list[Candidate] = []
    for key in cfg.tiers:
        tier = sorted((c for c in cands if c.tier == key), key=lambda c: -c.rank)[: cfg.max_holdings_per_tier]
        out.extend(tier)
    return out


# ------------------------------------------------------------------ decisions
def _digest(decision: Decision) -> str:
    data = decision.model_dump(mode="json", exclude={"sha256", "chain"})
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def needs_decision(fund: Optional[TopicFund], run_id: str, now: datetime, cfg: FundConfig) -> Optional[str]:
    if fund is None or not fund.decisions:
        return "first decision for this topic"
    last = fund.decisions[-1]
    if last.run_id != run_id:
        return "a newer report is available"
    if last.staged_tiers and now - last.at >= timedelta(days=cfg.review_days):
        return f"staged entry review ({cfg.review_days} days after the last decision)"
    if last.waiting_for_price and now - last.at >= timedelta(days=1):
        return f"price review: {len(last.waiting_for_price)} company(ies) were waiting for a daily close"
    return None


def decide(fund: TopicFund, run_id: str, report: ResearchReport, book: PriceBook, cfg: FundConfig,
           now: datetime, why_now: str) -> Decision:
    """Run the decision rules for one topic and apply the paper trades to `fund` (mutates it)."""
    verdict = build_verdict(report)
    band = verdict.get("band", "insufficient") if verdict.get("available") else "insufficient"
    score = verdict.get("score")
    today = now.date()
    prev = fund.decisions[-1] if fund.decisions else None
    reasons = [f"Why now: {why_now}."]

    # value the fund at today's closes before deciding
    for h in fund.holdings:
        bar = book.close_on_or_before(h.ticker, today)
        if bar:
            h.last_close, h.last_date = bar.close, bar.day.isoformat()
    value = fund.value()

    exposure = cfg.exposure_by_band.get(band, 0.0)
    reasons.append(f"Verdict band '{band}'" + (f" (score {score})" if score is not None else "")
                   + f" -> invest {exposure:.0%} of the fund.")
    conf = verdict.get("confidence_pct")
    if conf is not None and exposure > 0:
        k = min(1.0, conf / cfg.full_confidence_pct)
        if k < 1:
            exposure *= k
            reasons.append(f"Confidence {conf:.0f}% is below the {cfg.full_confidence_pct:.0f}% needed for full size -> "
                           f"invest {k:.0%} of that: {exposure:.0%} of the fund.")
        else:
            reasons.append(f"Confidence {conf:.0f}% is at or above {cfg.full_confidence_pct:.0f}%: full size.")
    prev_score = prev.score if prev else None
    if prev_score is not None and score is not None and prev_score - score >= cfg.score_drop_points:
        exposure *= 0.5
        reasons.append(f"Score fell {prev_score - score:.1f} points since the last decision -> target halved to {exposure:.0%}.")

    basket = build_basket(report, cfg)
    priced: list[tuple[Candidate, Bar]] = []
    waiting: list[str] = []
    for c in basket:
        bar = book.close_on_or_before(c.ticker, today)
        if bar:
            priced.append((c, bar))
        else:
            waiting.append(c.ticker)
    if waiting:
        reasons.append(f"Left out for now, no daily close yet (free price plan: 25 lookups a day): {', '.join(waiting)}. "
                       "Reviewed again after the next price update.")
    tiers_present = [k for k in cfg.tiers if any(c.tier == k for c, _ in priced)]
    weight_sum = sum(cfg.tiers[k].weight for k in tiers_present)
    for k in cfg.tiers:
        if k not in tiers_present:
            reasons.append(f"No priced company in the {k}-risk tier; its share goes to the other tiers.")

    tier_targets: dict[str, float] = {}
    staged: list[str] = []
    target_by_ticker: dict[str, float] = {}
    for k in tiers_present:
        members = [(c, b) for c, b in priced if c.tier == k]
        tier_usd = value * exposure * cfg.tiers[k].weight / weight_sum if weight_sum else 0.0
        risks = [c.timing_risk for c, _ in members if c.timing_risk]
        if risks and sum(1 for r in risks if r == "high") * 2 > len(risks):
            tier_usd *= cfg.stretched_stage_factor
            staged.append(k)
            reasons.append(f"{k.capitalize()}-risk tier: most of its stocks look stretched (timing risk high) -> invest "
                           f"{cfg.stretched_stage_factor:.0%} of its target now, the rest at the next review.")
        tier_targets[k] = round(tier_usd, 2)
        for c, _ in members:
            target_by_ticker[c.ticker] = tier_usd / len(members)

    # trades: sell what left the basket or is over target, then buy what is under target
    trades: list[Trade] = []
    min_trade = cfg.min_trade_share * value
    fee = cfg.fee_pct / 100
    by_ticker = {h.ticker: h for h in fund.holdings}
    info = {c.ticker: (c, b) for c, b in priced}
    for h in list(fund.holdings):
        target = target_by_ticker.get(h.ticker, 0.0)
        bar = info[h.ticker][1] if h.ticker in info else book.close_on_or_before(h.ticker, today)
        if not bar or h.shares <= 0:
            continue
        diff = h.shares * bar.close - target
        if diff > min_trade or (target == 0 and h.shares > 0):
            shares = h.shares if target == 0 else diff / bar.close
            usd = shares * bar.close
            fund.cash_usd += usd * (1 - fee)
            h.shares -= shares
            h.cost_usd = max(0.0, h.cost_usd - usd)
            trades.append(Trade(day=bar.day.isoformat(), ticker=h.ticker, tier=h.tier, side="sell", shares=round(shares, 6),
                                price=bar.close, usd=round(usd, 2), fee_usd=round(usd * fee, 2)))
    for t, target in target_by_ticker.items():
        c, bar = info[t]
        h = by_ticker.get(t)
        have = (h.shares if h else 0.0) * bar.close
        diff = target - have
        if diff <= min_trade:
            continue
        usd = min(diff, fund.cash_usd / (1 + fee))
        if usd <= 0:
            continue
        shares = usd / bar.close
        fund.cash_usd -= usd * (1 + fee)
        if h is None:
            h = Holding(ticker=t, company=c.company, tier=c.tier)
            fund.holdings.append(h)
            by_ticker[t] = h
        h.shares += shares
        h.cost_usd += usd
        trades.append(Trade(day=bar.day.isoformat(), ticker=t, tier=c.tier, side="buy", shares=round(shares, 6),
                            price=bar.close, usd=round(usd, 2), fee_usd=round(usd * fee, 2)))
    for h in fund.holdings:
        if h.ticker in info:
            c, bar = info[h.ticker]
            h.tier, h.why, h.timing_risk = c.tier, c.why, c.timing_risk
            h.last_close, h.last_date = bar.close, bar.day.isoformat()
    fund.holdings = [h for h in fund.holdings if h.shares > 1e-9]
    fund.cash_usd = round(fund.cash_usd, 2)
    if not trades:
        reasons.append("No trade: the fund is already close to its targets.")
    reasons.append(f"Each trade pays an assumed {cfg.fee_pct}% cost; fills at the latest daily close on or before {today.isoformat()}.")

    d = Decision(at=now, run_id=run_id, report_date=report.generated_at.date().isoformat(), band=band, score=score,
                 previous_score=prev_score, confidence_pct=conf, target_invested_pct=round(exposure * 100, 1), tier_targets_usd=tier_targets,
                 staged_tiers=staged, waiting_for_price=waiting, trades=trades, reasons=reasons, value_before_usd=value)
    d.sha256 = _digest(d)
    fund.decisions.append(d)
    if fund.benchmark_start_close is None:          # the benchmark starts when the fund first decides
        bench = book.close_on_or_before(fund.benchmark, today)
        if bench:
            fund.benchmark_start_close, fund.benchmark_start_date = bench.close, bench.day.isoformat()
    return d


def mark_to_market(fund: TopicFund, book: PriceBook, now: datetime) -> None:
    today = now.date()
    for h in fund.holdings:
        bar = book.close_on_or_before(h.ticker, today)
        if bar:
            h.last_close, h.last_date = bar.close, bar.day.isoformat()
    bench_bar = book.close_on_or_before(fund.benchmark, today)
    if fund.benchmark_start_close is None and bench_bar:
        first = fund.decisions[0].trades[0].day if fund.decisions and fund.decisions[0].trades else bench_bar.day.isoformat()
        start = book.close_on_or_before(fund.benchmark, date.fromisoformat(first)) or bench_bar
        fund.benchmark_start_close, fund.benchmark_start_date = start.close, start.day.isoformat()
    bench_value = (fund.start_cash_usd * bench_bar.close / fund.benchmark_start_close
                   if bench_bar and fund.benchmark_start_close else None)
    day = max([h.last_date for h in fund.holdings if h.last_date] or [today.isoformat()])
    point = ValuePoint(day=day, value_usd=fund.value(), benchmark_value_usd=round(bench_value, 2) if bench_value else None)
    if fund.history and fund.history[-1].day == point.day:
        fund.history[-1] = point
    else:
        fund.history.append(point)
    fund.updated_at = now


def check_routes(fund: TopicFund, client: OneClickClient, cfg: FundConfig) -> dict:
    """Stage 2: is each holding tradable via NEAR Intents? If yes, a real dry-run quote for its current value."""
    stats = {"checked": 0, "available": 0, "quoted": 0, "errors": []}
    client.pay = (cfg.intents.pay_asset, cfg.intents.pay_decimals, cfg.intents.quote_account)
    for h in fund.holdings:
        try:
            h.route = client.route_for(h.ticker, h.last_close, cfg.intents.price_tolerance_pct)
        except SourceError as exc:
            stats["errors"].append(exc.message)
            break
        stats["checked"] += 1
        h.quote = None
        if h.route.available and h.route.asset_id and h.value_usd >= 1:
            h.quote = client.dry_quote(cfg.intents.pay_asset, cfg.intents.pay_decimals, h.route.asset_id,
                                       h.value_usd, cfg.intents.quote_account)
            stats["quoted"] += 1
        stats["available"] += int(h.route.available)
    return stats


def new_fund(topic: str, sector: Optional[str], cfg: FundConfig, now: datetime) -> TopicFund:
    return TopicFund(topic=topic, slug=slug_of(topic), sector=sector, created_at=now, start_cash_usd=cfg.start_cash_usd,
                     cash_usd=cfg.start_cash_usd, benchmark=cfg.benchmark,
                     notes=["Simulation: pretend money, real closing prices. No money moves; nothing is traded.",
                            "Basket and decisions are computed by code from the latest sealed report; each decision is "
                            "fingerprinted on NEAR testnet so it cannot be changed afterwards.",
                            "NEAR Intents quotes are dry runs: nothing is reserved or sent.",
                            "Not investment advice."])


def fund_payload(fund: TopicFund) -> dict:
    data = fund.model_dump(mode="json")
    for h, raw in zip(fund.holdings, data["holdings"]):
        raw["value_usd"] = h.value_usd
        raw["return_pct"] = round((h.value_usd / h.cost_usd - 1) * 100, 2) if h.cost_usd else None
    return {**data, "summary": fund.summary(), "label": "simulation", "disclaimer": DISCLAIMER}


def tradable_tokens(funds_dir: Path) -> list[dict]:
    """Allowlist for live/shadow trading: fund holdings whose tokenized version passed the symbol + price check.

    One row per ticker (from the fund with the highest report score), strongest topic first."""
    best: dict[str, dict] = {}
    for f in list_funds(funds_dir):
        last = f.decisions[-1] if f.decisions else None
        for h in f.holdings:
            if not (h.route and h.route.available and h.route.asset_id):
                continue
            row = {"ticker": h.ticker, "symbol": h.route.symbol, "asset_id": h.route.asset_id, "decimals": 18,
                   "price": h.route.token_price_usd, "topic": f.topic, "band": last.band if last else None,
                   "score": last.score if last else None, "confidence_pct": last.confidence_pct if last else None, "tier": h.tier, "why": h.why, "stretch": h.timing_risk,
                   "last_close": h.last_close, "last_close_date": h.last_date}
            if h.ticker not in best or (row["score"] or 0) > (best[h.ticker]["score"] or 0):
                best[h.ticker] = row
    return sorted(best.values(), key=lambda r: -(r["score"] or 0))

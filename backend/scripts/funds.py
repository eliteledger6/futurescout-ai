"""Topic funds (SIMULATION, stages 1-2): build/update one paper fund per topic from its latest report.

  python scripts\\funds.py                      update every topic that has a scored report
  python scripts\\funds.py --topic "AI agents"  just one topic
  python scripts\\funds.py --no-seal            do not fingerprint decisions on NEAR (SEAL_NETWORK picks testnet or mainnet)
  python scripts\\funds.py --max-price-requests 10   fresh Alpha Vantage lookups allowed (free plan: 25/day); else cache

What it does per topic: if there is a newer report (or a staged entry is due for review), the decision agent runs its
code rules and makes paper trades at real daily closes; then the fund is valued, every holding is checked against the
public NEAR Intents token list, and holdings with a tokenized version get a real 1Click DRY-RUN quote (nothing sent).
No money moves. Nothing is traded. No wallet key is used except the testnet key that writes the decision fingerprint.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.chain import NearRecorder, NearRecordError  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.fund import (PriceBook, check_routes, decide, load_fund, load_fund_config, mark_to_market,  # noqa: E402
                      needs_decision, new_fund, save_fund, slug_of)
from app.fund.intents import OneClickClient  # noqa: E402
from app.sources.prices import AlphaVantageClient  # noqa: E402

FUNDS_DIR = service.RUNS_DIR / "funds"


def latest_reports(store, only: str | None) -> list[tuple[str, object]]:  # noqa: ANN001
    seen, out = set(), []
    for row in store.list(limit=200):
        t = row["topic"].lower()
        if t in seen or row.get("score") is None or (only and t != only.lower()):
            continue
        found = store.get(row["id"])
        if found:
            seen.add(t)
            out.append((row["id"], found[0]))
    return out


def intents_price_fallback(cfg):  # noqa: ANN001,ANN201
    """When no daily close is available: the NEAR Intents price of the Ondo tokenized stock (<TICKER>on), labelled as such."""
    from app.fund.intents_signed import SignedIntents
    from app.sources.prices import Bar
    cache: dict = {}

    def fallback(ticker: str):  # noqa: ANN202
        if "list" not in cache:
            cache["list"] = {str(t.get("symbol", "")).upper(): t for t in SignedIntents(cfg.intents.api).tokens()}
        t = cache["list"].get(f"{ticker.upper()}ON")
        if not t or not t.get("price"):
            return None
        when = datetime.fromisoformat(str(t.get("priceUpdatedAt") or datetime.now(timezone.utc).isoformat()).replace("Z", "+00:00"))
        px = float(t["price"])
        return Bar(day=when.date(), close=px, high=px, low=px, volume=0, source=f"NEAR Intents price of {t['symbol']}")
    return fallback


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic")
    ap.add_argument("--no-seal", action="store_true")
    ap.add_argument("--max-price-requests", type=int, default=10)
    ap.add_argument("--seal-missing", action="store_true", help="only fingerprint decisions that are not sealed yet")
    ap.add_argument("--redecide", help="force a new decision for every fund, with this reason (e.g. after a scoring-method change)")
    ap.add_argument("--out-dir", help="write funds here instead of runs/funds (for a trial run)")
    args = ap.parse_args()
    funds_dir = Path(args.out_dir) if args.out_dir else FUNDS_DIR
    s = get_settings()
    cfg = load_fund_config()
    prices = AlphaVantageClient(s.alpha_vantage_key_value()) if s.alpha_vantage_key_value() else None
    book = PriceBook(prices, max_requests=args.max_price_requests, fallback=intents_price_fallback(cfg))
    intents = OneClickClient(cfg.intents.api)
    from app.chain.near_record import make_recorder
    # only reports are sealed by default (owner 2026-11-11); SEAL_FUND_DECISIONS=true or --seal-missing seals decisions
    recorder = make_recorder(s) if (args.seal_missing or (s.seal_fund_decisions and not args.no_seal)) else None
    now = datetime.now(timezone.utc)

    if args.seal_missing:
        from app.fund import list_funds
        if not recorder:
            print("no testnet credentials")
            return 1
        for fund in list_funds(funds_dir):
            for n, d in enumerate(fund.decisions, start=1):
                if d.chain or not d.sha256:
                    continue
                try:
                    d.chain = recorder.record_fund_decision(f"fund_{fund.slug}_{n}", {"sha256": d.sha256, "topic": fund.topic[:120],
                                                            "run_id": d.run_id, "at": d.at.isoformat(), "band": d.band}).as_dict()
                    print(f"{fund.topic}: decision {n} sealed")
                    time.sleep(8)   # the public testnet RPC rate-limits bursts (HTTP 429)
                except NearRecordError as exc:
                    print(f"{fund.topic}: decision {n} NOT sealed ({str(exc)[:100]})")
            save_fund(fund, funds_dir)
        return 0

    reports = latest_reports(_default_store(s), args.topic)
    print(f"{len(reports)} topic(s) with a scored report")
    for run_id, report in reports:
        path = funds_dir / f"{slug_of(report.topic)}.json"
        fund = load_fund(path)
        why = args.redecide or needs_decision(fund, run_id, now, cfg)
        if fund is None:
            fund = new_fund(report.topic, report.sector, cfg, now)
        if why:
            d = decide(fund, run_id, report, book, cfg, now, why)
            line = f"{report.topic}: {d.band} (score {d.score}) -> invest {d.target_invested_pct:.0f}%; {len(d.trades)} paper trade(s)"
            if recorder:
                try:
                    rec = recorder.record_fund_decision(f"fund_{fund.slug}_{len(fund.decisions)}",
                                                        {"sha256": d.sha256, "topic": report.topic[:120], "run_id": run_id,
                                                         "at": d.at.isoformat(), "band": d.band})
                    d.chain = rec.as_dict()
                    line += "; sealed on NEAR testnet"
                    time.sleep(6)          # the public testnet RPC rate-limits bursts
                except NearRecordError as exc:
                    line += f"; NOT sealed ({str(exc)[:120]})"
            print(line)
        else:
            print(f"{report.topic}: no new report and no review due; revalued only")
        mark_to_market(fund, book, now)
        stats = check_routes(fund, intents, cfg)
        print(f"   value ${fund.value():,.2f} ({fund.summary()['return_pct']:+.2f}%), {len(fund.holdings)} holdings; "
              f"NEAR Intents: {stats['available']}/{stats['checked']} tradable, {stats['quoted']} dry quote(s)"
              + (f"; errors: {stats['errors'][:1]}" if stats["errors"] else ""))
        save_fund(fund, funds_dir)
    if book.notes:
        print("price notes:", "; ".join(book.notes[:6]))
    print(f"Alpha Vantage requests: {book.requests}; 1Click requests: {intents.requests}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

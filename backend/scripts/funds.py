"""Topic funds (SIMULATION, stages 1-2): build/update one paper fund per topic from its latest report.

  python scripts\\funds.py                      update every topic that has a scored report
  python scripts\\funds.py --topic "AI agents"  just one topic
  python scripts\\funds.py --no-seal            do not fingerprint decisions on NEAR testnet (~0.15 testnet NEAR each)
  python scripts\\funds.py --max-price-requests 10   fresh Alpha Vantage lookups allowed (free plan: 25/day); else cache

What it does per topic: if there is a newer report (or a staged entry is due for review), the decision agent runs its
code rules and makes paper trades at real daily closes; then the fund is valued, every holding is checked against the
public NEAR Intents token list, and holdings with a tokenized version get a real 1Click DRY-RUN quote (nothing sent).
No money moves. Nothing is traded. No wallet key is used except the testnet key that writes the decision fingerprint.
"""

from __future__ import annotations

import argparse
import sys
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic")
    ap.add_argument("--no-seal", action="store_true")
    ap.add_argument("--max-price-requests", type=int, default=10)
    ap.add_argument("--out-dir", help="write funds here instead of runs/funds (for a trial run)")
    args = ap.parse_args()
    funds_dir = Path(args.out_dir) if args.out_dir else FUNDS_DIR
    s = get_settings()
    cfg = load_fund_config()
    prices = AlphaVantageClient(s.alpha_vantage_key_value()) if s.alpha_vantage_key_value() else None
    book = PriceBook(prices, max_requests=args.max_price_requests)
    intents = OneClickClient(cfg.intents.api)
    creds = None if args.no_seal else s.near_testnet_credentials()
    recorder = NearRecorder(*creds) if creds else None
    now = datetime.now(timezone.utc)

    reports = latest_reports(_default_store(s), args.topic)
    print(f"{len(reports)} topic(s) with a scored report")
    for run_id, report in reports:
        path = funds_dir / f"{slug_of(report.topic)}.json"
        fund = load_fund(path)
        why = needs_decision(fund, run_id, now, cfg)
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

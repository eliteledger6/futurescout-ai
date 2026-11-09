"""Paper portfolio (SIMULATION): sync positions from the saved reports and refresh prices.

  python scripts\\portfolio.py                 sync positions from saved reports, then update prices (needs ALPHA_VANTAGE_API_KEY)
  python scripts\\portfolio.py --no-prices     sync only (no network)
  python scripts\\portfolio.py --max-requests 10

No money moves. Positions = top Company Scout candidates of each report, "bought" at the first close on/after the
report date with a fixed pretend notional. Output: backend/runs/portfolio.json (served by GET /api/portfolio).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.portfolio import load_portfolio, portfolio_payload, save_portfolio, sync_from_store, update_prices  # noqa: E402
from app.sources.prices import AlphaVantageClient  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-prices", action="store_true")
    ap.add_argument("--max-requests", type=int, default=None)
    args = ap.parse_args()
    settings = get_settings()
    path = service.RUNS_DIR / "portfolio.json"
    pf = load_portfolio(path, notional=settings.portfolio_notional_usd, per_report=settings.portfolio_positions_per_report)
    added = sync_from_store(pf, _default_store(settings))
    print(f"positions: {len(pf.positions)} ({added} new from saved reports)")
    if not args.no_prices:
        key = settings.alpha_vantage_key_value()
        if not key:
            print("ALPHA_VANTAGE_API_KEY is not set: positions stay 'pending' (free key: https://www.alphavantage.co/support/#api-key)")
        else:
            out = update_prices(pf, AlphaVantageClient(key), max_requests=args.max_requests or settings.portfolio_max_price_requests,
                                benchmark=settings.portfolio_benchmark)
            print(f"prices: {out['priced']} positions priced, {out['requests']} requests, {out['cache_hits']} cache hits")
            for e in out["errors"]:
                print(f"  {e}")
    save_portfolio(pf, path)
    s = portfolio_payload(pf, prices_configured=True)["summary"]
    print(f"SIMULATION: {s['open']} open / {s['pending']} pending; invested ${s['invested_usd']:,.0f} -> value ${s['value_usd']:,.0f} "
          f"({s['return_pct'] if s['return_pct'] is not None else 'n/a'}%); benchmark {s['benchmark_return_pct'] if s['benchmark_return_pct'] is not None else 'n/a'}%")
    print(f"saved {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

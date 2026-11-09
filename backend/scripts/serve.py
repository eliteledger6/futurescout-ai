"""Start the FUTURESCOUT AI API for the dashboard (local only).

  python scripts\\serve.py            then open http://127.0.0.1:8000/docs to try the API

Reads saved reports from PostgreSQL (DATABASE_URL) or, without a database, from backend/runs/.
Starting new runs from the dashboard needs ENABLE_RUN_API=true in .env (each run costs ~$0.17).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import uvicorn  # noqa: E402

from app.api import create_app  # noqa: E402
from app.config import get_settings, quiet_network_logs  # noqa: E402


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1", help="127.0.0.1 = this computer only (default); 0.0.0.0 = reachable from the network / a container")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
    quiet_network_logs()
    settings = get_settings()
    app = create_app(settings)
    print(f"FUTURESCOUT AI API on http://{args.host}:{args.port}  (API docs: http://{args.host}:{args.port}/docs)")
    print(f"New runs from the dashboard: {'ENABLED' if settings.enable_run_api else 'off (set ENABLE_RUN_API=true in .env)'}")
    print(f"Report market: {'ENABLED, seller ' + settings.near_testnet_account_id if settings.near_testnet_account_id else 'off (set NEAR_TESTNET_ACCOUNT_ID)'}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())

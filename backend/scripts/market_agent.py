"""The report agent on NEAR Agent Market (market.near.ai): take paid research jobs and deliver sealed reports.

  python scripts\\market_agent.py            run forever: check for jobs every minute (Ctrl+C stops)
  python scripts\\market_agent.py --once     one pass, then stop
  python scripts\\market_agent.py --status   what the agent has done (read-only, no token needed)

Needs AGENT_MARKET_TOKEN in .env (the `aat_...` token from the agent's listing page on market.near.ai; the owner makes
it). A brief is used only as a short topic name, never as instructions. A recent sealed report on the same topic is
delivered at no AI cost; otherwise the research team runs once (at most agent_market.new_runs_per_day new runs a day,
config/funds.yaml). Payment is held by the marketplace and released when the buyer accepts; withdrawals are made by the
owner on the website. Docs: https://docs.market.near.ai/list-your-agent.md
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.agent_market import AgentMarketClient, MarketConfig, handle, load_state, resume_stale, save_state  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.report import render_markdown  # noqa: E402

STATE = service.RUNS_DIR / "agent_market" / "state.json"


def market_config() -> MarketConfig:
    import yaml
    from app.config import CONFIG_DIR
    raw = yaml.safe_load((CONFIG_DIR / "funds.yaml").read_text(encoding="utf-8")) or {}
    return MarketConfig(**(raw.get("agent_market") or {}))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()
    s, cfg = get_settings(), market_config()
    state = load_state(STATE)
    if args.status:
        if not state.jobs:
            print("no Agent Market job yet")
        for j in sorted(state.jobs.values(), key=lambda x: x.at):
            print(f"{j.at:%m-%d %H:%M} {j.assignment_id[:12]:12} {j.status:9} {j.source:8} {j.topic[:40]:40} {j.note[:60]}")
        return 0
    if not s.agent_market_token:
        print("AGENT_MARKET_TOKEN is not set in .env: make the token on the agent's listing page at market.near.ai")
        return 1
    client = AgentMarketClient(s.agent_market_token.get_secret_value().strip(), cfg.base_url)
    store = _default_store(s)

    def recent() -> list[dict]:
        return store.list(limit=200)

    def load_report(run_id: str):  # noqa: ANN202
        found = store.get(run_id)
        if not found:
            return None
        report, md = found
        return md or render_markdown(report), (report.chain_record or {}).get("explorer_url")

    def run_research(topic: str):  # noqa: ANN202
        out = service.execute(topic, s, warn=lambda m: print("   ", m[:160]))
        return out.run_id or out.json_path.stem, out.markdown, (out.report.chain_record or {}).get("explorer_url")

    print(f"report agent on NEAR Agent Market: checking for jobs every {cfg.poll_seconds}s; "
          f"at most {cfg.new_runs_per_day} new research runs a day. Ctrl+C stops.")
    while True:
        now = datetime.now(timezone.utc)
        if resume_stale(state, timedelta(hours=1), now):
            save_state(state, STATE)
        try:
            rows = client.assignments()
        except Exception as exc:  # noqa: BLE001
            print(f"[{now:%H:%M}] could not reach the marketplace: {str(exc)[:160]}")
            rows = []
        for row in rows:
            handle(row, client=client, state=state, state_path=STATE, cfg=cfg, recent=recent, load_report=load_report,
                   run_research=run_research, now=datetime.now(timezone.utc), site_url=s.public_site_url)
        if args.once:
            return 0
        time.sleep(max(30, cfg.poll_seconds))


if __name__ == "__main__":
    sys.exit(main())

"""The report agent on NEAR Agent Market (market.near.ai): take paid research jobs and deliver sealed reports.

  python scripts\\market_agent.py            run forever: check for jobs every minute (Ctrl+C stops)
  python scripts\\market_agent.py --once     one pass, then stop
  python scripts\\market_agent.py --status   what the agent has done (read-only, no token needed)
  python scripts\\market_agent.py --publish  also put every new report on the hosted website: export the snapshot,
                                             commit backend/site_data and git push (the owner's choice; off by default)

It also works the website's TOPIC PROPOSALS (owner 2026-11-11): visitors propose a topic for free, at most
proposals.per_day a day; an AI reviewer (agent topic_review) decides whether it is worth a research run; approved topics
are researched, sealed on NEAR and listed on the site. Proposals made on the hosted site are collected when
PUBLIC_API_URL and PROPOSALS_TOKEN are set in .env (the same token is set on the hosted API).

Needs AGENT_MARKET_TOKEN in .env (the `aat_...` token from the agent's listing page on market.near.ai; the owner makes
it). A brief is used only as a short topic name, never as instructions. A recent sealed report on the same topic is
delivered at no AI cost; otherwise the research team runs once (at most agent_market.new_runs_per_day new runs a day,
config/funds.yaml). Payment is held by the marketplace and released when the buyer accepts; withdrawals are made by the
owner on the website. Docs: https://docs.market.near.ai/list-your-agent.md
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import proposals, service  # noqa: E402
from app.paper_fund_hook import build_paper_fund, funds_due, update_all_funds  # noqa: E402
from app.agents.science import topic_scout  # noqa: E402
from app.radar import load_sectors, load_topics  # noqa: E402
from app.radar_refresh import RadarRefresh  # noqa: E402
from app.sources.openalex import OpenAlexClient  # noqa: E402
from app.watch import add_topics  # noqa: E402
from app.agent_market import AgentMarketClient, MarketConfig, handle, load_state, resume_stale, save_state  # noqa: E402
from app.api.main import _default_store  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.models.config import load_model_config  # noqa: E402
from app.models.router import ModelRouter  # noqa: E402
from app.report import render_markdown  # noqa: E402

STATE = service.RUNS_DIR / "agent_market" / "state.json"
PROPOSALS = service.RUNS_DIR / "proposals" / "state.json"
SCOUT = service.RUNS_DIR / "topic_scout.json"                              # what the Science agent read and decided while idle
HOUSEKEEPING = service.RUNS_DIR / "agent_market" / "housekeeping.json"     # when the daily paper-fund update last ran
REPO = Path(__file__).resolve().parents[2]


def publish() -> None:
    """Put new reports on the hosted website (only with --publish: pushing is the owner's decision)."""
    from app.site_publish import publish as site_publish
    site_publish("Site data update (new report from the report agent)")


def market_config() -> MarketConfig:
    import yaml
    from app.config import CONFIG_DIR
    raw = yaml.safe_load((CONFIG_DIR / "funds.yaml").read_text(encoding="utf-8")) or {}
    return MarketConfig(**(raw.get("agent_market") or {}))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--publish", action="store_true", help="export, commit and git push backend/site_data after every new report")
    args = ap.parse_args()
    s, cfg = get_settings(), market_config()
    state = load_state(STATE)
    if args.status:
        if not state.jobs:
            print("no Agent Market job yet")
        for j in sorted(state.jobs.values(), key=lambda x: x.at):
            print(f"{j.at:%m-%d %H:%M} {j.assignment_id[:12]:12} {j.status:9} {j.source:8} {j.topic[:40]:40} {j.note[:60]}")
        for p in sorted(proposals.load_state(PROPOSALS).proposals, key=lambda x: x.created_at):
            print(f"{p.created_at:%m-%d %H:%M} proposal     {p.status:9} {'':8} {p.topic[:40]:40} {p.reason[:60]}")
        return 0
    client = AgentMarketClient(s.agent_market_token.get_secret_value().strip(), cfg.base_url) if s.agent_market_token else None
    if client is None:
        print("AGENT_MARKET_TOKEN is not set in .env: Agent Market jobs are skipped (topic proposals still run)")
    pcfg = proposals.load_config()
    remote = None
    if s.public_api_url and s.proposals_token:
        remote = proposals.RemoteProposals(s.public_api_url, s.proposals_token.get_secret_value().strip())
    router = ModelRouter(load_model_config(), s)
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
        build_paper_fund(out.report.topic)               # every new report gets its paper fund (owner 2026-11-11)
        return out.run_id or out.json_path.stem, out.markdown, (out.report.chain_record or {}).get("explorer_url")

    print(f"report agent: checking for Agent Market jobs and topic proposals every {cfg.poll_seconds}s; at most "
          f"{cfg.new_runs_per_day} Agent Market runs and {pcfg.per_day} proposal runs a day. "
          f"Hosted proposals: {'collected from ' + s.public_api_url if remote else 'off (PUBLIC_API_URL / PROPOSALS_TOKEN not set)'}. "
          f"Publishing: {'on' if args.publish else 'off (--publish)'}. "
          f"Radar refresh: {'every %g h' % cfg.radar_refresh_hours if cfg.radar_refresh_hours > 0 else 'off'}. "
          f"Idle scouting by the Science agent: {'every %g h, %d papers' % (cfg.topic_scout_hours, cfg.topic_scout_papers) if cfg.topic_scout_hours > 0 else 'off'}. Ctrl+C stops.")
    radar = RadarRefresh(service.RUNS_DIR, service.BACKEND_DIR / "site_data")
    while True:
        now = datetime.now(timezone.utc)
        if resume_stale(state, timedelta(hours=1), now):
            save_state(state, STATE)
        new_reports = 0
        try:
            rows = client.assignments() if client else []
        except Exception as exc:  # noqa: BLE001
            print(f"[{now:%H:%M}] could not reach the marketplace: {str(exc)[:160]}")
            rows = []
        for row in rows:
            rec = handle(row, client=client, state=state, state_path=STATE, cfg=cfg, recent=recent, load_report=load_report,
                         run_research=run_research, now=datetime.now(timezone.utc), site_url=s.public_site_url)
            new_reports += 1 if rec and rec.status == "submitted" and rec.source == "new_run" else 0

        # ---- topic proposals from the website -----------------------------------------------------------------
        if pcfg.enabled:
            def tell(p):  # noqa: ANN001, ANN202
                if remote:
                    try:
                        remote.sync([{"id": p.id, "status": p.status, "reason": p.reason, "run_id": p.run_id}])
                    except Exception as exc:  # noqa: BLE001
                        print(f"  could not update the hosted site: {str(exc)[:120]}")
            if remote:
                try:
                    got = proposals.pull_remote(PROPOSALS, remote.sync([]))
                    if got:
                        print(f"[{now:%H:%M}] {got} new topic proposal(s) from the hosted site")
                except Exception as exc:  # noqa: BLE001
                    print(f"[{now:%H:%M}] could not reach the hosted site for proposals: {str(exc)[:120]}")
            changed = proposals.work(path=PROPOSALS, cfg=pcfg, reviewer=lambda t: proposals.review(router, t), recent=recent,
                                     run_research=run_research, now=lambda: datetime.now(timezone.utc), report=tell)
            new_reports += sum(1 for p in changed if p.status == "done")
        # ---- once a day (and right after the agent starts): every paper fund is created or updated ---------------
        funds_changed = False
        try:
            hk = json.loads(HOUSEKEEPING.read_text(encoding="utf-8")) if HOUSEKEEPING.is_file() else {}
        except ValueError:
            hk = {}
        if funds_due(hk.get("funds_at"), datetime.now(timezone.utc)):
            print(f"[{datetime.now(timezone.utc):%H:%M}] daily paper-fund update (new topics get their fund; others are reviewed or revalued)")
            funds_changed = update_all_funds()
            hk["funds_at"] = datetime.now(timezone.utc).isoformat()      # tried today: a failure is retried tomorrow, not every minute
            HOUSEKEEPING.parent.mkdir(parents=True, exist_ok=True)
            HOUSEKEEPING.write_text(json.dumps(hk), encoding="utf-8")
        # ---- no job this round: the Science agent reads a few recent papers and may add one new radar topic --------
        topics_changed = False
        if (cfg.topic_scout_hours > 0 and not args.once and not rows and not new_reports and s.openalex_key_value()
                and funds_due(hk.get("scout_at"), datetime.now(timezone.utc), cfg.topic_scout_hours)):
            try:
                added = topic_scout.scout_once(
                    router=router, openalex=OpenAlexClient(s.openalex_key_value()), sectors=load_sectors(), known=load_topics(),
                    state_path=SCOUT, n_papers=cfg.topic_scout_papers, max_new_per_day=cfg.topic_scout_max_per_day,
                    add_topic=lambda t: bool(add_topics([t], found_by=topic_scout.FOUND_BY)))
                topics_changed = bool(added)
            except Exception as exc:  # noqa: BLE001  (scouting must never stop the loop)
                print(f"  science agent (idle scouting) failed: {str(exc)[:160]}")
            hk["scout_at"] = datetime.now(timezone.utc).isoformat()
            HOUSEKEEPING.parent.mkdir(parents=True, exist_ok=True)
            HOUSEKEEPING.write_text(json.dumps(hk), encoding="utf-8")
        # ---- the Hot-Topic Radar is recounted in the background (it takes over an hour), then published ----------
        radar_changed = radar.finished() is True
        if (cfg.radar_refresh_hours > 0 and not args.once and not radar.running
                and funds_due(hk.get("radar_at"), datetime.now(timezone.utc), cfg.radar_refresh_hours)):
            print(f"[{datetime.now(timezone.utc):%H:%M}] radar refresh is due")
            radar.start()
            hk["radar_at"] = datetime.now(timezone.utc).isoformat()      # tried now: a failure is retried at the next interval
            HOUSEKEEPING.parent.mkdir(parents=True, exist_ok=True)
            HOUSEKEEPING.write_text(json.dumps(hk), encoding="utf-8")
        if (new_reports or funds_changed or radar_changed or topics_changed) and args.publish:
            publish()
        if args.once:
            return 0
        time.sleep(max(30, cfg.poll_seconds))


if __name__ == "__main__":
    sys.exit(main())

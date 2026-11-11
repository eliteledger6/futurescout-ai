"""Pre-flight check: is everything in place to run the agents here (the owner's computer or the cloud server)?

  python scripts\\preflight.py            report agent + trading agent
  python scripts\\preflight.py --no-trading   only what the report agent needs

Read-only: nothing is signed, paid or changed. It never prints a key or a token, only whether each one is set.
It checks the settings in .env, the data the agents start from, that NEAR AI Cloud and the hosted site answer, and that
this machine may push to the repository (needed for publishing new reports and trades to the website).
Exit code 0 when nothing required is missing.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import service  # noqa: E402
from app.config import get_settings  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
OK, BAD, NOTE = "  ok   ", "  MISSING", "  note "


def has(value) -> bool:  # noqa: ANN001
    if value is None:
        return False
    try:
        value = value.get_secret_value()
    except AttributeError:
        pass
    return bool(str(value).strip())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-trading", action="store_true", help="skip what only the trading agent needs")
    args = ap.parse_args()
    s = get_settings()
    missing = 0

    def line(ok: bool, what: str, why: str = "", required: bool = True) -> None:
        nonlocal missing
        if ok:
            print(f"{OK} {what}")
        elif required:
            missing += 1
            print(f"{BAD} {what}" + (f"  ->  {why}" if why else ""))
        else:
            print(f"{NOTE} {what}" + (f"  ({why})" if why else ""))

    print(f"Python {sys.version.split()[0]} in {REPO}")
    print("\nSettings in .env (shown as set / missing, never the value)")
    for name, why in (("near_ai_api_key", "every agent's model calls"), ("openalex_api_key", "research papers"),
                      ("edgar_user_agent", "SEC filings")):
        line(has(getattr(s, name, None)), name.upper(), why)
    for name, why in (("x_bearer_token", "X signals are skipped without it"), ("serpapi_api_key", "patent search (or the EPO keys)"),
                      ("alpha_vantage_api_key", "price and timing check, paper funds use cached prices without it")):
        line(has(getattr(s, name, None)), name.upper(), why, required=False)
    line(s.report_agent_credentials() is not None, "REPORT_AGENT_ACCOUNT_ID + REPORT_AGENT_PRIVATE_KEY", "sealing on NEAR mainnet, staking")
    line((s.seal_network or "").lower() == "mainnet", "SEAL_NETWORK=mainnet", "seals would go to testnet", required=False)
    line(has(s.agent_market_token), "AGENT_MARKET_TOKEN", "NEAR Agent Market jobs are skipped without it", required=False)
    line(has(s.proposals_token) and has(s.public_api_url), "PROPOSALS_TOKEN + PUBLIC_API_URL",
         "topic proposals from the hosted site are not collected without them", required=False)
    if not args.no_trading:
        line(s.fund_mainnet_credentials() is not None, "FUND_MAINNET_ACCOUNT_ID + FUND_MAINNET_PRIVATE_KEY", "the trading agent cannot sign")
        line(has(getattr(s, "oneclick_api_key", None)), "ONECLICK_API_KEY", "paying reports and trading from the near.com balance")

    print("\nData the agents start from")
    reports = len(list(service.RUNS_DIR.glob("report_*.json")))
    db = bool(s.database_url_value())
    line(reports > 0 or db, f"reports in {service.RUNS_DIR.name}/ ({reports} files" + (", plus the database" if db else "") + ")",
         "copy backend/site_data into backend/runs (the setup script does this)")
    funds = len(list((service.RUNS_DIR / "funds").glob("*.json")))
    line(funds > 0, f"paper funds ({funds})", "they are built by the report agent's first daily update", required=False)
    line((service.RUNS_DIR / "trading" / "state.json").is_file(), "trading record", "starts empty", required=False)
    line(not (service.RUNS_DIR / "trading" / "STOP").exists(), "kill switch is off", "trading is paused: scripts/fund_trade.py start", required=False)

    print("\nConnections (read-only)")
    try:
        import httpx
        r = httpx.get(s.near_ai_base_url.rstrip("/") + "/models", headers={"Authorization": f"Bearer {s.require_near_key()}"}, timeout=30)
        line(r.status_code == 200, "NEAR AI Cloud answers with this key", f"HTTP {r.status_code}")
    except Exception as exc:  # noqa: BLE001
        line(False, "NEAR AI Cloud answers with this key", type(exc).__name__)
    if has(s.proposals_token) and has(s.public_api_url):
        try:
            from app.proposals import RemoteProposals
            n = len(RemoteProposals(s.public_api_url, s.proposals_token.get_secret_value().strip()).sync([]))
            line(True, f"hosted site accepts the proposals secret ({n} proposal(s) on record)")
        except Exception as exc:  # noqa: BLE001
            line(False, "hosted site accepts the proposals secret", str(exc)[:80])
    try:
        r = subprocess.run(["git", "push", "--dry-run", "-q"], cwd=str(REPO), capture_output=True, text=True, timeout=60)
        line(r.returncode == 0, "this machine may push to the repository (publishing)", (r.stderr or r.stdout).strip()[-120:])
    except Exception as exc:  # noqa: BLE001
        line(False, "this machine may push to the repository (publishing)", type(exc).__name__)

    print(f"\n{'READY: nothing required is missing.' if not missing else f'NOT READY: {missing} required item(s) missing (see MISSING above).'}")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())

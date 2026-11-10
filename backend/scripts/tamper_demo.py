"""Tamper demo: show that a sealed report cannot be edited quietly.

  python scripts\\tamper_demo.py                 use the newest sealed report
  python scripts\\tamper_demo.py --run <id>      a specific run

1. Loads the report and recomputes its SHA-256 fingerprint.
2. Reads the fingerprint FUTURESCOUT recorded on NEAR, on the record's own network (free RPC read, no key).
3. Shows MATCH.
4. Changes ONE word of the summary in memory (nothing is saved), recomputes, and shows MISMATCH.

Nothing is written anywhere: not to disk, not to the database, not to the chain.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402

from app.api.main import _default_store  # noqa: E402
from app.chain.near_record import MAINNET_RPC, SOCIALDB_TESTNET, TESTNET_RPC, NearRecordError, network_of, read_record, verify  # noqa: E402
from app.config import get_settings  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run")
    args = ap.parse_args()
    store = _default_store(get_settings())
    run_id = args.run
    if not run_id:
        for row in store.list(limit=50):
            found = store.get(row["id"])
            if found and found[0].chain_record:
                run_id = row["id"]
                break
    if not run_id:
        print("no sealed report found")
        return 1
    found = store.get(run_id)
    if not found:
        print(f"run {run_id} not found")
        return 1
    report, _ = found
    rec = report.chain_record
    if not rec:
        print(f"{run_id} has no NEAR record")
        return 1
    print(f"Report: {report.topic}  ({run_id})")
    contract = rec.get("contract", SOCIALDB_TESTNET)
    net = rec.get("network") or network_of(contract)
    print(f"Recorded on NEAR {net} by {rec['account']} in {contract}")
    print(f"  tx: {rec.get('explorer_url')}")
    try:
        onchain = read_record(httpx.Client(timeout=30.0), TESTNET_RPC if net == "testnet" else MAINNET_RPC, contract, rec["account"], rec["key"])
    except NearRecordError as exc:
        print(f"could not read NEAR {net}: {exc}")
        return 1
    v = verify(report, onchain)
    print(f"\n1) Stored report, as saved:\n   computed  {v['sha256']}\n   on chain  {v.get('onchain_sha256')}\n   -> {v['status']}")

    draft = report.investment.draft if report.investment else None
    if draft:
        words = draft.summary.split()
        for i, w in enumerate(words):
            if w.lower() in ("not", "no", "limited", "early", "uncertain", "low"):
                words[i] = "strongly"
                break
        else:
            words.append("(edited)")
        draft.summary = " ".join(words)
        what = "one word of the summary"
    else:
        report.topic = report.topic + " (edited)"
        what = "the topic"
    v2 = verify(report, onchain)
    print(f"\n2) Same report after changing {what} in memory (nothing saved):\n   computed  {v2['sha256']}\n   on chain  {v2.get('onchain_sha256')}\n   -> {v2['status']}")
    print(f"\nThe dashboard badge repeats check 1 on every page load (digest {v['sha256'][:16]}…).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

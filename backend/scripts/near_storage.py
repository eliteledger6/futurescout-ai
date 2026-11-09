"""Show, and optionally withdraw, the testnet account's prepaid SocialDB storage (TESTNET ONLY).

  python scripts\\near_storage.py                       show used/free bytes and the account balance
  python scripts\\near_storage.py --withdraw --keep 60000   return the deposit above 60,000 free bytes to the account

Each seal used to attach a 0.1 NEAR storage deposit; what a record does not use stays in SocialDB as prepaid storage.
SocialDB's storage_withdraw returns that unused deposit (1 yoctoNEAR attached, as the contract requires).
60,000 free bytes is room for well over 100 more seals. Mainnet is refused by NearRecorder.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.chain import NearRecorder, NearRecordError  # noqa: E402
from app.chain.near_record import SOCIALDB_TESTNET, TESTNET_RPC  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.chain.near_record import read_balance  # noqa: E402

YOCTO_PER_BYTE = 10**19   # NEAR storage price: 1 NEAR per 100 kB


def storage(http: httpx.Client, account: str) -> dict:
    args = base64.b64encode(json.dumps({"account_id": account}).encode()).decode()
    body = {"jsonrpc": "2.0", "id": "fs", "method": "query",
            "params": {"request_type": "call_function", "finality": "final", "account_id": SOCIALDB_TESTNET,
                       "method_name": "get_account_storage", "args_base64": args}}
    return json.loads(bytes(http.post(TESTNET_RPC, json=body).json()["result"]["result"]).decode() or "{}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--withdraw", action="store_true")
    ap.add_argument("--keep", type=int, default=60_000, help="free bytes to keep prepaid")
    args = ap.parse_args()
    creds = get_settings().near_testnet_credentials()
    if not creds:
        print("NEAR_TESTNET_ACCOUNT_ID / NEAR_TESTNET_PRIVATE_KEY not set")
        return 1
    http = httpx.Client(timeout=30)
    st = storage(http, creds[0])
    print(f"SocialDB storage: used {st.get('used_bytes')} bytes, free {st.get('available_bytes')} bytes; "
          f"account balance {read_balance(http, TESTNET_RPC, creds[0])['available_near']} NEAR")
    if not args.withdraw:
        return 0
    extra = int(st.get("available_bytes", 0)) - args.keep
    if extra <= 0:
        print("nothing to withdraw")
        return 0
    amount = extra * YOCTO_PER_BYTE
    import app.chain.near_record as nr
    nr.GAS = 10 * 10**12      # a withdraw needs far less than the 50 TGas a SocialDB write reserves (gas is reserved up front)
    rec = NearRecorder(*creds)
    try:
        rec._signer("storage_withdraw", {"amount": str(amount)}, 1)
    except NearRecordError as exc:
        print(f"withdraw failed: {exc}")
        return 1
    print(f"withdrew {amount / 10**24:.3f} NEAR of unused storage deposit")
    st = storage(http, creds[0])
    print(f"now: free {st.get('available_bytes')} bytes; account balance {read_balance(http, TESTNET_RPC, creds[0])['available_near']} NEAR")
    return 0


if __name__ == "__main__":
    sys.exit(main())

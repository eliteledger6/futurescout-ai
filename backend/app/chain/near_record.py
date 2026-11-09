"""Tamper-evident record of each research report on NEAR TESTNET.

What it does: computes a SHA-256 fingerprint of the finished report and stores it, with the topic
and time, in SocialDB on testnet (contract v1.social08.testnet, same code as social.near on mainnet;
checked live 2026-11-08). Anyone can later recompute the fingerprint of a report and compare it with
the on-chain value: if one character of the report changed, the fingerprints differ.

What it does NOT do: no trading, no transfers, no mainnet. The code refuses any account that is not
a *.testnet account and any RPC that is not a testnet RPC. Testnet NEAR has no monetary value.
The private key comes only from .env and is never logged or returned.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from typing import Any, Callable, Optional

import httpx

from app.schemas.research import ResearchReport

TESTNET_RPC = "https://rpc.testnet.fastnear.com"   # rpc.testnet.near.org is deprecated and rate-limits (HTTP 429, 2026-11-09)
SOCIALDB_TESTNET = "v1.social08.testnet"
APP_KEY = "futurescout"
# SocialDB refused 0.01 NEAR on the first write ("attached deposit is less than the minimum storage balance",
# live 2026-11-08); 0.1 testnet NEAR covers the account's initial storage balance and many records.
STORAGE_DEPOSIT_YOCTO = 10**23
GAS = 50 * 10**12                # 50 TGas
FREE_BYTES_NEEDED = 5_000        # prepaid storage that must remain before a write skips the deposit
EXPLORER_TX = "https://testnet.nearblocks.io/txns/{tx}"
EXPLORER_ACCOUNT = "https://testnet.nearblocks.io/address/{account}"


class NearRecordError(RuntimeError):
    pass


# Fields added to the schema AFTER reports were first sealed on chain. When such a field holds its default
# (None / empty) it is left out of the digest, so reports sealed before the field existed still verify.
# A report that actually carries the new data includes it in the digest as usual. Add to this list whenever a
# new optional field is introduced; never remove entries.
ADDED_TOP_LEVEL_IF_NONE = ("scout", "sector")        # 2026-11-09 Company Scout; 2026-11-09 sector
ADDED_ANYWHERE_IF_EMPTY = ("affiliations", "closes", "plain_summary", "ytd", "counting", "estimated_relevant",
                           "confidence_pct", "evidence_confidence_pct", "risk_multiplier", "scoring_version")   # 2026-11-09 scoring v2   # 2026-11-09: SourceRecord.affiliations, PriceMetrics.closes, InvestmentDraft.plain_summary


def _strip_added_defaults(obj):  # noqa: ANN001
    if isinstance(obj, dict):
        return {k: _strip_added_defaults(v) for k, v in obj.items()
                if not (k in ADDED_ANYWHERE_IF_EMPTY and v in ([], None))}
    if isinstance(obj, list):
        return [_strip_added_defaults(v) for v in obj]
    return obj


def report_digest(report: ResearchReport) -> str:
    """SHA-256 of the report's canonical JSON, excluding the chain record itself (stable across schema additions)."""
    data = report.model_dump(mode="json", exclude={"chain_record"})
    for key in ADDED_TOP_LEVEL_IF_NONE:
        if data.get(key) is None:
            data.pop(key, None)
    data = _strip_added_defaults(data)
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def record_key(run_key: str) -> str:
    """SocialDB keys must be simple; run ids are uuids or report_<time> file names."""
    key = re.sub(r"[^A-Za-z0-9_-]", "_", run_key)[:64]
    if not key:
        raise NearRecordError("empty run id")
    return key


def check_testnet(account_id: str, rpc: str) -> None:
    if not account_id.endswith(".testnet") and not re.fullmatch(r"[0-9a-f]{64}", account_id):
        raise NearRecordError("refusing: NEAR_TESTNET_ACCOUNT_ID must be a .testnet account (mainnet is not allowed)")
    if "testnet" not in rpc:
        raise NearRecordError("refusing: only a NEAR testnet RPC may be used")


@dataclass
class ChainRecord:
    network: str
    contract: str
    account: str
    key: str
    sha256: str
    tx_hash: Optional[str]
    explorer_url: Optional[str]

    def as_dict(self) -> dict:
        return self.__dict__.copy()


class NearRecorder:
    def __init__(
        self,
        account_id: str,
        private_key: str,
        *,
        rpc: str = TESTNET_RPC,
        contract: str = SOCIALDB_TESTNET,
        http: Optional[httpx.Client] = None,
        signer: Optional[Callable[[str, dict, int], str]] = None,
    ) -> None:
        check_testnet(account_id, rpc)
        if not private_key.startswith("ed25519:"):
            raise NearRecordError("NEAR_TESTNET_PRIVATE_KEY must look like 'ed25519:...'")
        self.account_id, self.rpc, self.contract = account_id, rpc, contract
        self._key = private_key
        self._http = http or httpx.Client(timeout=30.0)
        self._real_signer = signer is None
        self._signer = signer or self._sign_with_py_near

    def _set(self, args: dict) -> str:
        deposit = self._deposit()
        try:
            return self._signer("set", args, deposit)
        except NearRecordError as exc:
            # Pay the deposit only when the CONTRACT refused for lack of storage. Never on network errors: a dropped
            # response may hide a write that went through, and retrying with a deposit paid twice (seen live 2026-11-09).
            if deposit == STORAGE_DEPOSIT_YOCTO or not re.search(r"(?i)storage|not enough balance|attached deposit", str(exc)):
                raise
            return self._signer("set", args, STORAGE_DEPOSIT_YOCTO)

    def _deposit(self) -> int:
        """0 when the account's prepaid SocialDB storage covers the write (only gas is paid), else the full deposit.

        Checked live 2026-11-09: futurescoutai.testnet had ~331k free bytes prepaid; a record uses a few hundred.
        """
        if not self._real_signer:
            return STORAGE_DEPOSIT_YOCTO
        try:
            args = base64.b64encode(json.dumps({"account_id": self.account_id}).encode()).decode()
            body = {"jsonrpc": "2.0", "id": "fs", "method": "query",
                    "params": {"request_type": "call_function", "finality": "final", "account_id": self.contract,
                               "method_name": "get_account_storage", "args_base64": args}}
            payload = self._http.post(self.rpc, json=body).json()
            info = json.loads(bytes(payload["result"]["result"]).decode() or "null") or {}
            return 0 if int(info.get("available_bytes", 0)) >= FREE_BYTES_NEEDED else STORAGE_DEPOSIT_YOCTO
        except Exception:  # noqa: BLE001  (check unavailable: try without a deposit; a storage refusal is retried with one)
            return 0

    # ---- write --------------------------------------------------------------
    def _sign_with_py_near(self, method: str, args: dict, deposit: int) -> str:
        from py_near.account import Account  # imported lazily: only needed for real writes

        async def go() -> str:
            acc = Account(self.account_id, self._key, rpc_addr=self.rpc)
            await acc.startup()
            res = await acc.function_call(self.contract, method, args, gas=GAS, amount=deposit)
            tx = getattr(getattr(res, "transaction", None), "hash", None) or getattr(res, "transaction_hash", None)
            if isinstance(res, str):
                tx = res
            status = getattr(res, "status", None)
            if isinstance(status, dict) and "Failure" in status:
                raise NearRecordError(f"transaction failed on chain: {str(status['Failure'])[:200]}")
            return str(tx) if tx else ""

        if sys.platform == "win32":  # avoids noisy "Event loop is closed" SSL teardown errors from aiohttp on Windows
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        try:
            return asyncio.run(go())
        except NearRecordError:
            raise
        except Exception as exc:  # noqa: BLE001  (message only; never the key)
            raise NearRecordError(f"could not send the testnet transaction ({type(exc).__name__}: {str(exc)[:200]})".replace(self._key, "***")) from None

    def record(self, run_key: str, report: ResearchReport) -> ChainRecord:
        key = record_key(run_key)
        digest = report_digest(report)
        value = {"sha256": digest, "topic": report.topic[:120], "generated_at": report.generated_at.isoformat(),
                 "agents_run": ",".join(report.agents_run)}
        args = {"data": {self.account_id: {APP_KEY: {"reports": {key: value}}}}}
        tx = self._set(args)
        return ChainRecord("testnet", self.contract, self.account_id, key, digest, tx or None,
                           EXPLORER_TX.format(tx=tx) if tx else EXPLORER_ACCOUNT.format(account=self.account_id))

    def record_fund_decision(self, key: str, value: dict) -> ChainRecord:
        """Fingerprint of one topic-fund decision (paper simulation), under <account>/futurescout/funds/<key>."""
        k = record_key(key)
        args = {"data": {self.account_id: {APP_KEY: {"funds": {k: value}}}}}
        tx = self._set(args)
        return ChainRecord("testnet", self.contract, self.account_id, f"funds/{k}", str(value.get("sha256", "")), tx or None,
                           EXPLORER_TX.format(tx=tx) if tx else EXPLORER_ACCOUNT.format(account=self.account_id))

    # ---- read (free, no key needed) -----------------------------------------
    def read(self, run_key: str) -> Optional[dict]:
        return read_record(self._http, self.rpc, self.contract, self.account_id, record_key(run_key))


def read_record(http: httpx.Client, rpc: str, contract: str, account_id: str, key: str) -> Optional[dict]:
    path = f"{account_id}/{APP_KEY}/reports/{key}/**"
    args = base64.b64encode(json.dumps({"keys": [path]}).encode()).decode()
    body = {"jsonrpc": "2.0", "id": "fs", "method": "query",
            "params": {"request_type": "call_function", "finality": "final", "account_id": contract,
                       "method_name": "get", "args_base64": args}}
    try:
        r = http.post(rpc, json=body)
        payload: Any = r.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise NearRecordError(f"could not read from NEAR testnet ({type(exc).__name__})") from None
    if "error" in payload or "result" not in payload or "result" not in payload["result"]:
        raise NearRecordError(f"NEAR RPC error: {str(payload.get('error', payload))[:200]}")
    data = json.loads(bytes(payload["result"]["result"]).decode() or "{}")
    return (((data.get(account_id) or {}).get(APP_KEY) or {}).get("reports") or {}).get(key)


def verify(report: ResearchReport, onchain: Optional[dict]) -> dict:
    """Compare a report with its on-chain record."""
    digest = report_digest(report)
    if not onchain:
        return {"status": "not_recorded", "sha256": digest}
    return {"status": "match" if onchain.get("sha256") == digest else "MISMATCH",
            "sha256": digest, "onchain_sha256": onchain.get("sha256")}


def read_balance(http: httpx.Client, rpc: str, account_id: str) -> dict:
    """view_account on NEAR testnet -> {'available_near', 'locked_near', 'storage_bytes'}. Read-only, no key."""
    check_testnet(account_id, rpc)
    body = {"jsonrpc": "2.0", "id": "fs-bal", "method": "query",
            "params": {"request_type": "view_account", "finality": "final", "account_id": account_id}}
    try:
        payload: Any = http.post(rpc, json=body, timeout=30).json()
    except (httpx.HTTPError, ValueError) as exc:
        raise NearRecordError(f"could not read the balance from NEAR testnet ({type(exc).__name__})") from None
    if "error" in payload or "result" not in payload:
        raise NearRecordError(f"NEAR RPC error: {str(payload.get('error', payload))[:200]}")
    res = payload["result"]
    return {"available_near": round(int(res.get("amount", "0")) / 10 ** 24, 4),
            "locked_near": round(int(res.get("locked", "0")) / 10 ** 24, 4),
            "storage_bytes": int(res.get("storage_usage", 0))}

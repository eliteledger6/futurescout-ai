"""NEAR Intents "signed order" route: QUOTES ONLY (owner request 2026-11-09). There is no submit function here.

Why this exists: the two real test trades paid from the WALLET to a 1Click deposit address (depositType ORIGIN_CHAIN)
and stayed "PROCESSING", while the owner's manual swaps inside near.com were instant. near.com trades from money
already held inside NEAR Intents, with a signed order, and (from everything observable) through the private
"Confidential Intents" layer: its balances are not on the public contract and its swaps are not on the public explorer.

What this module can do, none of which moves funds:
  * dry quotes for the internal route (depositType INTENTS) and, after a login, the confidential route;
  * a real quote plus the UNSIGNED order the service generates for it (POST /v0/generate-intent);
  * a login: sign an EMPTY order ("intents": [], the documented ownership proof) with the account key to get a
    short-lived session token, then read the private balances (GET /v0/account/balances).
What it cannot do: sign or submit a swap order. Building that is a separate, explicit decision.

Formats were taken from the service's own answers and docs on 2026-11-09:
  * nonce (32 bytes) = magic 5628f6c6 | version 00 | 4-byte salt (intents.near `current_salt`) | u64 LE time in
    nanoseconds | 15 random bytes. In generated swap orders that time is the order deadline.
  * NEP-413: signature = ed25519( sha256( borsh(u32 2^31+413) + borsh{message: string, nonce: [u8;32],
    recipient: string, callback_url: Option<string>} ) ).
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import struct
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional

import httpx

NONCE_MAGIC = bytes.fromhex("5628f6c6")
NEP413_TAG = 2 ** 31 + 413
VERIFIER = "intents.near"
ROUTES = ("ORIGIN_CHAIN", "INTENTS", "CONFIDENTIAL_INTENTS")


def versioned_nonce(salt_hex: str, when: datetime, rand: Optional[bytes] = None) -> bytes:
    rand = os.urandom(15) if rand is None else rand
    if len(rand) != 15 or len(bytes.fromhex(salt_hex)) != 4:
        raise ValueError("nonce needs a 4-byte salt and 15 random bytes")
    return NONCE_MAGIC + b"\x00" + bytes.fromhex(salt_hex) + struct.pack("<Q", int(when.timestamp() * 1_000_000_000)) + rand


def _borsh_str(s: str) -> bytes:
    b = s.encode("utf-8")
    return struct.pack("<I", len(b)) + b


def nep413_hash(message: str, nonce: bytes, recipient: str, callback_url: Optional[str] = None) -> bytes:
    if len(nonce) != 32:
        raise ValueError("NEP-413 nonce must be 32 bytes")
    payload = _borsh_str(message) + nonce + _borsh_str(recipient) + (b"\x00" if callback_url is None else b"\x01" + _borsh_str(callback_url))
    return hashlib.sha256(struct.pack("<I", NEP413_TAG) + payload).digest()


def sign_nep413(private_key: str, message: str, nonce: bytes, recipient: str = VERIFIER) -> tuple[str, str]:
    """(public_key, signature), both 'ed25519:<base58>'. The key string never leaves this function."""
    import base58
    from nacl.signing import SigningKey

    if not private_key.startswith("ed25519:"):
        raise ValueError("only ed25519 keys are supported")
    raw = base58.b58decode(private_key.split(":", 1)[1])
    if len(raw) not in (32, 64):
        raise ValueError("unexpected ed25519 key length")
    sk = SigningKey(raw[:32])
    sig = sk.sign(nep413_hash(message, nonce, recipient)).signature
    return "ed25519:" + base58.b58encode(bytes(sk.verify_key)).decode(), "ed25519:" + base58.b58encode(sig).decode()


def login_message(account: str, deadline: datetime) -> str:
    """The documented ownership proof: an order with no intents. It cannot move tokens."""
    return json.dumps({"deadline": deadline.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "intents": [], "signer_id": account}, separators=(",", ":"))


class SignedIntents:
    def __init__(self, api: str, *, http: Optional[httpx.Client] = None, api_key: Optional[str] = None,
                 now: Callable[[], datetime] = lambda: datetime.now(timezone.utc)) -> None:
        self.api = api.rstrip("/")
        self._http = http or httpx.Client(timeout=40.0)
        self._key_header = {"X-API-Key": api_key} if api_key else {}
        self._now = now

    # ---- public reads
    def tokens(self) -> list[dict]:
        r = self._http.get(f"{self.api}/v0/tokens", params={"ondoTokens": "true"})
        return r.json() if r.status_code == 200 else []

    def quote(self, *, route: str, pay_asset: str, dest_asset: str, amount_units: int, account: str, dry: bool = True,
              session_token: Optional[str] = None, slippage_bps: int = 100) -> dict:
        """A quote on one route. Raises RuntimeError with the service's message when refused."""
        if route not in ROUTES:
            raise ValueError(f"unknown route {route}")
        body = {"dry": dry, "swapType": "EXACT_INPUT", "slippageTolerance": slippage_bps, "originAsset": pay_asset, "depositType": route,
                "destinationAsset": dest_asset, "amount": str(amount_units), "refundTo": account, "refundType": route,
                "recipient": account, "recipientType": "INTENTS" if route == "ORIGIN_CHAIN" else route,
                "deadline": (self._now() + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S.000Z")}
        headers = dict(self._key_header)
        if session_token:
            headers["Authorization"] = f"Bearer {session_token}"
        r = self._http.post(f"{self.api}/v0/quote", json=body, headers=headers)
        try:
            data = r.json()
        except ValueError:
            raise RuntimeError(f"HTTP {r.status_code}") from None
        q = data.get("quote") if isinstance(data, dict) else None
        if not q:
            raise RuntimeError(str((data or {}).get("message") or f"HTTP {r.status_code}")[:160])
        return {**q, "correlationId": data.get("correlationId")}

    def unsigned_order(self, deposit_address: str, account: str) -> dict:
        """The order the service wants signed for a real INTENTS-route quote. Nothing is signed or submitted here."""
        r = self._http.post(f"{self.api}/v0/generate-intent", headers=self._key_header,
                            json={"type": "swap_transfer", "standard": "nep413", "signerId": account, "depositAddress": deposit_address})
        data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        if r.status_code >= 400 or "intent" not in data:
            raise RuntimeError(str(data.get("message") or f"HTTP {r.status_code}")[:160])
        return data["intent"]

    # ---- login (needs the account key; signs an EMPTY order)
    def login(self, account: str, private_key: str, salt_hex: str) -> dict:
        """Session token for the account's private balances. Tries the two plausible nonce times; a failed try is harmless."""
        errors = []
        for label, minutes in (("now", 0), ("deadline", 5)):
            deadline = self._now() + timedelta(minutes=5)
            nonce = versioned_nonce(salt_hex, self._now() + timedelta(minutes=minutes))
            message = login_message(account, deadline)
            public_key, signature = sign_nep413(private_key, message, nonce)
            signed = {"standard": "nep413", "payload": {"message": message, "nonce": base64.b64encode(nonce).decode(), "recipient": VERIFIER},
                      "public_key": public_key, "signature": signature}
            r = self._http.post(f"{self.api}/v0/auth/authenticate", json={"signedData": signed}, headers=self._key_header)
            data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
            if r.status_code < 300 and data.get("accessToken"):
                return {"accessToken": data["accessToken"], "expiresIn": data.get("expiresIn"), "nonce_time": label, "public_key": public_key}
            errors.append(f"{label}: {str(data.get('message') or r.status_code)[:120]}")
        raise RuntimeError("login refused (" + "; ".join(errors) + ")")

    def balances(self, session_token: str) -> list[dict]:
        r = self._http.get(f"{self.api}/v0/account/balances", headers={**self._key_header, "Authorization": f"Bearer {session_token}"})
        data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        if r.status_code >= 400:
            raise RuntimeError(str(data.get("message") or f"HTTP {r.status_code}")[:160])
        return data.get("balances") or []

"""Signed-order route, QUOTES ONLY: formats, the empty-order login, and proof that nothing here can submit a swap."""

import base64
import hashlib
import json
import struct
from datetime import datetime, timezone

import base58
import httpx
import pytest
from nacl.signing import SigningKey, VerifyKey

from app.fund import intents_signed as si

NOW = datetime(2026, 11, 9, 15, 0, tzinfo=timezone.utc)
SK = SigningKey(bytes(range(32)))                                   # throwaway test key, never a real one
KEY = "ed25519:" + base58.b58encode(bytes(SK) + bytes(SK.verify_key)).decode()


def test_nonce_layout_matches_the_service():
    n = si.versioned_nonce("252812b3", datetime(2026, 11, 12, 15, 19, 32, tzinfo=timezone.utc), rand=bytes(15))
    assert len(n) == 32 and n[:4].hex() == "5628f6c6" and n[4] == 0 and n[5:9].hex() == "252812b3"
    assert struct.unpack("<Q", n[9:17])[0] == 1794496772000000000      # the value decoded from a real generated order
    # a real nonce from the service decodes with the same layout
    real = base64.b64decode("Vij2xgAlKBKzACildU5V5xjB3eLDs6eJS/zqG3MJP3U=")
    assert real[:9] == n[:9] and real[9:17] == n[9:17]
    with pytest.raises(ValueError):
        si.versioned_nonce("2528", NOW)


def test_nep413_hash_and_signature():
    nonce = si.versioned_nonce("252812b3", NOW, rand=bytes(15))
    msg = si.login_message("fund-test.near", NOW)
    assert json.loads(msg) == {"deadline": "2026-11-09T15:00:00.000Z", "intents": [], "signer_id": "fund-test.near"}
    expected = hashlib.sha256(bytes.fromhex("9d010080") + struct.pack("<I", len(msg)) + msg.encode() + nonce
                              + struct.pack("<I", 12) + b"intents.near" + b"\x00").digest()
    assert si.nep413_hash(msg, nonce, "intents.near") == expected
    pub, sig = si.sign_nep413(KEY, msg, nonce)
    assert pub == "ed25519:" + base58.b58encode(bytes(SK.verify_key)).decode()
    VerifyKey(bytes(SK.verify_key)).verify(expected, base58.b58decode(sig.split(":", 1)[1]))     # raises if wrong
    with pytest.raises(ValueError):
        si.sign_nep413("secp256k1:abc", msg, nonce)
    with pytest.raises(ValueError):
        si.nep413_hash(msg, b"short", "intents.near")


def client(handler):
    return si.SignedIntents("https://oc.test", http=httpx.Client(transport=httpx.MockTransport(handler)), now=lambda: NOW)


def test_login_signs_only_an_empty_order_and_retries_the_other_nonce_time():
    seen = []

    def handler(req):
        body = json.loads(req.read())
        seen.append(body)
        if len(seen) == 1:
            return httpx.Response(401, json={"message": "timestamp validation failed"})
        return httpx.Response(200, json={"accessToken": "tok-abc", "refreshToken": "r", "expiresIn": 3600})
    out = client(handler).login("fund-test.near", KEY, "252812b3")
    assert out["accessToken"] == "tok-abc" and out["nonce_time"] == "deadline" and len(seen) == 2
    for body in seen:
        sd = body["signedData"]
        assert sd["standard"] == "nep413" and sd["payload"]["recipient"] == "intents.near"
        assert json.loads(sd["payload"]["message"])["intents"] == []                # nothing but the ownership proof is ever signed
        assert len(base64.b64decode(sd["payload"]["nonce"])) == 32 and sd["signature"].startswith("ed25519:")
        assert KEY.split(":")[1] not in json.dumps(body)                            # the private key never goes on the wire
    with pytest.raises(RuntimeError, match="login refused"):
        client(lambda r: httpx.Response(401, json={"message": "signature verification failed"})).login("fund-test.near", KEY, "252812b3")


def test_quotes_per_route_and_unsigned_order():
    seen = []

    def handler(req):
        if req.url.path == "/v0/quote":
            body = json.loads(req.read())
            seen.append((body, req.headers.get("authorization")))
            if body["depositType"] == "CONFIDENTIAL_INTENTS" and not req.headers.get("authorization"):
                return httpx.Response(401, json={"message": "User authentication is required for confidential quotes"})
            return httpx.Response(201, json={"quote": {"amountInUsd": "10", "amountOutUsd": "9.9", "depositAddress": "dep1"}, "correlationId": "c"})
        if req.url.path == "/v0/generate-intent":
            return httpx.Response(201, json={"intent": {"standard": "nep413", "payload": {"message": "{}", "nonce": "x", "recipient": "intents.near"}}})
        if req.url.path == "/v0/account/balances":
            return httpx.Response(200, json={"balances": [{"tokenId": "nep141:wrap.near", "available": "5", "source": "private"}]})
        return httpx.Response(404, json={})
    c = client(handler)
    q = c.quote(route="INTENTS", pay_asset="nep141:wrap.near", dest_asset="d", amount_units=5, account="a.near")
    assert q["depositAddress"] == "dep1" and seen[-1][0]["dry"] is True and seen[-1][0]["refundType"] == "INTENTS" and seen[-1][0]["recipientType"] == "INTENTS"
    c.quote(route="ORIGIN_CHAIN", pay_asset="p", dest_asset="d", amount_units=5, account="a.near")
    assert seen[-1][0]["refundType"] == "ORIGIN_CHAIN" and seen[-1][0]["recipientType"] == "INTENTS"
    with pytest.raises(RuntimeError, match="authentication is required"):
        c.quote(route="CONFIDENTIAL_INTENTS", pay_asset="p", dest_asset="d", amount_units=5, account="a.near")
    c.quote(route="CONFIDENTIAL_INTENTS", pay_asset="p", dest_asset="d", amount_units=5, account="a.near", session_token="tok")
    assert seen[-1][1] == "Bearer tok" and seen[-1][0]["recipientType"] == "CONFIDENTIAL_INTENTS"
    assert c.unsigned_order("dep1", "a.near")["standard"] == "nep413"
    assert c.balances("tok")[0]["source"] == "private"
    with pytest.raises(ValueError):
        c.quote(route="BANK", pay_asset="p", dest_asset="d", amount_units=5, account="a.near")


def test_there_is_no_way_to_submit_a_swap_order():
    names = [n for n in dir(si.SignedIntents) if not n.startswith("_")] + [n for n in dir(si) if not n.startswith("_")]
    assert not any("submit" in n.lower() for n in names)
    src = open(si.__file__, encoding="utf-8").read()
    assert "/v0/submit-intent" not in src.replace("POST /v0/submit-intent", "")      # only ever mentioned in prose, never called

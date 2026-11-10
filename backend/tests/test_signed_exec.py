"""Signed-order route (near.com's private route): the order is verified before signing, sent once, and off by default."""

import base64
import json
from datetime import datetime, timezone

import httpx
import pytest

from app.fund.intents_signed import versioned_nonce
from app.fund.live import LiveConfig, OneClickLive, Proposal, TradingState
from app.fund.signed_exec import SignedExecutor, submit_signed_order, verify_order

NOW = datetime(2026, 11, 10, 9, tzinfo=timezone.utc)
ACCOUNT, DEPOSIT, NEAR = "fund-test.near", "dep" + "0" * 61, "nep141:wrap.near"
UNITS = int(25.0 / 5.0 * 10 ** 24)                                   # $25 at $5 per NEAR
KEY = "ed25519:" + "1" * 40                                          # never used for real signing in these tests


def order(*, signer=ACCOUNT, receiver=DEPOSIT, tokens=None, intents=None, recipient="intents.near", extra=None, deadline="2026-11-13T09:00:00.000Z"):
    msg = {"deadline": deadline, "signer_id": signer,
           "intents": intents if intents is not None else [{"intent": "transfer", "receiver_id": receiver, "tokens": tokens or {NEAR: str(UNITS)}}]}
    msg.update(extra or {})
    nonce = base64.b64encode(versioned_nonce("252812b3", datetime(2026, 11, 13, 9, tzinfo=timezone.utc), rand=bytes(15))).decode()
    return {"standard": "nep413", "payload": {"message": json.dumps(msg), "nonce": nonce, "recipient": recipient}}


def check(o):
    return verify_order(o, account=ACCOUNT, deposit_address=DEPOSIT, pay_asset=NEAR, units=UNITS, allowed_recipients=["intents.near"], now=NOW)


def test_only_the_exact_approved_transfer_passes():
    assert check(order()) == []
    cases = {
        "not a transfer": order(intents=[{"intent": "native_withdraw", "receiver_id": DEPOSIT, "amount": "1"}]),
        "exactly one transfer": order(intents=[{"intent": "transfer", "receiver_id": DEPOSIT, "tokens": {NEAR: str(UNITS)}}] * 2),
        "deposit address": order(receiver="attacker.near"),
        "not exactly": order(tokens={NEAR: str(UNITS * 2)}),
        "not exactly ": order(tokens={NEAR: str(UNITS), "nep141:usdc": "1"}),
        "signer is": order(signer="someone-else.near"),
        "addressed to": order(recipient="evil.near"),
        "unexpected message fields": order(extra={"referral": "x"}),
        "already passed": order(deadline="2026-11-09T09:00:00.000Z"),
        "exactly one transfer ": order(intents=[]),
    }
    for expect, o in cases.items():
        assert any(expect.strip() in p for p in check(o)), (expect, check(o))
    bad_nonce = order()
    bad_nonce["payload"]["nonce"] = base64.b64encode(bytes(32)).decode()
    assert any("versioned nonce" in p for p in check(bad_nonce))
    private_form = order(tokens={"imt:" + "5" * 64 + ":" + NEAR: str(UNITS)})          # the private balance's form of the same asset
    assert check(private_form) == []
    wrong_asset = order(tokens={"imt:" + "5" * 64 + ":nep141:usdc": str(UNITS)})
    assert any("not exactly" in p for p in check(wrong_asset))
    short_id = order(tokens={"imt:abc:" + NEAR: str(UNITS)})
    assert any("not exactly" in p for p in check(short_id))
    far = order(recipient="intents.far")
    assert any("addressed to" in p for p in check(far))                                  # only when the config lists it
    assert verify_order(far, account=ACCOUNT, deposit_address=DEPOSIT, pay_asset=NEAR, units=UNITS,
                        allowed_recipients=["intents.near", "intents.far"], now=NOW) == []
    with_cb = order()
    with_cb["payload"]["callbackUrl"] = "https://x.test"
    assert any("callback" in p for p in check(with_cb))
    assert check({"standard": "erc191"})[0].startswith("unexpected order standard")


class FakeApi:
    def __init__(self, *, balance=10 * 10 ** 24, order_obj=None, quote=None):
        self.balance, self.order_obj, self.quote_obj, self.calls = balance, order_obj, quote, []

    def login(self, account, key, salt):
        self.calls.append("login")
        return {"accessToken": "tok"}

    def tokens(self):
        return [{"assetId": NEAR, "price": 5.0}]

    def balances(self, token):
        self.calls.append("balances")
        return [{"tokenId": NEAR, "available": str(self.balance), "source": "private"}]

    def quote(self, **kw):
        self.calls.append(("quote", kw["route"], kw["dry"], kw["session_token"]))
        return self.quote_obj or {"amountIn": str(UNITS), "amountInUsd": "25", "amountOutUsd": "24.8", "amountOutFormatted": "0.5", "depositAddress": DEPOSIT,
                                  "deadline": "2026-11-13T09:00:00.000Z"}

    def unsigned_order(self, deposit, account):
        self.calls.append("order")
        return self.order_obj or order()


def make(tmp_path, api, *, cfg=None, submit_error=None, statuses=("PROCESSING", "SUCCESS"), kill=False):
    cfg = cfg or LiveConfig(trading_enabled=True, route="confidential", signed_route_enabled=True, max_trade_usd=25, max_day_usd=35, max_total_usd=35,
                            poll_seconds=0.0)
    sent, n = [], {"i": 0}

    def status(req):
        st = statuses[min(n["i"], len(statuses) - 1)]
        n["i"] += 1
        return httpx.Response(200, json={"status": st, "swapDetails": {"amountOutFormatted": "0.5"}})

    def submitter(o, key):
        sent.append(o)
        if submit_error:
            raise RuntimeError(submit_error)
        return "IntentHash111"
    oc = OneClickLive("https://oc.test", http=httpx.Client(transport=httpx.MockTransport(status)))
    ex = SignedExecutor(cfg, tmp_path / "trading" / "state.json", api, oc, account=ACCOUNT, private_key=KEY, salt_reader=lambda: "252812b3",
                        submitter=submitter, now=lambda: NOW, sleep=lambda s: None)
    if kill:
        ex._poller.kill_file.parent.mkdir(parents=True, exist_ok=True)
        ex._poller.kill_file.write_text("stop")
    return ex, sent


def prop(status="approved"):
    p = Proposal(id="sig1234567", created_at=NOW, mode="live", topic="AI agents", ticker="GOOGL", symbol="GOOGLon", asset_id="nep141:googl",
                 usd=25.0, ref_close=50.0, ref_close_date="2026-11-09")
    p.status = status
    return p


def test_happy_path_logs_in_checks_balance_verifies_then_submits_once(tmp_path):
    api = FakeApi()
    ex, sent = make(tmp_path, api)
    st, p = TradingState(), prop()
    st.proposals.append(p)
    ex.execute(st, p)
    assert p.status == "success" and len(sent) == 1 and sent[0] == order()
    assert api.calls == ["login", "balances", ("quote", "CONFIDENTIAL_INTENTS", False, "tok"), "order"]
    assert p.quote["route"] == "confidential" and [e.status for e in p.history][:2] == ["executing", "deposited"]
    assert "IntentHash111" in " ".join(e.note for e in p.history)
    with pytest.raises(RuntimeError, match="never sent twice"):
        ex.execute(st, p)
    assert len(sent) == 1


def test_switched_off_by_default_and_every_guard_stops_before_signing(tmp_path):
    base = dict(trading_enabled=True, route="confidential", max_trade_usd=25, max_day_usd=35, max_total_usd=35, poll_seconds=0.0)
    guards = [
        (dict(cfg=LiveConfig(**base)), FakeApi(), "switched off"),                                          # the default: signed_route_enabled False
        (dict(cfg=LiveConfig(**{**base, "route": "wallet", "signed_route_enabled": True})), FakeApi(), "not 'confidential'"),
        (dict(cfg=LiveConfig(**{**base, "trading_enabled": False, "signed_route_enabled": True})), FakeApi(), "trading_enabled"),
        (dict(kill=True), FakeApi(), "kill switch"),
        (dict(cfg=LiveConfig(**{**base, "signed_route_enabled": True, "max_trade_usd": 20})), FakeApi(), "per-trade cap"),
        (dict(), FakeApi(balance=10 ** 24), "private balance holds"),
        (dict(), FakeApi(order_obj=order(receiver="attacker.near")), "deposit address"),
        (dict(), FakeApi(order_obj=order(tokens={NEAR: str(UNITS * 3)})), "not exactly"),
        (dict(), FakeApi(quote={"amountIn": str(UNITS), "amountInUsd": "25", "amountOutUsd": "20", "amountOutFormatted": "0.5", "depositAddress": DEPOSIT}), "cost"),
        (dict(), FakeApi(quote={"amountIn": "1", "amountInUsd": "25", "amountOutUsd": "24.8", "amountOutFormatted": "0.5", "depositAddress": DEPOSIT}), "amountIn differs"),
    ]
    for i, (kw, api, match) in enumerate(guards):
        ex, sent = make(tmp_path / str(i), api, **kw)
        with pytest.raises(RuntimeError, match=match):
            ex.execute(TradingState(), prop())
        assert sent == [], match
    ex, sent = make(tmp_path / "unapproved", FakeApi())
    with pytest.raises(RuntimeError, match="not 'approved'"):
        ex.execute(TradingState(), prop("proposed"))
    assert sent == [] and LiveConfig().signed_route_enabled is False and LiveConfig().route == "wallet"


def test_unclear_submit_error_is_recorded_and_never_retried(tmp_path):
    ex, sent = make(tmp_path, FakeApi(), submit_error="connection reset")
    st, p = TradingState(), prop()
    st.proposals.append(p)
    with pytest.raises(RuntimeError, match="never approve again"):
        ex.execute(st, p)
    assert p.status == "deposited" and len(sent) == 1 and st.spent("live") == 25.0
    with pytest.raises(RuntimeError):
        ex.execute(st, p)
    assert len(sent) == 1


def test_submit_signs_the_exact_payload_and_posts_it_once():
    import base58
    from nacl.signing import SigningKey, VerifyKey

    from app.fund.intents_signed import nep413_hash
    sk = SigningKey(bytes(range(32)))
    key = "ed25519:" + base58.b58encode(bytes(sk) + bytes(sk.verify_key)).decode()
    seen = []

    def handler(req):
        seen.append((req.url.path, req.headers.get("x-api-key"), json.loads(req.read())))
        return httpx.Response(200, json={"intentHash": "Hash9", "correlationId": "c"})
    o = order()
    out = submit_signed_order(httpx.Client(transport=httpx.MockTransport(handler)), "https://oc.test", "pk-1", o, key)
    path, api_key, body = seen[0]
    assert out == "Hash9" and len(seen) == 1 and path == "/v0/submit-intent" and api_key == "pk-1" and body["type"] == "swap_transfer"
    sd = body["signedData"]
    assert sd["payload"] == o["payload"]                                                   # the verified payload is sent unmodified
    digest = nep413_hash(o["payload"]["message"], base64.b64decode(o["payload"]["nonce"]), "intents.near")
    VerifyKey(bytes(sk.verify_key)).verify(digest, base58.b58decode(sd["signature"].split(":", 1)[1]))
    assert key.split(":")[1] not in json.dumps(body)
    with pytest.raises(RuntimeError, match="refused the order"):
        submit_signed_order(httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(400, json={"message": "bad"}))), "https://oc.test", None, o, key)

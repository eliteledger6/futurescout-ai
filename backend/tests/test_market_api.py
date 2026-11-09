"""Report marketplace tests. Payments are FAKED (no chain access); reports are SYNTHETIC fixture runs."""

import pytest
from fastapi.testclient import TestClient

from app.api import create_app
from app.api.market import DbLedger, FileLedger
from app.api.store import DbStore, FileStore
from app.chain.near_record import NearRecordError, NearRecorder
from app.chain.payments import VerifiedPayment, near_to_yocto, parse_transfer
from app.config import Settings
from app.db import Base, make_engine, make_session_factory, save_report
from app.report import render_markdown
from tests.test_db import fixture_report

SELLER, BUYER = "futurescout-fixture.testnet", "buyerbot-fixture.testnet"
TX = "FixtureTxHash1111111111111111111111111111111"


def rpc_result(signer=BUYER, receiver=SELLER, deposit=near_to_yocto(0.1), ok=True, hash_=TX):
    return {"result": {"status": ({"SuccessValue": ""} if ok else {"Failure": {"x": 1}}),
                       "transaction": {"hash": hash_, "signer_id": signer, "receiver_id": receiver,
                                       "actions": [{"Transfer": {"deposit": str(deposit)}}, {"CreateAccount": {}}]},
                       "transaction_outcome": {"block_hash": "BlockFixture"}}}


def test_near_to_yocto_is_exact():
    assert near_to_yocto(0.1) == 10**23 and near_to_yocto(1) == 10**24 and near_to_yocto(0.25) == 25 * 10**22


def test_parse_transfer_checks_everything():
    p = parse_transfer(rpc_result(), tx_hash=TX, buyer=BUYER, seller=SELLER, min_yocto=near_to_yocto(0.1))
    assert p.amount_near == pytest.approx(0.1) and p.block_hash == "BlockFixture"
    for bad, msg in [(rpc_result(signer="someone.testnet"), "not by the buyer"), (rpc_result(receiver="thief.testnet"), "not the seller"),
                     (rpc_result(deposit=near_to_yocto(0.05)), "too small"), (rpc_result(ok=False), "did not succeed"),
                     ({"error": {"data": "UNKNOWN_TRANSACTION"}}, "not found"), (rpc_result(hash_="Other"), "hash mismatch")]:
        with pytest.raises(NearRecordError, match=msg):
            parse_transfer(bad, tx_hash=TX, buyer=BUYER, seller=SELLER, min_yocto=near_to_yocto(0.1))


@pytest.fixture
def market(tmp_path):
    report = fixture_report()
    (tmp_path / "report_20261108T000000Z.json").write_text(report.model_dump_json(), encoding="utf-8")
    (tmp_path / "report_20261108T000000Z.md").write_text(render_markdown(report), encoding="utf-8")
    verified = []

    def fake_verifier(tx_hash, buyer, seller, price):
        verified.append((tx_hash, buyer, seller, price))
        if tx_hash.startswith("Bad"):
            raise NearRecordError("payment too small: 0.0100 NEAR, price is 0.1000 NEAR")
        return VerifiedPayment(tx_hash=tx_hash, buyer=buyer, seller=seller, amount_yocto=near_to_yocto(price), block_hash="B")

    sales = []
    recorder = NearRecorder(SELLER, "ed25519:FIXTUREkey", signer=lambda m, a, d: sales.append(a) or "SaleTx1")
    app = create_app(Settings(_env_file=None, near_ai_api_key="k", near_testnet_account_id=SELLER, report_price_near=0.1),
                     store=FileStore(tmp_path), ledger=FileLedger(tmp_path / "purchases.json"),
                     payment_verifier=fake_verifier, sale_recorder=lambda: recorder)
    return TestClient(app), verified, sales


def test_listing_is_a_teaser_and_full_report_needs_a_verified_payment(market):
    client, verified, sales = market
    listing = client.get("/api/market").json()
    assert listing["enabled"] and listing["seller_account"] == SELLER and listing["price_near"] == 0.1
    [t] = listing["reports"]
    assert t["locked"] and t["summary"] and t["themes"] and "report" not in t and "how_to_buy" in t
    rid = t["id"]
    assert client.get(f"/api/market/{rid}", params={"buyer": BUYER}).json()["locked"] is True

    res = client.post(f"/api/market/{rid}/purchase", json={"buyer_account": BUYER, "tx_hash": TX})
    assert res.status_code == 200
    body = res.json()
    assert body["locked"] is False and body["report"]["topic"] == "chiplet interconnect" and body["markdown"].startswith("# FUTURESCOUT")
    assert body["receipt"]["amount_near"] == pytest.approx(0.1) and body["receipt"]["tx_hash"] == TX
    assert body["receipt"]["sale_record"]["tx_hash"] == "SaleTx1"   # the seller's on-chain sale note (its own transaction)
    assert verified == [(TX, BUYER, SELLER, 0.1)]
    assert sales and "sales" in str(sales[0])                     # seller noted the sale on-chain
    # now unlocked for this buyer, still locked for others
    assert client.get(f"/api/market/{rid}", params={"buyer": BUYER}).json()["locked"] is False
    assert client.get(f"/api/market/{rid}", params={"buyer": "other.testnet"}).json()["locked"] is True
    [p] = client.get(f"/api/market/{rid}/purchases").json()
    assert p["buyer_account"] == BUYER and p["tx_hash"] == TX


def test_payment_rules(market):
    client, _, _ = market
    rid = client.get("/api/market").json()["reports"][0]["id"]
    assert client.post(f"/api/market/{rid}/purchase", json={"buyer_account": BUYER, "tx_hash": TX}).status_code == 200
    # same tx cannot unlock for a second buyer
    res = client.post(f"/api/market/{rid}/purchase", json={"buyer_account": "second.testnet", "tx_hash": TX})
    assert res.status_code == 409
    # bad payment
    res = client.post(f"/api/market/{rid}/purchase", json={"buyer_account": "second.testnet", "tx_hash": "Bad" + "x" * 40})
    assert res.status_code == 402 and "too small" in res.json()["detail"]
    # malformed inputs never reach the chain
    assert client.post(f"/api/market/{rid}/purchase", json={"buyer_account": "Bad Account!", "tx_hash": TX}).status_code == 422
    assert client.post("/api/market/nope/purchase", json={"buyer_account": BUYER, "tx_hash": TX}).status_code == 404


def test_marketplace_disabled_without_seller_account(tmp_path):
    report = fixture_report()
    (tmp_path / "report_20261108T000000Z.json").write_text(report.model_dump_json(), encoding="utf-8")
    client = TestClient(create_app(Settings(_env_file=None, near_ai_api_key="k"), store=FileStore(tmp_path),
                                   ledger=FileLedger(tmp_path / "p.json")))
    assert client.get("/api/market").json()["enabled"] is False
    assert client.post("/api/market/report_20261108T000000Z/purchase", json={"buyer_account": BUYER, "tx_hash": TX}).status_code == 503


def test_db_ledger_round_trip(tmp_path):
    url = f"sqlite:///{(tmp_path / 'm.db').as_posix()}"
    engine = make_engine(url)
    Base.metadata.create_all(engine)
    sessions = make_session_factory(engine)
    with sessions() as s:
        rid = save_report(s, fixture_report(), "md")
        s.commit()
    ledger = DbLedger(sessions)
    assert not ledger.has_access(rid, BUYER) and not ledger.tx_used(TX)
    ledger.record(rid, VerifiedPayment(TX, BUYER, SELLER, near_to_yocto(0.1), "B"), {"note": "fixture"})
    assert ledger.has_access(rid, BUYER) and ledger.tx_used(TX)
    [p] = ledger.purchases(rid)
    assert p["amount_yocto"] == str(near_to_yocto(0.1)) and p["sale_record"] == {"note": "fixture"}
    client = TestClient(create_app(Settings(_env_file=None, near_ai_api_key="k", near_testnet_account_id=SELLER), store=DbStore(url), ledger=ledger))
    assert client.get(f"/api/market/{rid}", params={"buyer": BUYER}).json()["locked"] is False

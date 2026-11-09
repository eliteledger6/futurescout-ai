"""NEAR testnet record tests. Nothing is sent to any network: signing is faked and RPC reads use
httpx.MockTransport. Keys below are SYNTHETIC (FIXTURE)."""

import base64
import json

import httpx
import pytest
from fastapi.testclient import TestClient

from app import service
from app.api import create_app
from app.api.store import FileStore
from app.chain import NearRecorder, NearRecordError, read_record, report_digest, verify
from app.chain.near_record import SOCIALDB_TESTNET, TESTNET_RPC
from app.config import Settings
from app.schemas.research import ResearchReport
from tests.test_db import fixture_report

ACCOUNT = "futurescout-fixture.testnet"
KEY = "ed25519:FIXTUREprivatekeyNEVERshown123"


@pytest.fixture(scope="module")
def report():
    return fixture_report()


def test_mainnet_is_refused():
    with pytest.raises(NearRecordError, match="testnet"):
        NearRecorder("someone.near", KEY)
    with pytest.raises(NearRecordError, match="testnet RPC"):
        NearRecorder(ACCOUNT, KEY, rpc="https://rpc.mainnet.near.org")
    with pytest.raises(NearRecordError, match="ed25519"):
        NearRecorder(ACCOUNT, "not-a-key")


def test_fingerprint_survives_save_and_reload_and_detects_changes(report):
    digest = report_digest(report)
    reloaded = ResearchReport.model_validate(json.loads(report.model_dump_json()))
    assert report_digest(reloaded) == digest and len(digest) == 64
    reloaded.chain_record = {"anything": "here"}          # the record itself is excluded
    assert report_digest(reloaded) == digest
    reloaded.investment.draft.summary += " (edited)"      # any change to the content is detected
    assert report_digest(reloaded) != digest


def test_fingerprint_is_stable_across_schema_additions(report):
    """A report sealed before `scout` / `affiliations` existed must still verify after the schema grew."""
    import hashlib

    from app.schemas.scout import CompanySignal, ScoutResult
    report.scout = None                                            # a report from before the scout existed
    old_style = report.model_dump(mode="json", exclude={"chain_record"})
    old_style.pop("scout", None)                                   # these fields did not exist when it was sealed
    old_style.pop("sector", None)
    if (old_style.get("investment") or {}).get("draft"):
        old_style["investment"]["draft"].pop("plain_summary", None)
    for m in ((old_style.get("timing") or {}).get("metrics") or []):
        m.pop("closes", None)
    (old_style.get("science") or {}).pop("counting", None)          # added 2026-11-09
    for part in ("science", "risk", "market", "x", "patent", "timing"):
        for src in ((old_style.get(part) or {}).get("sources") or []):
            src.pop("affiliations", None)
    legacy = hashlib.sha256(json.dumps(old_style, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    assert report_digest(report) == legacy
    # real scout data IS part of the fingerprint
    report.scout = ScoutResult(topic=report.topic, status="ok", candidates=[CompanySignal(name="Fixture Co", ticker="FX", sec_listed=True)])
    assert report_digest(report) != legacy


def test_record_writes_one_socialdb_entry(report):
    calls = []
    rec = NearRecorder(ACCOUNT, KEY, signer=lambda m, a, d: calls.append((m, a, d)) or "FixtureTxHash111").record(
        "report_20261108T120719Z", report)
    method, args, deposit = calls[0]
    assert method == "set" and deposit == 10**23
    entry = args["data"][ACCOUNT]["futurescout"]["reports"]["report_20261108T120719Z"]
    assert entry["sha256"] == report_digest(report) and entry["topic"] == "chiplet interconnect"
    assert rec.explorer_url == "https://testnet.nearblocks.io/txns/FixtureTxHash111" and rec.network == "testnet"
    assert "keys" not in json.dumps(rec.as_dict()) and KEY not in json.dumps(rec.as_dict())


def test_read_record_parses_rpc_view_call(report):
    stored = {ACCOUNT: {"futurescout": {"reports": {"report_x": {"sha256": "abc"}}}}}
    seen = {}

    def rpc(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        seen.update(body["params"])
        result = list(json.dumps(stored).encode())
        return httpx.Response(200, json={"jsonrpc": "2.0", "id": "fs", "result": {"result": result}})

    http = httpx.Client(transport=httpx.MockTransport(rpc))
    assert read_record(http, TESTNET_RPC, SOCIALDB_TESTNET, ACCOUNT, "report_x") == {"sha256": "abc"}
    assert seen["account_id"] == SOCIALDB_TESTNET and seen["method_name"] == "get"
    assert json.loads(base64.b64decode(seen["args_base64"]))["keys"] == [f"{ACCOUNT}/futurescout/reports/report_x/**"]


def test_verify_states(report):
    d = report_digest(report)
    assert verify(report, None)["status"] == "not_recorded"
    assert verify(report, {"sha256": d})["status"] == "match"
    assert verify(report, {"sha256": "0" * 64})["status"] == "MISMATCH"


def test_service_never_blocks_and_never_leaks_the_key(report, monkeypatch):
    warnings = []
    assert service.record_on_testnet(Settings(_env_file=None), "k", report, warnings.append) is None
    assert "not set" in warnings[-1]

    def broken(self, method, args, deposit):
        raise NearRecordError(f"boom with {KEY}".replace(KEY, "***"))

    monkeypatch.setattr(NearRecorder, "_sign_with_py_near", broken)
    s = Settings(_env_file=None, near_testnet_account_id=ACCOUNT, near_testnet_private_key=KEY)
    assert service.record_on_testnet(s, "k", report, warnings.append) is None
    assert "record failed" in warnings[-1] and KEY not in warnings[-1]


def test_api_verify_endpoint_detects_tampering(tmp_path, report):
    rec = NearRecorder(ACCOUNT, KEY, signer=lambda m, a, d: "Tx1").record("report_20261108T000000Z", report)
    recorded = report.model_copy(deep=True)
    recorded.chain_record = rec.as_dict()
    (tmp_path / "report_20261108T000000Z.json").write_text(recorded.model_dump_json(), encoding="utf-8")
    onchain = {"sha256": rec.sha256}
    app = create_app(Settings(_env_file=None), store=FileStore(tmp_path), chain_reader=lambda a, k, c: onchain)
    client = TestClient(app)
    res = client.get("/api/runs/report_20261108T000000Z/verify").json()
    assert res["status"] == "match" and res["explorer_url"].endswith("/Tx1") and res["network"] == "testnet"

    tampered = recorded.model_copy(deep=True)
    tampered.investment.draft.summary = "Edited after the fact."
    (tmp_path / "report_20261108T000000Z.json").write_text(tampered.model_dump_json(), encoding="utf-8")
    assert client.get("/api/runs/report_20261108T000000Z/verify").json()["status"] == "MISMATCH"

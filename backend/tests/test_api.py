"""API tests. Reports are SYNTHETIC (FIXTURE) runs from the mocked workflow; no model, no network,
and new runs use a fake runner, so nothing spends NEAR AI credit."""

import threading
import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api import create_app
from app.api.store import DbStore, FileStore
from app.config import Settings
from app.db import Base, make_engine, save_report
from app.report import render_markdown
from tests.test_db import fixture_report

import pytest as _pt
pytestmark = _pt.mark.usefixtures("closed_market")


def settings(**kw):
    return Settings(_env_file=None, near_ai_api_key="k", **kw)


@pytest.fixture(scope="module")
def report():
    return fixture_report()


@pytest.fixture
def file_store(tmp_path, report):
    (tmp_path / "report_20261108T000000Z.json").write_text(report.model_dump_json(), encoding="utf-8")
    (tmp_path / "report_20261108T000000Z.md").write_text(render_markdown(report), encoding="utf-8")
    (tmp_path / "report_broken.json").write_text("{not json", encoding="utf-8")
    return FileStore(tmp_path)


def test_health_and_config_say_what_is_enabled_and_leak_nothing(file_store):
    client = TestClient(create_app(settings(), store=file_store))
    assert client.get("/api/health").json() == {"ok": True, "store": "files"}
    cfg = client.get("/api/config").json()
    assert cfg["run_api_enabled"] is False and cfg["store"] == "files"
    assert set(cfg["agents"]) == {"chief", "science", "risk", "market", "x", "patent", "timing", "investment", "relevance", "trader"}
    assert cfg["agents_not_built"] == [] and "not investment advice" in cfg["disclaimer"]
    assert "near_ai_api_key" not in client.get("/api/config").text.lower()


def test_list_and_detail_from_report_files(file_store, report):
    client = TestClient(create_app(settings(), store=file_store))
    runs = client.get("/api/runs").json()
    assert len(runs) == 1  # the broken file is skipped, not fatal
    card = runs[0]
    assert card["id"] == "report_20261108T000000Z" and card["topic"] == "chiplet interconnect"
    assert card["agents_run"] == ["chief", "science", "risk", "market", "scout", "investment"] and card["findings"] == 6
    detail = client.get(f"/api/runs/{card['id']}").json()
    assert detail["report"]["market"]["findings"][0]["fid"] == "M1"
    assert detail["markdown"].startswith("# FUTURESCOUT AI research report")
    assert client.get("/api/runs", params={"topic": "photonics"}).json() == []


def test_unknown_runs_and_path_tricks_are_404(file_store):
    client = TestClient(create_app(settings(), store=file_store))
    assert client.get("/api/runs/report_nope").status_code == 404
    assert client.get("/api/runs/..%2F..%2Fsecret").status_code == 404
    assert client.get("/api/runs/not_a_report").status_code == 404


def test_database_store_lists_and_loads(tmp_path, report):
    url = f"sqlite:///{(tmp_path / 'fixture.db').as_posix()}"
    Base.metadata.create_all(make_engine(url))
    with Session(make_engine(url)) as session:
        run_id = save_report(session, report, "md-fixture")
        session.commit()
    client = TestClient(create_app(settings(), store=DbStore(url)))
    [card] = client.get("/api/runs").json()
    assert card["id"] == run_id and card["total_cost_usd"] == report.total_cost_usd
    assert client.get(f"/api/runs/{run_id}").json()["markdown"] == "md-fixture"


def test_starting_a_run_is_off_unless_enabled(file_store):
    called = []
    client = TestClient(create_app(settings(), store=file_store, runner=lambda r, s: called.append(r) or "x"))
    res = client.post("/api/runs", json={"topic": "high bandwidth memory"})
    assert res.status_code == 403 and "ENABLE_RUN_API" in res.json()["detail"] and called == []


def test_enabled_run_completes_and_only_one_runs_at_a_time(file_store):
    release = threading.Event()

    def fake_runner(req, s):  # FAKE: stands in for a real (paid) research run
        release.wait(5)
        return "report_fake"

    client = TestClient(create_app(settings(enable_run_api=True), store=file_store, runner=fake_runner))
    assert client.post("/api/runs", json={"topic": "x"}).status_code == 422  # topic too short
    job = client.post("/api/runs", json={"topic": "high bandwidth memory"}).json()
    assert job["status"] == "running"
    assert client.post("/api/runs", json={"topic": "another topic"}).status_code == 409
    release.set()
    for _ in range(50):
        status = client.get(f"/api/jobs/{job['id']}").json()
        if status["status"] != "running":
            break
        time.sleep(0.05)
    assert status["status"] == "done" and status["run_id"] == "report_fake"
    assert client.get("/api/jobs/nope").status_code == 404


def test_failed_run_is_reported_not_hidden(file_store):
    def broken(req, s):
        raise RuntimeError("simulated failure")

    client = TestClient(create_app(settings(enable_run_api=True), store=file_store, runner=broken))
    job = client.post("/api/runs", json={"topic": "high bandwidth memory"}).json()
    for _ in range(50):
        status = client.get(f"/api/jobs/{job['id']}").json()
        if status["status"] != "running":
            break
        time.sleep(0.05)
    assert status["status"] == "failed" and "simulated failure" in status["error"]


def test_missing_near_key_is_a_clear_400(file_store):
    client = TestClient(create_app(Settings(_env_file=None, enable_run_api=True), store=file_store, runner=lambda r, s: "x"))
    res = client.post("/api/runs", json={"topic": "high bandwidth memory"})
    assert res.status_code == 400 and "NEAR_AI_API_KEY" in res.json()["detail"]

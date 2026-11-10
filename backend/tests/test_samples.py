"""A fresh clone has no runs and no database: the API must serve the shipped sample reports and radar instead."""

import json

from fastapi.testclient import TestClient

from app.api import create_app
from app.api import main as api_main
from app.config import Settings
from app.radar import Radar, load_radar
from tests.test_db import fixture_report

import pytest as _pt
pytestmark = _pt.mark.usefixtures("closed_market")


def test_store_falls_back_to_samples_when_runs_is_empty(tmp_path, monkeypatch):
    runs, samples = tmp_path / "runs", tmp_path / "samples"
    runs.mkdir(); samples.mkdir()
    (samples / "report_sample1.json").write_text(fixture_report().model_dump_json(), encoding="utf-8")
    monkeypatch.setattr(api_main.service, "RUNS_DIR", runs)
    monkeypatch.setattr(api_main, "SAMPLES_DIR", samples)
    client = TestClient(create_app(Settings(_env_file=None, near_ai_api_key="k"), portfolio_path=tmp_path / "p.json"))
    rows = client.get("/api/runs").json()
    assert [r["id"] for r in rows] == ["report_sample1"] and rows[0]["topic"] == "chiplet interconnect"
    assert client.get("/api/runs/report_sample1").json()["report"]["topic"] == "chiplet interconnect"
    # once a real run exists, the samples step aside
    (runs / "report_real.json").write_text(fixture_report("real topic").model_dump_json(), encoding="utf-8")
    client2 = TestClient(create_app(Settings(_env_file=None, near_ai_api_key="k"), portfolio_path=tmp_path / "p2.json"))
    assert [r["topic"] for r in client2.get("/api/runs").json()] == ["real topic"]


def test_radar_falls_back_to_the_sample_file(tmp_path, monkeypatch):
    import app.radar as radar_mod
    sample = tmp_path / "radar.json"
    sample.write_text(json.dumps({"generated_at": "2026-11-09T00:00:00Z", "topics": []}), encoding="utf-8")
    monkeypatch.setattr(radar_mod, "RADAR_FILE", tmp_path / "missing.json")
    monkeypatch.setattr(radar_mod, "SAMPLE_RADAR_FILE", sample)
    assert isinstance(load_radar(tmp_path / "missing.json"), Radar)
    assert load_radar(tmp_path / "also-missing.json") is None      # an explicit other path does not fall back


def test_shipped_samples_are_valid_sealed_reports():
    from app.schemas.research import ResearchReport
    files = sorted(api_main.SAMPLES_DIR.glob("report_*.json"))
    assert files, "backend/samples must contain at least one report (scripts/export_samples.py)"
    for f in files:
        r = ResearchReport.model_validate(json.loads(f.read_text(encoding="utf-8")))
        assert r.chain_record and r.chain_record.get("explorer_url"), f"{f.name} is not sealed on NEAR"
    assert (api_main.SAMPLES_DIR / "radar.json").is_file()

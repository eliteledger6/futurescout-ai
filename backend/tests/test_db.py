"""Database tests. They use a throwaway in-memory SQLite database (no PostgreSQL needed) and
SYNTHETIC (FIXTURE) research runs produced by the mocked workflow. PostgreSQL-specific behaviour
(JSONB, the psycopg driver) is NOT exercised here; scripts/db_check.py checks a real server."""

import importlib.util
import json
from datetime import timedelta
from pathlib import Path

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.config import Settings
from app.db import Base, list_runs, load_report, save_report, safe_url
from app.db.models import ErrorRow, FindingRow, Run, Source, Usage
from app.db.session import normalise_url
from app.graph import workflow
from app.report import render_markdown
from tests import test_market_agent as m
from tests.test_workflow import clients as paper_clients
from tests.test_workflow import replies as workflow_replies

BACKEND = Path(__file__).resolve().parents[1]


def fixture_report(topic="chiplet interconnect"):
    script = m.Scripted(workflow_replies(MarketReport={"findings": [
        {"claim": "Fixture Memory Corp says its chiplet interconnect products entered qualification.",
         "label": "verified_fact", "confidence": "medium", "source_ids": [m.FILING_ID],
         "supporting_excerpt": "our chiplet interconnect products entered qualification"}], "limitations": []}))
    router, _ = m.router_for(script)
    oa, ax = paper_clients()
    market = m.MarketAgent(router, m.edgar(), m.gdelt(), companies=m.COMPANIES, now=lambda: m.NOW)  # NOPE ticker -> error row
    return workflow.run_research(topic, router=router, openalex=oa, arxiv=ax, max_papers=10,
                                 market_agent=market, now=lambda: m.NOW)


@pytest.fixture
def migrated():
    """In-memory SQLite with the tables created by the real Alembic migration."""
    engine = create_engine("sqlite://")
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "migrations"))
    cfg.attributes["skip_logging"] = True
    with engine.begin() as conn:
        cfg.attributes["connection"] = conn
        command.upgrade(cfg, "head")
    return engine


def test_migration_matches_the_models_exactly(migrated):
    with migrated.connect() as conn:
        diff = compare_metadata(MigrationContext.configure(conn), Base.metadata)
    assert diff == [], f"migration and models differ: {diff}"


def test_save_and_reload_a_full_run(migrated):
    report = fixture_report()
    markdown = render_markdown(report)
    with Session(migrated) as session:
        run_id = save_report(session, report, markdown)
        session.commit()

    with Session(migrated) as session:
        run = session.get(Run, run_id)
        assert run.topic == "chiplet interconnect" and run.report_markdown == markdown
        assert run.agents_run == ["chief", "science", "risk", "market", "scout", "investment"]
        assert run.score_reportable is False and run.score == report.investment.score.score
        # findings from every agent, with their ids and labels
        rows = session.scalars(select(FindingRow).where(FindingRow.run_id == run_id)).all()
        by_agent = {a: [r.fid for r in rows if r.agent == a] for a in ("science", "risk", "risk_challenge", "market")}
        assert by_agent == {"science": ["S1", "S2"], "risk": ["R1"], "risk_challenge": ["C1", "C2"], "market": ["M1"]}
        c1 = next(r for r in rows if r.fid == "C1")
        assert c1.target_finding_ids == ["S1"] and c1.severity == "high"
        m1 = next(r for r in rows if r.fid == "M1")
        assert m1.label == "verified_fact" and m1.source_ids == [m.FILING_ID]
        # sources found by both Science and Risk are stored once per run
        ids = [s.source_id for s in run.sources]
        assert len(ids) == len(set(ids)) and m.FILING_ID in ids
        expected = {s.id for part in (report.science, report.risk, report.market) for s in part.sources}
        assert set(ids) == expected
        assert session.scalar(select(func.count()).select_from(Usage).where(Usage.run_id == run_id)) == len(report.usage)
        errors = session.scalars(select(ErrorRow).where(ErrorRow.run_id == run_id)).all()
        assert any("NOPE" in e.message for e in errors)

        # the stored JSON reloads into an identical report
        assert load_report(session, run_id).model_dump(mode="json") == report.model_dump(mode="json")
        assert load_report(session, "no-such-run") is None


def test_no_prompts_or_keys_are_stored(migrated):
    report = fixture_report()
    with Session(migrated) as session:
        run_id = save_report(session, report, render_markdown(report))
        session.commit()
        stored = json.dumps(session.get(Run, run_id).report_json)
    for prompt in (BACKEND / "app" / "agents").rglob("*.md"):
        first_line = prompt.read_text(encoding="utf-8").splitlines()[0]
        assert first_line[:60] not in stored, f"prompt text from {prompt.name} was stored"
    assert '"k"' not in stored and "near_ai_api_key" not in stored


def test_list_runs_newest_first_and_topic_filter(migrated):
    first, second = fixture_report("chiplet interconnect"), fixture_report("chiplet interconnect")
    second.generated_at = first.generated_at + timedelta(hours=1)
    second.topic = "fixture photonics"
    with Session(migrated) as session:
        id1 = save_report(session, first)
        id2 = save_report(session, second)
        session.commit()
        runs = list_runs(session)
        assert [r.id for r in runs] == [id2, id1]
        assert runs[1].findings == 6 and runs[1].sources > 0
        assert [r.id for r in list_runs(session, topic="CHIPLET")] == [id1]
        assert len(list_runs(session, limit=1)) == 1


def test_deleting_a_run_deletes_its_rows(migrated):
    report = fixture_report()
    with Session(migrated) as session:
        run_id = save_report(session, report)
        session.commit()
        session.delete(session.get(Run, run_id))
        session.commit()
        assert session.scalar(select(func.count()).select_from(Source)) == 0
        assert session.scalar(select(func.count()).select_from(FindingRow)) == 0


def test_url_helpers_hide_the_password_and_pick_psycopg3():
    url = "postgresql://futurescout:s3cret-FIXTURE@localhost:5432/futurescout"
    assert normalise_url(url).startswith("postgresql+psycopg://")
    assert normalise_url("sqlite://") == "sqlite://"
    assert "s3cret-FIXTURE" not in safe_url(url) and "***" in safe_url(url)


def test_unescaped_at_sign_in_password_gives_a_clear_error_without_the_password():
    from app.config import ConfigError
    with pytest.raises(ConfigError, match="%40") as info:
        normalise_url("postgresql://futurescout:FIXTURE@pw99@localhost:5432/futurescout")
    assert "pw99" not in str(info.value)
    # escaped form is accepted and decodes back to the real password
    from sqlalchemy.engine import make_url
    assert make_url(normalise_url("postgresql://futurescout:FIXTURE%40pw99@localhost:5432/futurescout")).password == "FIXTURE@pw99"


def test_run_research_script_keeps_files_when_database_is_unreachable(capsys):
    spec = importlib.util.spec_from_file_location("run_research_script", BACKEND / "scripts" / "run_research.py")
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)
    report = fixture_report()
    # nothing listens on port 1: connection fails; the password must not be printed
    bad = Settings(_env_file=None, database_url="postgresql://u:pw-FIXTURE-secret@127.0.0.1:1/none")
    assert script.save_to_database(bad, report, "md") is None
    out = capsys.readouterr().out
    assert "could not save" in out and "pw-FIXTURE-secret" not in out
    assert script.save_to_database(Settings(_env_file=None), report, "md") is None
    assert "DATABASE_URL not set" in capsys.readouterr().out


def test_nul_characters_are_stripped_before_saving():
    from app.schemas.research import ResearchReport, strip_control_chars
    rep = ResearchReport(topic="6G\x00 junk", question="a\x07b\tc\nd")
    clean = strip_control_chars(rep)
    assert clean.topic == "6G junk" and clean.question == "ab\tc\nd"
    ok = ResearchReport(topic="fine")
    assert strip_control_chars(ok) is ok

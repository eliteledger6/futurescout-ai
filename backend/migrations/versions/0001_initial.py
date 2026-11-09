"""initial tables: runs, sources, findings, usage, errors

Revision ID: 0001_initial
Revises:
Create Date: 2026-11-08
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

Json = sa.JSON().with_variant(JSONB(), "postgresql")


def upgrade() -> None:
    op.create_table(
        "runs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("topic", sa.String(300), nullable=False),
        sa.Column("question", sa.Text()),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("agents_run", Json, nullable=False),
        sa.Column("agents_not_run", Json, nullable=False),
        sa.Column("score", sa.Float()),
        sa.Column("score_reportable", sa.Boolean(), nullable=False),
        sa.Column("score_coverage", sa.Float()),
        sa.Column("total_cost_usd", sa.Float(), nullable=False),
        sa.Column("report_json", Json, nullable=False),
        sa.Column("report_markdown", sa.Text()),
    )
    op.create_index("ix_runs_topic", "runs", ["topic"])
    op.create_index("ix_runs_generated_at", "runs", ["generated_at"])

    op.create_table(
        "sources",
        sa.Column("run_id", sa.String(36), sa.ForeignKey("runs.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("source_id", sa.String(20), primary_key=True),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("source_name", sa.String(50), nullable=False),
        sa.Column("content_type", sa.String(30), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("published_at", sa.String(10)),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("organization", sa.Text()),
        sa.Column("doi", sa.Text()),
        sa.Column("text_depth", sa.String(20), nullable=False),
        sa.Column("abstract", sa.Text()),
        sa.Column("is_mock", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_sources_source_id", "sources", ["source_id"])

    op.create_table(
        "findings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.String(36), sa.ForeignKey("runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("agent", sa.String(20), nullable=False),
        sa.Column("fid", sa.String(10)),
        sa.Column("claim", sa.Text(), nullable=False),
        sa.Column("label", sa.String(30), nullable=False),
        sa.Column("confidence", sa.String(10), nullable=False),
        sa.Column("horizon", sa.String(20), nullable=False),
        sa.Column("source_ids", Json, nullable=False),
        sa.Column("companies", Json, nullable=False),
        sa.Column("technologies", Json, nullable=False),
        sa.Column("rationale", sa.Text()),
        sa.Column("supporting_excerpt", sa.Text()),
        sa.Column("guard_note", sa.Text()),
        sa.Column("target_finding_ids", Json, nullable=False),
        sa.Column("severity", sa.String(10)),
    )
    op.create_index("ix_findings_run_id", "findings", ["run_id"])
    op.create_index("ix_findings_label", "findings", ["label"])

    op.create_table(
        "usage",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.String(36), sa.ForeignKey("runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("agent", sa.String(30), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("calls", sa.Integer(), nullable=False),
        sa.Column("failed_calls", sa.Integer(), nullable=False),
        sa.Column("prompt_tokens", sa.Integer(), nullable=False),
        sa.Column("completion_tokens", sa.Integer(), nullable=False),
        sa.Column("cost_usd", sa.Float(), nullable=False),
    )
    op.create_index("ix_usage_run_id", "usage", ["run_id"])

    op.create_table(
        "errors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.String(36), sa.ForeignKey("runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("agent", sa.String(30), nullable=False),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("recoverable", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_errors_run_id", "errors", ["run_id"])


def downgrade() -> None:
    for table in ("errors", "usage", "findings", "sources", "runs"):
        op.drop_table(table)

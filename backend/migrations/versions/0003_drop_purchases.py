"""drop purchases: report selling was removed (owner decision 2026-11-10)

Revision ID: 0003_drop_purchases
Revises: 0002_purchases
Create Date: 2026-11-10
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0003_drop_purchases"
down_revision = "0002_purchases"
branch_labels = None
depends_on = None

Json = sa.JSON().with_variant(JSONB(), "postgresql")


def upgrade() -> None:
    op.drop_table("purchases")


def downgrade() -> None:
    op.create_table(
        "purchases",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.String(36), sa.ForeignKey("runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("buyer_account", sa.String(64), nullable=False),
        sa.Column("seller_account", sa.String(64), nullable=False),
        sa.Column("tx_hash", sa.String(64), nullable=False),
        sa.Column("amount_yocto", sa.String(40), nullable=False),
        sa.Column("network", sa.String(16), nullable=False),
        sa.Column("purchased_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sale_record", Json),
        sa.UniqueConstraint("tx_hash", name="uq_purchases_tx_hash"),   # inside create_table: SQLite cannot add it later
    )
    op.create_index("ix_purchases_run_id", "purchases", ["run_id"])
    op.create_index("ix_purchases_buyer_account", "purchases", ["buyer_account"])

"""Database tables (SQLAlchemy 2.0). Written for PostgreSQL; also run on SQLite in tests.

What is stored per research run:
  runs      one row per run: topic, time, agents, score summary, cost, the full report as
            JSON (so it can be reloaded exactly) and the rendered Markdown
  sources   every retrieved source of that run (url, title, type, text depth...)
  findings  every finding (S/R/C/M ids) with its label, confidence and cited source ids
  usage     model calls, tokens and estimated cost per agent/model
  errors    every recorded error
Never stored: prompts, model responses, API keys. (The report contains none of these.)
Schema changes go through Alembic migrations in backend/migrations/.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# JSONB on PostgreSQL (indexable), plain JSON elsewhere
Json = JSON().with_variant(JSONB(), "postgresql")


class Base(DeclarativeBase):
    pass


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # uuid4
    topic: Mapped[str] = mapped_column(String(300), index=True)
    question: Mapped[Optional[str]] = mapped_column(Text)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    agents_run: Mapped[list] = mapped_column(Json, default=list)
    agents_not_run: Mapped[list] = mapped_column(Json, default=list)
    score: Mapped[Optional[float]] = mapped_column(Float)
    score_reportable: Mapped[bool] = mapped_column(Boolean, default=False)
    score_coverage: Mapped[Optional[float]] = mapped_column(Float)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    report_json: Mapped[dict] = mapped_column(Json)
    report_markdown: Mapped[Optional[str]] = mapped_column(Text)

    sources: Mapped[list["Source"]] = relationship(back_populates="run", cascade="all, delete-orphan")
    findings: Mapped[list["FindingRow"]] = relationship(back_populates="run", cascade="all, delete-orphan")
    usage: Mapped[list["Usage"]] = relationship(back_populates="run", cascade="all, delete-orphan")
    errors: Mapped[list["ErrorRow"]] = relationship(back_populates="run", cascade="all, delete-orphan")


class Source(Base):
    __tablename__ = "sources"

    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), primary_key=True)
    source_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)  # src_ + sha1(url)[:10]
    url: Mapped[str] = mapped_column(Text)
    source_name: Mapped[str] = mapped_column(String(50))
    content_type: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(Text)
    published_at: Mapped[Optional[str]] = mapped_column(String(10))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    organization: Mapped[Optional[str]] = mapped_column(Text)
    doi: Mapped[Optional[str]] = mapped_column(Text)
    text_depth: Mapped[str] = mapped_column(String(20))
    abstract: Mapped[Optional[str]] = mapped_column(Text)  # abstract or verbatim filing excerpts
    is_mock: Mapped[bool] = mapped_column(Boolean, default=False)

    run: Mapped[Run] = relationship(back_populates="sources")


class FindingRow(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), index=True)
    agent: Mapped[str] = mapped_column(String(20))         # science | risk | risk_challenge | market
    fid: Mapped[Optional[str]] = mapped_column(String(10))  # S1, R1, C1, M1...
    claim: Mapped[str] = mapped_column(Text)
    label: Mapped[str] = mapped_column(String(30), index=True)
    confidence: Mapped[str] = mapped_column(String(10))
    horizon: Mapped[str] = mapped_column(String(20))
    source_ids: Mapped[list] = mapped_column(Json, default=list)
    companies: Mapped[list] = mapped_column(Json, default=list)
    technologies: Mapped[list] = mapped_column(Json, default=list)
    rationale: Mapped[Optional[str]] = mapped_column(Text)
    supporting_excerpt: Mapped[Optional[str]] = mapped_column(Text)
    guard_note: Mapped[Optional[str]] = mapped_column(Text)
    target_finding_ids: Mapped[list] = mapped_column(Json, default=list)  # risk challenges only
    severity: Mapped[Optional[str]] = mapped_column(String(10))           # risk challenges only

    run: Mapped[Run] = relationship(back_populates="findings")


class Usage(Base):
    __tablename__ = "usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), index=True)
    agent: Mapped[str] = mapped_column(String(30))
    model: Mapped[str] = mapped_column(String(100))
    calls: Mapped[int] = mapped_column(Integer, default=0)
    failed_calls: Mapped[int] = mapped_column(Integer, default=0)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)

    run: Mapped[Run] = relationship(back_populates="usage")


class Purchase(Base):
    """A report bought by a NEAR account: the on-chain payment that unlocked it."""
    __tablename__ = "purchases"
    __table_args__ = (UniqueConstraint("tx_hash", name="uq_purchases_tx_hash"),)   # one payment unlocks one report once

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), index=True)
    buyer_account: Mapped[str] = mapped_column(String(64), index=True)
    seller_account: Mapped[str] = mapped_column(String(64))
    tx_hash: Mapped[str] = mapped_column(String(64))
    amount_yocto: Mapped[str] = mapped_column(String(40))           # exact integer as text (too big for int columns)
    network: Mapped[str] = mapped_column(String(16), default="testnet")
    purchased_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sale_record: Mapped[Optional[dict]] = mapped_column(Json)       # seller's on-chain sale note, if written


class ErrorRow(Base):
    __tablename__ = "errors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), index=True)
    agent: Mapped[str] = mapped_column(String(30))
    source: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    recoverable: Mapped[bool] = mapped_column(Boolean, default=False)

    run: Mapped[Run] = relationship(back_populates="errors")

"""Alembic environment. The URL comes from DATABASE_URL (or, in tests, config.attributes["url"])."""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy.exc import OperationalError

from app.db.models import Base
from app.db.session import make_engine, normalise_url
from app.config import ConfigError, get_settings

config = context.config
if config.config_file_name is not None and not config.attributes.get("skip_logging"):
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = Base.metadata


def _url() -> str:
    url = config.attributes.get("url") or get_settings().database_url_value()
    if not url:
        raise ConfigError("DATABASE_URL is not set in .env")
    return normalise_url(url)


def run_migrations_offline() -> None:
    context.configure(url=_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connection = config.attributes.get("connection")
    if connection is not None:  # tests pass an open connection
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
        return
    engine = make_engine(_url())
    try:
        conn = engine.connect()
    except OperationalError as exc:
        # short, plain message; never the URL or password
        text = str(exc.orig if exc.orig is not None else exc)
        if "password authentication failed" in text:
            hint = ("the password in DATABASE_URL does not match the database user's password. Reset it in SQL Shell "
                    "with ALTER USER futurescout WITH PASSWORD '...'; and put the same password in .env")
        elif "does not exist" in text:
            hint = "the database or user in DATABASE_URL does not exist (see PROJECT_STATUS.md for the CREATE commands)"
        elif "Connection refused" in text or "timeout" in text.lower():
            hint = "PostgreSQL is not running or not on port 5432 (check the 'postgresql' service in Windows Services)"
        else:
            hint = text.splitlines()[0][:200]
        raise SystemExit(f"ERROR: could not connect to the database: {hint}") from None
    with conn:
        context.configure(connection=conn, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

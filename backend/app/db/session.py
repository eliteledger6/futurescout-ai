"""Database connection. The URL comes only from DATABASE_URL (it contains a password)."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.config import ConfigError, Settings, get_settings

CONNECT_TIMEOUT_S = 5


def check_url(url: str) -> None:
    """Catch the common mistake of an unescaped '@' (or similar) in the password.
    The message never contains the URL or the password."""
    rest = url.split("://", 1)[-1]
    authority = rest.split("/", 1)[0]
    if authority.count("@") > 1:
        raise ConfigError(
            "DATABASE_URL looks wrong: the password seems to contain '@'. In .env, write each '@' inside the "
            "password as %40 (keep the last '@' before localhost). Likewise ':' -> %3A, '/' -> %2F, '#' -> %23, "
            "'?' -> %3F, '%' -> %25. Or choose a password with letters and digits only."
        )


def normalise_url(url: str) -> str:
    """Use the psycopg 3 driver for plain postgresql:// URLs (SQLAlchemy would pick psycopg2)."""
    check_url(url)
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


def safe_url(url: str) -> str:
    """The URL with the password hidden, for messages."""
    try:
        return make_url(url).render_as_string(hide_password=True)
    except Exception:  # noqa: BLE001
        return "(unparseable DATABASE_URL)"


def make_engine(url: Optional[str] = None, settings: Optional[Settings] = None) -> Engine:
    if url is None:
        url = (settings or get_settings()).database_url_value()
    if not url:
        raise ConfigError("DATABASE_URL is not set. Add it to .env, e.g. "
                          "DATABASE_URL=postgresql://futurescout:YOUR_PASSWORD@localhost:5432/futurescout")
    url = normalise_url(url)
    # fail fast when the server is down (without this, Windows waited ~2 minutes; measured)
    connect_args = {"connect_timeout": CONNECT_TIMEOUT_S} if url.startswith("postgresql") else {}
    return create_engine(url, pool_pre_ping=True, connect_args=connect_args)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)

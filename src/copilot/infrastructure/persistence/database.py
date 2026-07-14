"""Engine, session factory, and declarative base.

Centralises SQLAlchemy setup so the rest of infrastructure just asks for a
``sessionmaker``. The URL comes from ``Settings`` (``DATABASE_URL``), so SQLite
locally and Postgres in compose are the same code path (ADR-0006/0007).
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from copilot.config.settings import Settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def create_db_engine(settings: Settings) -> Engine:
    url = settings.database_url
    connect_args: dict[str, object] = {}

    if url.startswith("sqlite"):
        # Allow use across FastAPI's threadpool and ensure the parent dir exists.
        connect_args["check_same_thread"] = False
        db_path = url.split("sqlite:///")[-1]
        if db_path and db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    return create_engine(url, connect_args=connect_args, future=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)


def init_db(engine: Engine) -> None:
    """Create tables from metadata (local convenience; Alembic owns prod)."""
    # Import models so they register on Base.metadata before create_all.
    from copilot.infrastructure.persistence import models  # noqa: F401

    Base.metadata.create_all(engine)


@contextmanager
def session_scope(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    """Transactional scope: commit on success, rollback on error, always close."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

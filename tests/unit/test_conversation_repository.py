"""Integration-ish test of the SQLAlchemy repository against in-memory SQLite.

Uses a real engine (StaticPool so every session shares one in-memory DB) to prove
the ORM mapping and upsert logic, without any external service.
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from copilot.domain.entities.conversation import Conversation
from copilot.domain.value_objects.message import Role
from copilot.infrastructure.persistence.database import create_session_factory, init_db
from copilot.infrastructure.persistence.repositories import SqlAlchemyConversationRepository


@pytest.fixture()
def repo() -> SqlAlchemyConversationRepository:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    init_db(engine)
    return SqlAlchemyConversationRepository(create_session_factory(engine))


@pytest.mark.integration
def test_save_and_get_roundtrip(repo: SqlAlchemyConversationRepository) -> None:
    conv = Conversation(title="demo")
    conv.add(Role.SYSTEM, "system")
    conv.add(Role.USER, "hello")
    conv.add(Role.ASSISTANT, "hi")
    repo.save(conv)

    loaded = repo.get(conv.id)
    assert loaded is not None
    assert loaded.title == "demo"
    assert [(m.role, m.content) for m in loaded.messages] == [
        (Role.SYSTEM, "system"),
        (Role.USER, "hello"),
        (Role.ASSISTANT, "hi"),
    ]


@pytest.mark.integration
def test_get_missing_returns_none(repo: SqlAlchemyConversationRepository) -> None:
    assert repo.get("nope") is None


@pytest.mark.integration
def test_save_is_upsert_and_replaces_messages(repo: SqlAlchemyConversationRepository) -> None:
    conv = Conversation()
    conv.add(Role.USER, "one")
    repo.save(conv)

    conv.add(Role.ASSISTANT, "answer")
    conv.title = "updated"
    repo.save(conv)

    loaded = repo.get(conv.id)
    assert loaded is not None
    assert loaded.title == "updated"
    assert [m.content for m in loaded.messages] == ["one", "answer"]


@pytest.mark.integration
def test_list_returns_newest_first(repo: SqlAlchemyConversationRepository) -> None:
    from datetime import datetime, timedelta, timezone

    older = Conversation(created_at=datetime.now(timezone.utc) - timedelta(hours=1))
    older.add(Role.USER, "old")
    newer = Conversation(created_at=datetime.now(timezone.utc))
    newer.add(Role.USER, "new")
    repo.save(older)
    repo.save(newer)

    listed = repo.list(limit=10)
    assert [c.id for c in listed] == [newer.id, older.id]

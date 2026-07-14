"""Composition root (Dependency Injection container).

The only module that knows which concrete adapters implement which ports.
Adapters are built lazily and cached: importing the container is cheap, and we
open no HTTP client or database engine until something actually needs it.
"""

from __future__ import annotations

from functools import lru_cache

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from copilot.application.use_cases.chat import ChatUseCase
from copilot.application.use_cases.converse import ConverseUseCase
from copilot.config.settings import Settings, get_settings
from copilot.domain.ports.llm import LLMPort
from copilot.domain.ports.repositories import ConversationRepository
from copilot.infrastructure.llm.factory import create_llm
from copilot.infrastructure.persistence.database import (
    create_db_engine,
    create_session_factory,
    init_db,
)
from copilot.infrastructure.persistence.repositories import SqlAlchemyConversationRepository


class Container:
    """Builds and holds application singletons from a ``Settings`` instance."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._llm: LLMPort | None = None
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None

    # --- infrastructure singletons ---
    @property
    def llm(self) -> LLMPort:
        if self._llm is None:
            self._llm = create_llm(self.settings)
        return self._llm

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_db_engine(self.settings)
            # Local convenience: ensure tables exist. Alembic owns prod schema.
            init_db(self._engine)
        return self._engine

    @property
    def session_factory(self) -> sessionmaker[Session]:
        if self._session_factory is None:
            self._session_factory = create_session_factory(self.engine)
        return self._session_factory

    def conversation_repository(self) -> ConversationRepository:
        return SqlAlchemyConversationRepository(self.session_factory)

    # --- use case factories ---
    def chat_use_case(self) -> ChatUseCase:
        return ChatUseCase(self.llm)

    def converse_use_case(self) -> ConverseUseCase:
        return ConverseUseCase(self.llm, self.conversation_repository())


@lru_cache
def get_container() -> Container:
    """Process-wide container singleton."""
    return Container()

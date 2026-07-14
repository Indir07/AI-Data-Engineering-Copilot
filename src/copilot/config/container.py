"""Composition root (Dependency Injection container).

The only module that knows which concrete adapters implement which ports.
Adapters are built lazily and cached: importing the container is cheap, and we
open no HTTP client, database engine, or LangGraph graph until something needs it.
"""

from __future__ import annotations

from functools import lru_cache

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from copilot.agents.orchestrator.registry import AgentRegistry
from copilot.application.use_cases.chat import ChatUseCase
from copilot.application.use_cases.converse import ConverseUseCase
from copilot.config.settings import Settings, get_settings
from copilot.domain.ports.llm import LLMPort
from copilot.domain.ports.repositories import ConversationRepository
from copilot.domain.ports.retriever import RetrieverPort
from copilot.infrastructure.llm.factory import create_llm
from copilot.infrastructure.persistence.database import (
    create_db_engine,
    create_session_factory,
    init_db,
)
from copilot.infrastructure.persistence.repositories import SqlAlchemyConversationRepository
from copilot.infrastructure.vectorstore.null_retriever import NullRetriever


class Container:
    """Builds and holds application singletons from a ``Settings`` instance."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._llm: LLMPort | None = None
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None
        self._retriever: RetrieverPort | None = None
        self._orchestrator: object | None = None

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
            init_db(self._engine)  # local convenience; Alembic owns prod schema
        return self._engine

    @property
    def session_factory(self) -> sessionmaker[Session]:
        if self._session_factory is None:
            self._session_factory = create_session_factory(self.engine)
        return self._session_factory

    @property
    def retriever(self) -> RetrieverPort:
        # Phase 5 replaces NullRetriever with the ChromaDB-backed retriever.
        if self._retriever is None:
            self._retriever = NullRetriever()
        return self._retriever

    def conversation_repository(self) -> ConversationRepository:
        return SqlAlchemyConversationRepository(self.session_factory)

    def agent_registry(self) -> AgentRegistry:
        return AgentRegistry(self.llm, self.retriever)

    # --- use case factories ---
    def chat_use_case(self) -> ChatUseCase:
        return ChatUseCase(self.llm)

    def converse_use_case(self) -> ConverseUseCase:
        return ConverseUseCase(self.llm, self.conversation_repository())

    def run_agent_use_case(self):
        # Lazy imports: only touch LangGraph when the agent flow is actually used.
        from copilot.agents.orchestrator.orchestrator import AgentOrchestrator
        from copilot.application.use_cases.run_agent import RunAgentUseCase

        if self._orchestrator is None:
            self._orchestrator = AgentOrchestrator(self.agent_registry())
        return RunAgentUseCase(self._orchestrator)


@lru_cache
def get_container() -> Container:
    """Process-wide container singleton."""
    return Container()

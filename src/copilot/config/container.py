"""Composition root (Dependency Injection container).

The only module that knows which concrete adapters implement which ports.
Adapters are built lazily and cached: importing the container is cheap, and we
open no HTTP client, DB engine, embedding model, Chroma index, or LangGraph graph
until something actually needs it. Heavy libraries (sentence-transformers,
chromadb, langgraph) are imported inside the builder methods for the same reason.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from copilot.agents.orchestrator.registry import AgentRegistry
from copilot.application.use_cases.chat import ChatUseCase
from copilot.application.use_cases.converse import ConverseUseCase
from copilot.application.use_cases.ingest_document import IngestDocumentUseCase
from copilot.application.use_cases.search_documents import SearchDocumentsUseCase
from copilot.config.settings import Settings, get_settings
from copilot.domain.ports.embedding import EmbedderPort
from copilot.domain.ports.llm import LLMPort
from copilot.domain.ports.repositories import ConversationRepository
from copilot.domain.ports.retriever import RetrieverPort
from copilot.domain.ports.vector_store import VectorStorePort
from copilot.infrastructure.llm.factory import create_llm
from copilot.infrastructure.persistence.database import (
    create_db_engine,
    create_session_factory,
    init_db,
)
from copilot.infrastructure.persistence.repositories import SqlAlchemyConversationRepository

if TYPE_CHECKING:
    from copilot.application.use_cases.run_agent import RunAgentUseCase


class Container:
    """Builds and holds application singletons from a ``Settings`` instance."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._llm: LLMPort | None = None
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None
        self._embedder: EmbedderPort | None = None
        self._vector_store: VectorStorePort | None = None
        self._retriever: RetrieverPort | None = None
        self._orchestrator: object | None = None

    # --- LLM ---
    @property
    def llm(self) -> LLMPort:
        if self._llm is None:
            self._llm = create_llm(self.settings)
        return self._llm

    # --- persistence ---
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

    def conversation_repository(self) -> ConversationRepository:
        return SqlAlchemyConversationRepository(self.session_factory)

    # --- RAG ---
    @property
    def embedder(self) -> EmbedderPort:
        if self._embedder is None:
            from copilot.infrastructure.embeddings.sentence_transformer import (
                SentenceTransformerEmbedder,
            )

            self._embedder = SentenceTransformerEmbedder(
                self.settings.embedding_model, self.settings.embedding_device
            )
        return self._embedder

    @property
    def vector_store(self) -> VectorStorePort:
        if self._vector_store is None:
            from copilot.infrastructure.vectorstore.chroma_store import ChromaVectorStore

            self._vector_store = ChromaVectorStore(
                self.settings.chroma_persist_dir, self.settings.chroma_collection
            )
        return self._vector_store

    @property
    def retriever(self) -> RetrieverPort:
        if self._retriever is None:
            from copilot.rag.retrieval.retriever import VectorRetriever

            self._retriever = VectorRetriever(self.embedder, self.vector_store)
        return self._retriever

    def ingest_document_use_case(self) -> IngestDocumentUseCase:
        from copilot.rag.chunking.fixed_size import FixedSizeChunker

        chunker = FixedSizeChunker(self.settings.rag_chunk_size, self.settings.rag_chunk_overlap)
        return IngestDocumentUseCase(self.embedder, self.vector_store, chunker)

    def search_documents_use_case(self) -> SearchDocumentsUseCase:
        return SearchDocumentsUseCase(self.retriever)

    # --- agents ---
    def agent_registry(self) -> AgentRegistry:
        return AgentRegistry(self.llm, self.retriever)

    def run_agent_use_case(self) -> RunAgentUseCase:
        # Lazy: only touch LangGraph when the agent flow is actually used.
        from copilot.agents.orchestrator.orchestrator import AgentOrchestrator
        from copilot.application.use_cases.run_agent import RunAgentUseCase

        if self._orchestrator is None:
            self._orchestrator = AgentOrchestrator(self.agent_registry())
        return RunAgentUseCase(self._orchestrator)

    # --- plain use cases ---
    def chat_use_case(self) -> ChatUseCase:
        return ChatUseCase(self.llm)

    def converse_use_case(self) -> ConverseUseCase:
        return ConverseUseCase(self.llm, self.conversation_repository())


@lru_cache
def get_container() -> Container:
    """Process-wide container singleton."""
    return Container()

"""FastAPI dependency providers.

Thin bridge between FastAPI's ``Depends`` system and the composition root. Tests
override these with ``app.dependency_overrides`` to inject fakes without touching
the container.
"""

from __future__ import annotations

from copilot.application.use_cases.chat import ChatUseCase
from copilot.application.use_cases.converse import ConverseUseCase
from copilot.application.use_cases.ingest_document import IngestDocumentUseCase
from copilot.application.use_cases.run_agent import RunAgentUseCase
from copilot.application.use_cases.search_documents import SearchDocumentsUseCase
from copilot.config.container import get_container
from copilot.domain.ports.repositories import ConversationRepository
from copilot.domain.ports.vector_store import VectorStorePort


def get_chat_use_case() -> ChatUseCase:
    return get_container().chat_use_case()


def get_converse_use_case() -> ConverseUseCase:
    return get_container().converse_use_case()


def get_conversation_repository() -> ConversationRepository:
    return get_container().conversation_repository()


def get_run_agent_use_case() -> RunAgentUseCase:
    return get_container().run_agent_use_case()


def get_ingest_document_use_case() -> IngestDocumentUseCase:
    return get_container().ingest_document_use_case()


def get_search_documents_use_case() -> SearchDocumentsUseCase:
    return get_container().search_documents_use_case()


def get_vector_store() -> VectorStorePort:
    return get_container().vector_store

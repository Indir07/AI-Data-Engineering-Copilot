"""FastAPI dependency providers.

Thin bridge between FastAPI's ``Depends`` system and the composition root. Tests
override these with ``app.dependency_overrides`` to inject fakes without touching
the container.
"""

from __future__ import annotations

from copilot.application.use_cases.chat import ChatUseCase
from copilot.application.use_cases.converse import ConverseUseCase
from copilot.application.use_cases.run_agent import RunAgentUseCase
from copilot.config.container import get_container
from copilot.domain.ports.repositories import ConversationRepository


def get_chat_use_case() -> ChatUseCase:
    return get_container().chat_use_case()


def get_converse_use_case() -> ConverseUseCase:
    return get_container().converse_use_case()


def get_conversation_repository() -> ConversationRepository:
    return get_container().conversation_repository()


def get_run_agent_use_case() -> RunAgentUseCase:
    return get_container().run_agent_use_case()

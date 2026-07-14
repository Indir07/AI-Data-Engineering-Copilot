"""FastAPI dependency providers.

Thin bridge between FastAPI's ``Depends`` system and the composition root. Tests
override these with ``app.dependency_overrides`` to inject fakes without touching
the container.
"""

from __future__ import annotations

from copilot.application.use_cases.chat import ChatUseCase
from copilot.config.container import get_container


def get_chat_use_case() -> ChatUseCase:
    return get_container().chat_use_case()

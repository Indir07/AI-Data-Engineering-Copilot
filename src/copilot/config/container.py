"""Composition root (Dependency Injection container).

This is the *only* module that knows which concrete adapters implement which
ports. Everything else depends on abstractions. Wiring lives in one place so the
dependency graph is explicit and swapping an implementation (e.g. a fake LLM in
tests, pgvector later) is a one-line change here.

Adapters are built lazily and cached: importing the container is cheap, and we
don't open an HTTP client until something actually needs the LLM.
"""

from __future__ import annotations

from functools import lru_cache

from copilot.application.use_cases.chat import ChatUseCase
from copilot.config.settings import Settings, get_settings
from copilot.domain.ports.llm import LLMPort
from copilot.infrastructure.llm.factory import create_llm


class Container:
    """Builds and holds application singletons from a ``Settings`` instance."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._llm: LLMPort | None = None

    # --- infrastructure singletons ---
    @property
    def llm(self) -> LLMPort:
        if self._llm is None:
            self._llm = create_llm(self.settings)
        return self._llm

    # --- use case factories ---
    def chat_use_case(self) -> ChatUseCase:
        return ChatUseCase(self.llm)


@lru_cache
def get_container() -> Container:
    """Process-wide container singleton."""
    return Container()

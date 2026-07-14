"""DTOs for the persistence-aware conversation flow."""

from __future__ import annotations

from dataclasses import dataclass

from copilot.domain.value_objects.completion import CompletionResult


@dataclass(frozen=True, slots=True)
class ConverseRequestDTO:
    """Input to :class:`copilot.application.use_cases.converse.ConverseUseCase`."""

    prompt: str
    conversation_id: str | None = None
    system: str | None = None
    model: str | None = None
    temperature: float | None = None


@dataclass(frozen=True, slots=True)
class ConversationTurn:
    """Result of one persisted turn: which conversation, and the LLM reply."""

    conversation_id: str
    result: CompletionResult

"""Chat use case — the first end-to-end application flow.

A use case is a single unit of application behaviour. It depends only on the
``LLMPort`` abstraction, so it can be unit-tested with a fake and works against
any backend. Agents (Phase 6) build on this same pattern.
"""

from __future__ import annotations

from copilot.application.dto.chat import ChatRequestDTO
from copilot.application.services.prompts import BASE_SYSTEM_PROMPT
from copilot.domain.entities.conversation import Conversation
from copilot.domain.ports.llm import LLMPort
from copilot.domain.value_objects.completion import CompletionResult
from copilot.domain.value_objects.message import Role


class ChatUseCase:
    """Assemble a conversation and get a grounded completion from the LLM."""

    def __init__(self, llm: LLMPort) -> None:
        self._llm = llm

    def execute(self, request: ChatRequestDTO) -> CompletionResult:
        conversation = Conversation(messages=list(request.history))
        conversation.with_system_prompt(request.system or BASE_SYSTEM_PROMPT)
        conversation.add(Role.USER, request.prompt)

        return self._llm.complete(
            conversation.messages,
            model=request.model,
            temperature=request.temperature,
        )

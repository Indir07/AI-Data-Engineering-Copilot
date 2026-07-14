"""Converse use case — chat with durable history.

Loads (or creates) a conversation, appends the user turn, calls the LLM, appends
the assistant turn, and persists the whole aggregate. Depends only on the
``LLMPort`` and ``ConversationRepository`` abstractions, so it is unit-testable
with fakes and agnostic to the database.
"""

from __future__ import annotations

from copilot.application.dto.conversation import ConversationTurn, ConverseRequestDTO
from copilot.application.services.prompts import BASE_SYSTEM_PROMPT
from copilot.domain.entities.conversation import Conversation
from copilot.domain.exceptions import NotFoundError
from copilot.domain.ports.llm import LLMPort
from copilot.domain.ports.repositories import ConversationRepository
from copilot.domain.value_objects.message import Role


class ConverseUseCase:
    def __init__(self, llm: LLMPort, conversations: ConversationRepository) -> None:
        self._llm = llm
        self._conversations = conversations

    def execute(self, request: ConverseRequestDTO) -> ConversationTurn:
        conversation = self._load_or_create(request.conversation_id)
        conversation.with_system_prompt(request.system or BASE_SYSTEM_PROMPT)
        conversation.add(Role.USER, request.prompt)

        result = self._llm.complete(
            conversation.messages,
            model=request.model,
            temperature=request.temperature,
        )

        conversation.add(Role.ASSISTANT, result.content)
        conversation.ensure_title(fallback="Conversation")
        self._conversations.save(conversation)

        return ConversationTurn(conversation_id=conversation.id, result=result)

    def _load_or_create(self, conversation_id: str | None) -> Conversation:
        if conversation_id is None:
            return Conversation()
        existing = self._conversations.get(conversation_id)
        if existing is None:
            raise NotFoundError(f"Conversation {conversation_id!r} not found")
        return existing

"""Conversations router — persistent chat history.

POST /conversations   send a message (new or continuing) and persist the turn
GET  /conversations   list recent conversations
GET  /conversations/{id}  fetch a conversation's messages

Transport-only: map schema ↔ DTO, invoke use case / repository, map back.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from copilot.application.dto.conversation import ConverseRequestDTO
from copilot.application.use_cases.converse import ConverseUseCase
from copilot.domain.exceptions import NotFoundError
from copilot.domain.ports.repositories import ConversationRepository
from copilot.domain.value_objects.message import Role
from copilot.presentation.api.dependencies import (
    get_conversation_repository,
    get_converse_use_case,
)
from copilot.presentation.api.schemas.conversation import (
    ConversationDetail,
    ConversationMessage,
    ConversationSummary,
    ConverseRequest,
    ConverseResponse,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConverseResponse, summary="Send a message (persisted)")
def converse(
    request: ConverseRequest,
    use_case: ConverseUseCase = Depends(get_converse_use_case),
) -> ConverseResponse:
    turn = use_case.execute(
        ConverseRequestDTO(
            prompt=request.prompt,
            conversation_id=request.conversation_id,
            system=request.system,
            model=request.model,
            temperature=request.temperature,
        )
    )
    return ConverseResponse(
        conversation_id=turn.conversation_id,
        content=turn.result.content,
        model=turn.result.model,
        prompt_tokens=turn.result.prompt_tokens,
        completion_tokens=turn.result.completion_tokens,
    )


@router.get("", response_model=list[ConversationSummary], summary="List conversations")
def list_conversations(
    limit: int = 50,
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> list[ConversationSummary]:
    return [
        ConversationSummary(
            id=c.id,
            title=c.title,
            created_at=c.created_at,
            message_count=sum(1 for m in c.messages if m.role is not Role.SYSTEM),
        )
        for c in repo.list(limit=limit)
    ]


@router.get("/{conversation_id}", response_model=ConversationDetail, summary="Get a conversation")
def get_conversation(
    conversation_id: str,
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationDetail:
    conversation = repo.get(conversation_id)
    if conversation is None:
        raise NotFoundError(f"Conversation {conversation_id!r} not found")
    return ConversationDetail(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        messages=[
            ConversationMessage(role=m.role, content=m.content)
            for m in conversation.messages
            if m.role is not Role.SYSTEM
        ],
    )

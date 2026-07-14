"""Chat router — first feature endpoint backed by the LLM.

The router's only job is transport: validate input, map schema → DTO, invoke the
use case, map result → schema. No business logic lives here.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from copilot.application.dto.chat import ChatRequestDTO
from copilot.application.use_cases.chat import ChatUseCase
from copilot.presentation.api.dependencies import get_chat_use_case
from copilot.presentation.api.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, summary="Chat with the copilot")
def chat(
    request: ChatRequest,
    use_case: ChatUseCase = Depends(get_chat_use_case),
) -> ChatResponse:
    result = use_case.execute(
        ChatRequestDTO(
            prompt=request.prompt,
            system=request.system,
            history=[m.to_domain() for m in request.history],
            model=request.model,
            temperature=request.temperature,
        )
    )
    return ChatResponse(
        content=result.content,
        model=result.model,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
    )

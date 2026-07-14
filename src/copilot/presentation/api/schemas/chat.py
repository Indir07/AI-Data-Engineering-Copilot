"""Pydantic request/response schemas for the chat endpoint.

These are the transport contract (validated, documented in OpenAPI). The router
maps them to application DTOs so the core stays framework-free.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from copilot.domain.value_objects.message import Message, Role


class MessageSchema(BaseModel):
    role: Role
    content: str = Field(min_length=1)

    def to_domain(self) -> Message:
        return Message(role=self.role, content=self.content)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, examples=["Generate SQL to get top 10 customers by revenue"])
    system: str | None = Field(default=None, description="Override the default system prompt")
    history: list[MessageSchema] = Field(default_factory=list)
    model: str | None = Field(default=None, description="Override the configured model")
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    content: str
    model: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

"""Pydantic schemas for the /conversations endpoints."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from copilot.domain.value_objects.message import Role


class ConverseRequest(BaseModel):
    prompt: str = Field(min_length=1)
    conversation_id: str | None = Field(
        default=None, description="Continue an existing conversation; omit to start a new one"
    )
    system: str | None = None
    model: str | None = None
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)


class ConverseResponse(BaseModel):
    conversation_id: str
    content: str
    model: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


class ConversationMessage(BaseModel):
    role: Role
    content: str


class ConversationSummary(BaseModel):
    id: str
    title: str | None
    created_at: datetime
    message_count: int


class ConversationDetail(BaseModel):
    id: str
    title: str | None
    created_at: datetime
    messages: list[ConversationMessage]

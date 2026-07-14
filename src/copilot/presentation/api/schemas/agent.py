"""Pydantic schemas for the /agents endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field

from copilot.domain.value_objects.enums import AgentType, SqlDialect


class CitationSchema(BaseModel):
    source: str
    snippet: str


class AgentRunRequest(BaseModel):
    prompt: str = Field(min_length=1)
    dialect: SqlDialect | None = Field(default=None, description="Only used by the SQL agent")
    model: str | None = None
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    use_rag: bool = False


class AgentRunResponse(BaseModel):
    agent: AgentType
    content: str
    model: str
    citations: list[CitationSchema] = Field(default_factory=list)
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


class AgentInfo(BaseModel):
    agent: AgentType
    description: str

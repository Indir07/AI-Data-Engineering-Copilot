"""Agent request/result value types (application layer)."""

from __future__ import annotations

from dataclasses import dataclass, field

from copilot.domain.value_objects.enums import AgentType, SqlDialect
from copilot.domain.value_objects.retrieval import Citation


@dataclass(frozen=True, slots=True)
class AgentRequest:
    """A task handed to a specialist agent."""

    agent: AgentType
    prompt: str
    dialect: SqlDialect | None = None
    model: str | None = None
    temperature: float | None = None
    use_rag: bool = False


@dataclass(frozen=True, slots=True)
class AgentResult:
    """The agent's answer plus provenance."""

    agent: AgentType
    content: str
    model: str
    citations: list[Citation] = field(default_factory=list)
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

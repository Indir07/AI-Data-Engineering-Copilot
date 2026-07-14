"""SQL agent: generate / explain / debug / optimize / translate SQL."""

from __future__ import annotations

from copilot.agents.base.agent import BaseAgent
from copilot.agents.base.types import AgentRequest
from copilot.domain.value_objects.enums import AgentType, SqlDialect
from copilot.domain.value_objects.retrieval import RetrievedChunk


class SqlAgent(BaseAgent):
    agent_type = AgentType.SQL

    def build_user_prompt(self, request: AgentRequest, chunks: list[RetrievedChunk]) -> str:
        dialect = (request.dialect or SqlDialect.ANSI).value
        header = f"Target SQL dialect: {dialect}."
        base = super().build_user_prompt(request, chunks)
        return f"{header}\n\n{base}"

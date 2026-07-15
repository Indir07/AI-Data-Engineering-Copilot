"""RAG agent: answer strictly from retrieved context, always cite.

Unlike other agents, this one always attempts retrieval (grounding is its whole
purpose) regardless of the request's ``use_rag`` flag.
"""

from __future__ import annotations

from copilot.agents.base.agent import BaseAgent
from copilot.agents.base.types import AgentRequest
from copilot.domain.value_objects.enums import AgentType
from copilot.domain.value_objects.retrieval import RetrievedChunk


class RagAgent(BaseAgent):
    agent_type = AgentType.RAG

    def _gather_context(self, request: AgentRequest) -> list[RetrievedChunk]:
        if self._retriever is None:
            return []
        return self._retriever.retrieve(request.prompt)

    def build_user_prompt(self, request: AgentRequest, chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return (
                "No indexed documents matched the question. Tell the user no "
                f"relevant context found; answer cautiously.\n\nQuestion:\n{request.prompt}"
            )
        return super().build_user_prompt(request, chunks)

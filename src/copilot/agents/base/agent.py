"""BaseAgent — the template-method shared by every specialist.

The algorithm is fixed (gather context → build prompt → call LLM → wrap result);
subclasses override only the parts that differ. This is the Open/Closed
Principle: adding an agent means adding a subclass, not editing this file.

Agents depend only on the ``LLMPort`` and ``RetrieverPort`` abstractions.
"""

from __future__ import annotations

from copilot.agents.base.types import AgentRequest, AgentResult
from copilot.application.services.prompts import system_prompt_for
from copilot.domain.ports.llm import LLMPort
from copilot.domain.ports.retriever import RetrieverPort
from copilot.domain.value_objects.enums import AgentType
from copilot.domain.value_objects.message import Message, Role
from copilot.domain.value_objects.retrieval import Citation, RetrievedChunk


class BaseAgent:
    #: Set by each subclass.
    agent_type: AgentType

    def __init__(self, llm: LLMPort, retriever: RetrieverPort | None = None) -> None:
        self._llm = llm
        self._retriever = retriever

    # --- template method (do not override) ---
    def handle(self, request: AgentRequest) -> AgentResult:
        chunks = self._gather_context(request)
        messages = [
            Message(Role.SYSTEM, system_prompt_for(self.agent_type)),
            Message(Role.USER, self.build_user_prompt(request, chunks)),
        ]
        completion = self._llm.complete(
            messages, model=request.model, temperature=request.temperature
        )
        return AgentResult(
            agent=self.agent_type,
            content=completion.content,
            model=completion.model,
            citations=[c.as_citation() for c in chunks],
            prompt_tokens=completion.prompt_tokens,
            completion_tokens=completion.completion_tokens,
        )

    # --- overridable hooks ---
    def build_user_prompt(self, request: AgentRequest, chunks: list[RetrievedChunk]) -> str:
        """Assemble the user message. Override to add agent-specific framing."""
        if not chunks:
            return request.prompt
        return f"{self._context_block(chunks)}\n\nTask:\n{request.prompt}"

    def _gather_context(self, request: AgentRequest) -> list[RetrievedChunk]:
        """Retrieve grounding context when requested and a retriever is present."""
        if request.use_rag and self._retriever is not None:
            return self._retriever.retrieve(request.prompt)
        return []

    @staticmethod
    def _context_block(chunks: list[RetrievedChunk]) -> str:
        lines = ["Use the following context to ground your answer. Cite sources by name."]
        for i, chunk in enumerate(chunks, start=1):
            lines.append(f"[{i}] ({chunk.source}) {chunk.text.strip()}")
        return "\n".join(lines)

    @staticmethod
    def _citations(chunks: list[RetrievedChunk]) -> list[Citation]:
        return [c.as_citation() for c in chunks]

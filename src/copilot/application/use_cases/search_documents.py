"""Search-documents use case: semantic search over the indexed corpus."""

from __future__ import annotations

from copilot.domain.ports.retriever import RetrieverPort
from copilot.domain.value_objects.retrieval import RetrievedChunk


class SearchDocumentsUseCase:
    def __init__(self, retriever: RetrieverPort) -> None:
        self._retriever = retriever

    def execute(self, query: str, *, top_k: int = 5) -> list[RetrievedChunk]:
        return self._retriever.retrieve(query, top_k=top_k)

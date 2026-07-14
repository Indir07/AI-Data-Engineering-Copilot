"""No-op retriever used until the RAG engine (Phase 5) is wired in.

Satisfies ``RetrieverPort`` structurally and always returns no context, so the
RAG agent degrades gracefully ("no documents indexed yet") instead of failing.
"""

from __future__ import annotations

from copilot.domain.value_objects.retrieval import RetrievedChunk


class NullRetriever:
    def retrieve(self, query: str, *, top_k: int = 5) -> list[RetrievedChunk]:
        return []

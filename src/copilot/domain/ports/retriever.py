"""Retriever port — the domain's contract for semantic search.

Agents depend on this abstraction to fetch grounding context. The real
ChromaDB-backed implementation arrives in Phase 5; a ``NullRetriever`` (returns
nothing) lets the agents run before then.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from copilot.domain.value_objects.retrieval import RetrievedChunk


@runtime_checkable
class RetrieverPort(Protocol):
    def retrieve(self, query: str, *, top_k: int = 5) -> list[RetrievedChunk]:
        """Return the ``top_k`` most relevant chunks for ``query`` (may be empty)."""
        ...

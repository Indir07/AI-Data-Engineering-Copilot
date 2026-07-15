"""Retrieval value objects (shared by RAG engine and agents).

Kept in the domain so agents can consume grounding context and emit citations
without knowing anything about ChromaDB or embeddings (those are Phase 5
infrastructure details behind the ``RetrieverPort``).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    """A chunk of a document returned by semantic search."""

    text: str
    source: str
    score: float

    def as_citation(self) -> Citation:
        snippet = self.text.strip().replace("\n", " ")
        return Citation(source=self.source, snippet=snippet[:200])


@dataclass(frozen=True, slots=True)
class Citation:
    """A user-facing reference to grounding context."""

    source: str
    snippet: str

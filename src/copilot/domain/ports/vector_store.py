"""Vector store port — the domain's contract for a vector index.

ChromaDB implements this today; pgvector/Qdrant could tomorrow (ADR-0004). The
application depends only on this interface.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from copilot.domain.value_objects.document import Chunk
from copilot.domain.value_objects.retrieval import RetrievedChunk


@runtime_checkable
class VectorStorePort(Protocol):
    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Upsert chunks with their embeddings."""
        ...

    def query(self, embedding: list[float], *, top_k: int = 5) -> list[RetrievedChunk]:
        """Return the ``top_k`` most similar chunks to ``embedding``."""
        ...

    def count(self) -> int:
        """Total number of indexed chunks."""
        ...

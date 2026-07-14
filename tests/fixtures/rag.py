"""RAG test doubles: a deterministic embedder and an in-memory vector store."""

from __future__ import annotations

from copilot.domain.value_objects.document import Chunk
from copilot.domain.value_objects.retrieval import RetrievedChunk


class FakeEmbedder:
    """Deterministic 2-D embeddings so tests need no model."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(t)), 1.0] for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return [float(len(text)), 1.0]


class FakeVectorStore:
    """In-memory vector store; query returns the most recently added chunks."""

    def __init__(self) -> None:
        self._chunks: list[Chunk] = []

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        assert len(chunks) == len(embeddings)
        self._chunks.extend(chunks)

    def query(self, embedding: list[float], *, top_k: int = 5) -> list[RetrievedChunk]:
        return [
            RetrievedChunk(text=c.text, source=c.source, score=1.0) for c in self._chunks[:top_k]
        ]

    def count(self) -> int:
        return len(self._chunks)

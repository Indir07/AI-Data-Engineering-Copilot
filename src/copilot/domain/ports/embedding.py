"""Embedder port — the domain's contract for turning text into vectors.

Keeps the embedding model (Sentence-Transformers today, a managed API tomorrow)
behind an interface so ingestion and retrieval never import the model library.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmbedderPort(Protocol):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of documents/chunks."""
        ...

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query string."""
        ...

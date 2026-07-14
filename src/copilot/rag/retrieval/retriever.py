"""Vector retriever — composes an embedder and a vector store.

Implements the domain ``RetrieverPort`` by embedding the query and asking the
vector store for the nearest chunks. This is what the RAG agent uses to ground
its answers.
"""

from __future__ import annotations

from copilot.domain.ports.embedding import EmbedderPort
from copilot.domain.ports.vector_store import VectorStorePort
from copilot.domain.value_objects.retrieval import RetrievedChunk


class VectorRetriever:
    def __init__(self, embedder: EmbedderPort, vector_store: VectorStorePort) -> None:
        self._embedder = embedder
        self._vector_store = vector_store

    def retrieve(self, query: str, *, top_k: int = 5) -> list[RetrievedChunk]:
        embedding = self._embedder.embed_query(query)
        return self._vector_store.query(embedding, top_k=top_k)

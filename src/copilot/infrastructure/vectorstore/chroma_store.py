"""ChromaDB implementation of ``VectorStorePort`` (ADR-0004).

Persistent, embedded, zero-ops. Distances use cosine; we convert distance to a
similarity score for the domain ``RetrievedChunk``.
"""

from __future__ import annotations

from typing import Any

from copilot.domain.exceptions import RetrievalError
from copilot.domain.value_objects.document import Chunk
from copilot.domain.value_objects.retrieval import RetrievedChunk


class ChromaVectorStore:
    def __init__(self, persist_dir: str, collection_name: str) -> None:
        import chromadb

        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection = self._client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        self._collection.add(
            ids=[c.id for c in chunks],
            embeddings=embeddings,
            documents=[c.text for c in chunks],
            metadatas=[dict(c.metadata()) for c in chunks],
        )

    def query(self, embedding: list[float], *, top_k: int = 5) -> list[RetrievedChunk]:
        try:
            result: dict[str, Any] = self._collection.query(
                query_embeddings=[embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as exc:  # noqa: BLE001 - normalise to a domain error
            raise RetrievalError(f"Vector store query failed: {exc}") from exc

        documents = (result.get("documents") or [[]])[0]
        metadatas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]

        chunks: list[RetrievedChunk] = []
        for text, meta, distance in zip(documents, metadatas, distances, strict=False):
            source = str((meta or {}).get("source", "unknown"))
            chunks.append(
                RetrievedChunk(text=text, source=source, score=1.0 - float(distance))
            )
        return chunks

    def count(self) -> int:
        return int(self._collection.count())

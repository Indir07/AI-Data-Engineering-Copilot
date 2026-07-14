"""Retriever test doubles."""

from __future__ import annotations

from copilot.domain.value_objects.retrieval import RetrievedChunk


class FakeRetriever:
    """Returns a fixed set of chunks, ignoring the query."""

    def __init__(self, chunks: list[RetrievedChunk] | None = None) -> None:
        self._chunks = chunks or [
            RetrievedChunk(text="Bronze holds raw ingested data.", source="medallion.md", score=0.9)
        ]

    def retrieve(self, query: str, *, top_k: int = 5) -> list[RetrievedChunk]:
        return self._chunks[:top_k]

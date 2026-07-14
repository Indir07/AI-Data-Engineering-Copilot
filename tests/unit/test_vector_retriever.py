"""Unit test for the VectorRetriever (embedder + vector store composition)."""

from __future__ import annotations

import pytest

from copilot.domain.value_objects.document import Chunk
from copilot.rag.retrieval.retriever import VectorRetriever
from tests.fixtures.rag import FakeEmbedder, FakeVectorStore


@pytest.mark.unit
def test_retrieve_embeds_query_and_returns_chunks() -> None:
    store = FakeVectorStore()
    store.add(
        [Chunk(id="1", text="silver layer is cleaned data", source="med.md", index=0)],
        [[1.0, 1.0]],
    )
    retriever = VectorRetriever(FakeEmbedder(), store)

    results = retriever.retrieve("what is the silver layer?", top_k=3)

    assert results and results[0].source == "med.md"
    assert "silver" in results[0].text

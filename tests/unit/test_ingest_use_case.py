"""Unit tests for IngestDocumentUseCase with fakes (no model, no Chroma)."""

from __future__ import annotations

import pytest

from copilot.application.use_cases.ingest_document import IngestDocumentUseCase
from copilot.domain.exceptions import CopilotError
from copilot.rag.chunking.fixed_size import FixedSizeChunker
from copilot.rag.ingestion.loaders import UnsupportedDocumentError
from tests.fixtures.rag import FakeEmbedder, FakeVectorStore


def _use_case(store: FakeVectorStore) -> IngestDocumentUseCase:
    return IngestDocumentUseCase(FakeEmbedder(), store, FixedSizeChunker(chunk_size=50, overlap=10))


@pytest.mark.unit
def test_ingest_txt_indexes_chunks() -> None:
    store = FakeVectorStore()
    result = _use_case(store).execute("notes.txt", b"the bronze layer holds raw data " * 20)

    assert result.source == "notes.txt"
    assert result.chunks_indexed > 0
    assert store.count() == result.chunks_indexed


@pytest.mark.unit
def test_unsupported_extension_rejected() -> None:
    with pytest.raises(UnsupportedDocumentError):
        _use_case(FakeVectorStore()).execute("image.png", b"\x89PNG")


@pytest.mark.unit
def test_empty_document_rejected() -> None:
    with pytest.raises(CopilotError):
        _use_case(FakeVectorStore()).execute("empty.txt", b"    ")

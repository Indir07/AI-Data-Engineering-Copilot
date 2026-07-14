"""Ingest-document use case: load → chunk → embed → index.

Depends on the ``EmbedderPort`` and ``VectorStorePort`` abstractions plus a
chunker; the concrete model and vector DB are injected by the composition root.
"""

from __future__ import annotations

from uuid import uuid4

from copilot.application.dto.rag import IngestResult
from copilot.domain.exceptions import CopilotError
from copilot.domain.ports.embedding import EmbedderPort
from copilot.domain.ports.vector_store import VectorStorePort
from copilot.rag.chunking.fixed_size import FixedSizeChunker


class IngestDocumentUseCase:
    def __init__(
        self,
        embedder: EmbedderPort,
        vector_store: VectorStorePort,
        chunker: FixedSizeChunker,
    ) -> None:
        self._embedder = embedder
        self._vector_store = vector_store
        self._chunker = chunker

    def execute(self, filename: str, data: bytes, content_type: str | None = None) -> IngestResult:
        # Imported here so the app import graph doesn't pull pypdf eagerly.
        from copilot.rag.ingestion.loaders import load_text

        text = load_text(filename, data, content_type)
        chunks = self._chunker.split(text, source=filename)
        if not chunks:
            raise CopilotError(f"No extractable text found in {filename!r}")

        embeddings = self._embedder.embed_documents([c.text for c in chunks])
        self._vector_store.add(chunks, embeddings)

        return IngestResult(
            document_id=str(uuid4()), source=filename, chunks_indexed=len(chunks)
        )

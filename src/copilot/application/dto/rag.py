"""DTOs for RAG ingestion and search."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IngestResult:
    document_id: str
    source: str
    chunks_indexed: int

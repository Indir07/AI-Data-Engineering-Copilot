"""Fixed-size character chunker with overlap.

Chosen for the first iteration because it is simple, deterministic, and easy to
debug (ADR-0004). Overlap preserves context across chunk boundaries. Semantic or
recursive chunking can replace this later without touching callers — it only has
to produce ``Chunk`` objects.
"""

from __future__ import annotations

from uuid import uuid4

from copilot.domain.value_objects.document import Chunk


class FixedSizeChunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 120) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self._chunk_size = chunk_size
        self._overlap = overlap

    def split(self, text: str, *, source: str) -> list[Chunk]:
        normalized = text.strip()
        if not normalized:
            return []

        step = self._chunk_size - self._overlap
        chunks: list[Chunk] = []
        index = 0
        for start in range(0, len(normalized), step):
            piece = normalized[start : start + self._chunk_size].strip()
            if not piece:
                continue
            chunks.append(Chunk(id=str(uuid4()), text=piece, source=source, index=index))
            index += 1
            if start + self._chunk_size >= len(normalized):
                break
        return chunks

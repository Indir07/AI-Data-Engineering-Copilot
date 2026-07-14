"""Document/chunk value objects for the RAG engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Chunk:
    """A slice of a source document, ready to embed and index."""

    id: str
    text: str
    source: str
    index: int

    def metadata(self) -> dict[str, str | int]:
        return {"source": self.source, "index": self.index}

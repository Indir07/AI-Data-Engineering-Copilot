"""Unit tests for FixedSizeChunker."""

from __future__ import annotations

import pytest

from copilot.rag.chunking.fixed_size import FixedSizeChunker


@pytest.mark.unit
def test_empty_text_yields_no_chunks() -> None:
    assert FixedSizeChunker().split("   ", source="x.txt") == []


@pytest.mark.unit
def test_splits_with_overlap_and_metadata() -> None:
    text = "abcdefghij" * 30  # 300 chars
    chunks = FixedSizeChunker(chunk_size=100, overlap=20).split(text, source="doc.md")

    assert len(chunks) >= 3
    assert all(c.source == "doc.md" for c in chunks)
    assert [c.index for c in chunks] == list(range(len(chunks)))
    assert len({c.id for c in chunks}) == len(chunks)  # unique ids
    assert all(len(c.text) <= 100 for c in chunks)


@pytest.mark.unit
def test_overlap_must_be_smaller_than_chunk_size() -> None:
    with pytest.raises(ValueError):
        FixedSizeChunker(chunk_size=100, overlap=100)

"""Pydantic schemas for the RAG endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    document_id: str
    source: str
    chunks_indexed: int


class RetrievedChunkSchema(BaseModel):
    text: str
    source: str
    score: float


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, gt=0, le=50)


class SearchResponse(BaseModel):
    query: str
    results: list[RetrievedChunkSchema]


class RagStats(BaseModel):
    indexed_chunks: int

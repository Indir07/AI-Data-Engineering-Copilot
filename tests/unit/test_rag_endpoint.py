"""Endpoint tests for /upload, /rag/search, /rag/stats with fakes injected."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from copilot.application.dto.rag import IngestResult
from copilot.domain.value_objects.retrieval import RetrievedChunk
from copilot.presentation.api.dependencies import (
    get_ingest_document_use_case,
    get_search_documents_use_case,
    get_vector_store,
)
from copilot.presentation.api.main import create_app
from tests.fixtures.rag import FakeVectorStore


class _FakeIngest:
    def execute(self, filename: str, data: bytes, content_type=None) -> IngestResult:
        return IngestResult(document_id="doc-1", source=filename, chunks_indexed=3)


class _FakeSearch:
    def execute(self, query: str, *, top_k: int = 5) -> list[RetrievedChunk]:
        return [RetrievedChunk(text="silver = cleaned", source="med.md", score=0.87)]


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    store = FakeVectorStore()
    app.dependency_overrides[get_ingest_document_use_case] = _FakeIngest
    app.dependency_overrides[get_search_documents_use_case] = _FakeSearch
    app.dependency_overrides[get_vector_store] = lambda: store
    return TestClient(app)


@pytest.mark.unit
def test_upload_returns_index_summary(client: TestClient) -> None:
    resp = client.post(
        "/upload",
        files={"file": ("notes.txt", b"bronze raw data", "text/plain")},
    )
    assert resp.status_code == 200
    assert resp.json()["chunks_indexed"] == 3


@pytest.mark.unit
def test_search_returns_results(client: TestClient) -> None:
    resp = client.post("/rag/search", json={"query": "silver layer", "top_k": 3})
    assert resp.status_code == 200
    body = resp.json()
    assert body["results"][0]["source"] == "med.md"


@pytest.mark.unit
def test_stats_reports_count(client: TestClient) -> None:
    resp = client.get("/rag/stats")
    assert resp.status_code == 200
    assert resp.json()["indexed_chunks"] == 0

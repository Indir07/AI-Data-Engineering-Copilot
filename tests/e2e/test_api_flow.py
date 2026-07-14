"""End-to-end journey through the API.

Exercises the *real* use cases, agents, SQLite-free in-memory repo, chunker and
retriever — only the external adapters (LLM, embedding model, Chroma) are faked.
This is the closest thing to a full-system test that still runs anywhere.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from copilot.agents.base.types import AgentRequest, AgentResult
from copilot.agents.orchestrator.registry import AgentRegistry
from copilot.application.use_cases.chat import ChatUseCase
from copilot.application.use_cases.converse import ConverseUseCase
from copilot.application.use_cases.ingest_document import IngestDocumentUseCase
from copilot.application.use_cases.run_agent import RunAgentUseCase
from copilot.application.use_cases.search_documents import SearchDocumentsUseCase
from copilot.presentation.api.dependencies import (
    get_chat_use_case,
    get_conversation_repository,
    get_converse_use_case,
    get_ingest_document_use_case,
    get_run_agent_use_case,
    get_search_documents_use_case,
    get_vector_store,
)
from copilot.presentation.api.main import create_app
from copilot.rag.chunking.fixed_size import FixedSizeChunker
from copilot.rag.retrieval.retriever import VectorRetriever
from tests.fixtures.fakes import FakeLLM
from tests.fixtures.rag import FakeEmbedder, FakeVectorStore
from tests.fixtures.repositories import InMemoryConversationRepository


class _DirectOrchestrator:
    """Real agent dispatch without LangGraph (keeps e2e dependency-light)."""

    def __init__(self, registry: AgentRegistry) -> None:
        self._registry = registry

    def run(self, request: AgentRequest) -> AgentResult:
        return self._registry.get(request.agent).handle(request)


@pytest.fixture()
def client() -> TestClient:
    llm = FakeLLM(reply="SELECT 1;")
    repo = InMemoryConversationRepository()
    embedder = FakeEmbedder()
    store = FakeVectorStore()

    app = create_app()
    o = app.dependency_overrides
    o[get_chat_use_case] = lambda: ChatUseCase(llm)
    o[get_converse_use_case] = lambda: ConverseUseCase(llm, repo)
    o[get_conversation_repository] = lambda: repo
    o[get_run_agent_use_case] = lambda: RunAgentUseCase(_DirectOrchestrator(AgentRegistry(llm)))
    o[get_ingest_document_use_case] = lambda: IngestDocumentUseCase(
        embedder, store, FixedSizeChunker(chunk_size=120, overlap=20)
    )
    o[get_search_documents_use_case] = lambda: SearchDocumentsUseCase(
        VectorRetriever(embedder, store)
    )
    o[get_vector_store] = lambda: store
    return TestClient(app)


@pytest.mark.e2e
def test_health_and_root(client: TestClient) -> None:
    assert client.get("/health").status_code == 200
    assert client.get("/").json()["service"] == "ai-data-engineering-copilot"


@pytest.mark.e2e
def test_chat_flow(client: TestClient) -> None:
    resp = client.post("/chat", json={"prompt": "give me a query"})
    assert resp.status_code == 200
    assert resp.json()["content"] == "SELECT 1;"


@pytest.mark.e2e
def test_conversation_persistence_flow(client: TestClient) -> None:
    first = client.post("/conversations", json={"prompt": "one"}).json()
    cid = first["conversation_id"]
    client.post("/conversations", json={"prompt": "two", "conversation_id": cid})

    listing = client.get("/conversations").json()
    assert any(item["id"] == cid for item in listing)

    detail = client.get(f"/conversations/{cid}").json()
    user_turns = [m["content"] for m in detail["messages"] if m["role"] == "user"]
    assert user_turns == ["one", "two"]


@pytest.mark.e2e
def test_rag_flow(client: TestClient) -> None:
    payload = b"the silver layer holds cleaned data " * 10
    up = client.post("/upload", files={"file": ("medallion.txt", payload, "text/plain")})
    assert up.status_code == 200
    indexed = up.json()["chunks_indexed"]
    assert indexed > 0

    search = client.post("/rag/search", json={"query": "silver layer", "top_k": 3})
    assert search.status_code == 200
    assert search.json()["results"]

    assert client.get("/rag/stats").json()["indexed_chunks"] == indexed


@pytest.mark.e2e
def test_agents_flow(client: TestClient) -> None:
    assert len(client.get("/agents").json()) == 8
    run = client.post("/agents/sql", json={"prompt": "top customers", "dialect": "postgres"})
    assert run.status_code == 200
    assert run.json()["content"] == "SELECT 1;"

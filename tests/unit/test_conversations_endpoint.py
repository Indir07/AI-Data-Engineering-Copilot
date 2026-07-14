"""Endpoint tests for /conversations with fakes injected via dependency override."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from copilot.application.use_cases.converse import ConverseUseCase
from copilot.presentation.api.dependencies import (
    get_conversation_repository,
    get_converse_use_case,
)
from copilot.presentation.api.main import create_app
from tests.fixtures.fakes import FakeLLM
from tests.fixtures.repositories import InMemoryConversationRepository


@pytest.fixture()
def client_and_repo() -> tuple[TestClient, InMemoryConversationRepository]:
    repo = InMemoryConversationRepository()
    use_case = ConverseUseCase(FakeLLM(reply="stored reply"), repo)

    app = create_app()
    app.dependency_overrides[get_converse_use_case] = lambda: use_case
    app.dependency_overrides[get_conversation_repository] = lambda: repo
    return TestClient(app), repo


@pytest.mark.unit
def test_converse_then_fetch_roundtrip(client_and_repo) -> None:
    client, _ = client_and_repo

    posted = client.post("/conversations", json={"prompt": "generate sql"})
    assert posted.status_code == 200
    cid = posted.json()["conversation_id"]
    assert posted.json()["content"] == "stored reply"

    listed = client.get("/conversations")
    assert listed.status_code == 200
    assert any(item["id"] == cid for item in listed.json())

    detail = client.get(f"/conversations/{cid}")
    assert detail.status_code == 200
    roles = [m["role"] for m in detail.json()["messages"]]
    assert roles == ["user", "assistant"]  # system prompt filtered out


@pytest.mark.unit
def test_get_unknown_conversation_returns_404(client_and_repo) -> None:
    client, _ = client_and_repo
    resp = client.get("/conversations/missing")
    assert resp.status_code == 404
    assert resp.json()["error"] == "NotFoundError"

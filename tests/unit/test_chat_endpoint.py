"""Endpoint test for POST /chat with the LLM dependency overridden by a fake."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from copilot.application.use_cases.chat import ChatUseCase
from copilot.presentation.api.dependencies import get_chat_use_case
from copilot.presentation.api.main import create_app
from tests.fixtures.fakes import FakeLLM


@pytest.fixture()
def app_with_fake_llm():
    app = create_app()
    app.dependency_overrides[get_chat_use_case] = lambda: ChatUseCase(
        FakeLLM(reply="hello from fake")
    )
    yield app
    app.dependency_overrides.clear()


@pytest.mark.unit
def test_chat_returns_200_and_content(app_with_fake_llm) -> None:
    client = TestClient(app_with_fake_llm)
    resp = client.post("/chat", json={"prompt": "generate a query"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["content"] == "hello from fake"
    assert body["model"] == "fake-model"


@pytest.mark.unit
def test_chat_rejects_empty_prompt(app_with_fake_llm) -> None:
    client = TestClient(app_with_fake_llm)
    resp = client.post("/chat", json={"prompt": ""})
    assert resp.status_code == 422  # Pydantic validation (min_length=1)

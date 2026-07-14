"""Verify domain exceptions map to the right HTTP status codes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from copilot.application.use_cases.chat import ChatUseCase
from copilot.presentation.api.dependencies import get_chat_use_case
from copilot.presentation.api.main import create_app
from tests.fixtures.failing import RaisingLLM, TimingOutLLM


def _client_with(llm) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_chat_use_case] = lambda: ChatUseCase(llm)
    return TestClient(app, raise_server_exceptions=False)


@pytest.mark.unit
def test_llm_error_maps_to_502() -> None:
    resp = _client_with(RaisingLLM()).post("/chat", json={"prompt": "hi"})
    assert resp.status_code == 502
    assert resp.json()["error"] == "LLMError"


@pytest.mark.unit
def test_llm_timeout_maps_to_504() -> None:
    resp = _client_with(TimingOutLLM()).post("/chat", json={"prompt": "hi"})
    assert resp.status_code == 504
    assert resp.json()["error"] == "LLMTimeoutError"

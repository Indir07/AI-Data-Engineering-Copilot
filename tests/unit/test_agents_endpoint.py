"""Endpoint tests for /agents with the run-agent use case overridden by a fake."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from copilot.agents.base.types import AgentRequest, AgentResult
from copilot.domain.value_objects.enums import AgentType
from copilot.domain.value_objects.retrieval import Citation
from copilot.presentation.api.dependencies import get_run_agent_use_case
from copilot.presentation.api.main import create_app


class _FakeRunAgent:
    def execute(self, request: AgentRequest) -> AgentResult:
        return AgentResult(
            agent=request.agent,
            content=f"result for {request.agent.value}",
            model="fake-model",
            citations=[Citation(source="doc.md", snippet="ctx")],
            prompt_tokens=1,
            completion_tokens=2,
        )


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_run_agent_use_case] = _FakeRunAgent
    return TestClient(app)


@pytest.mark.unit
def test_list_agents_returns_all(client: TestClient) -> None:
    resp = client.get("/agents")
    assert resp.status_code == 200
    agents = {item["agent"] for item in resp.json()}
    assert agents == {a.value for a in AgentType}


@pytest.mark.unit
def test_run_sql_agent(client: TestClient) -> None:
    resp = client.post("/agents/sql", json={"prompt": "top 10 customers", "dialect": "postgres"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent"] == "sql"
    assert body["content"] == "result for sql"
    assert body["citations"][0]["source"] == "doc.md"


@pytest.mark.unit
def test_unknown_agent_is_422(client: TestClient) -> None:
    resp = client.post("/agents/not-an-agent", json={"prompt": "x"})
    assert resp.status_code == 422  # enum path param validation

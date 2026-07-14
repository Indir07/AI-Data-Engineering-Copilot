"""Unit tests for the system endpoints (no external infra required)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from copilot import __version__


@pytest.mark.unit
def test_health_ok(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["version"] == __version__
    assert body["llm_model"]  # non-empty


@pytest.mark.unit
def test_root_banner(client: TestClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["service"] == "ai-data-engineering-copilot"

"""Shared pytest fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from copilot.presentation.api.main import create_app


@pytest.fixture()
def client() -> TestClient:
    """A TestClient over a freshly-built app instance."""
    return TestClient(create_app())

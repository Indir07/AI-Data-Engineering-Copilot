"""Thin HTTP client the Streamlit UI uses to talk to the FastAPI backend.

The UI is a pure client of the REST API (see docs/ARCHITECTURE.md); all logic
lives behind the API. Keeping the calls here keeps ``app.py`` about layout.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Static fallback so the sidebar renders even if the API is down.
FALLBACK_AGENTS: list[dict[str, str]] = [
    {"agent": "sql", "description": "Generate, explain, debug, optimize, translate SQL."},
    {"agent": "pyspark", "description": "Generate & optimize PySpark; explain Spark errors."},
    {"agent": "etl", "description": "Bronze/Silver/Gold, incremental, CDC, SCD."},
    {"agent": "data_quality", "description": "Great Expectations/Soda suites, profiling."},
    {"agent": "documentation", "description": "READMEs, architecture, pipeline docs."},
    {"agent": "airflow", "description": "DAGs, scheduling, retries, task groups, sensors."},
    {"agent": "dbt", "description": "Models, tests, sources, snapshots, macros."},
    {"agent": "rag", "description": "Answer from your uploaded documents with citations."},
]


def _client() -> httpx.Client:
    return httpx.Client(base_url=API_BASE_URL, timeout=180.0)


def get_health() -> dict[str, Any]:
    with _client() as c:
        resp = c.get("/health")
        resp.raise_for_status()
        return resp.json()


def list_agents() -> list[dict[str, str]]:
    try:
        with _client() as c:
            resp = c.get("/agents")
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return FALLBACK_AGENTS


def run_agent(agent: str, payload: dict[str, Any]) -> dict[str, Any]:
    with _client() as c:
        resp = c.post(f"/agents/{agent}", json=payload)
        resp.raise_for_status()
        return resp.json()


def upload_document(filename: str, data: bytes, content_type: str) -> dict[str, Any]:
    """Best-effort upload; returns a 'not available' marker until Phase 5 ships /upload."""
    with _client() as c:
        resp = c.post("/upload", files={"file": (filename, data, content_type)})
        if resp.status_code == 404:
            return {"available": False}
        resp.raise_for_status()
        return {"available": True, **resp.json()}

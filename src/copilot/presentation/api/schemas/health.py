"""Response schemas for the health endpoint."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Liveness/readiness payload returned by ``GET /health``."""

    status: str = Field(examples=["ok"])
    version: str = Field(examples=["0.1.0"])
    app_env: str = Field(examples=["local"])
    llm_model: str = Field(examples=["qwen2.5-coder:7b-instruct"])

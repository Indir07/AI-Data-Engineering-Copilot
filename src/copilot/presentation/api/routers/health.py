"""Health/readiness router.

Kept dependency-light on purpose: orchestrators and load balancers hit this to
decide if the process is alive. It reports the active model so a quick curl
confirms which LLM the container is wired to.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from copilot import __version__
from copilot.config import Settings, get_settings
from copilot.presentation.api.schemas.health import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse, summary="Liveness probe")
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=__version__,
        app_env=settings.app_env,
        llm_model=settings.llm_model,
    )

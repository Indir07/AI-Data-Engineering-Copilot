"""FastAPI application factory.

The app is built by a factory (``create_app``) rather than a module-level global
so tests can construct isolated instances and override dependencies. Routers are
included here; business logic lives behind use cases wired via the composition
root (``copilot.config.container``).
"""

from __future__ import annotations

from fastapi import FastAPI

from copilot import __version__
from copilot.config import configure_logging, get_settings
from copilot.presentation.api.errors import register_exception_handlers
from copilot.presentation.api.routers import chat, health


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(level=settings.log_level, json_logs=settings.is_prod)

    app = FastAPI(
        title="AI Data Engineering Copilot",
        description=(
            "An AI teammate that automates data engineering tasks "
            "(SQL, PySpark, ETL, dbt, Airflow, data quality, docs) via local "
            "LLMs and RAG."
        ),
        version=__version__,
    )

    register_exception_handlers(app)

    # System routers + feature routers. More feature routers land in later phases.
    app.include_router(health.router)
    app.include_router(chat.router)

    @app.get("/", tags=["system"], summary="Service banner")
    def root() -> dict[str, str]:
        return {
            "service": "ai-data-engineering-copilot",
            "version": __version__,
            "docs": "/docs",
            "health": "/health",
        }

    return app


# ASGI entrypoint: `uvicorn copilot.presentation.api.main:app`
app = create_app()

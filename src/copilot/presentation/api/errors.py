"""Domain-exception → HTTP mapping.

One place translates domain errors to HTTP responses (RFC-7807-ish problem
JSON). The domain raises meaningful exceptions; transport concerns (status codes)
stay in the presentation layer.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from copilot.domain.exceptions import (
    ConfigurationError,
    CopilotError,
    LLMError,
    LLMTimeoutError,
    NotFoundError,
    RetrievalError,
)

# Domain exception → HTTP status. Order matters: most specific first.
_STATUS_MAP: list[tuple[type[CopilotError], int]] = [
    (LLMTimeoutError, 504),
    (LLMError, 502),
    (RetrievalError, 502),
    (NotFoundError, 404),
    (ConfigurationError, 500),
    (CopilotError, 500),
]


def _status_for(exc: CopilotError) -> int:
    for exc_type, status in _STATUS_MAP:
        if isinstance(exc, exc_type):
            return status
    return 500


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CopilotError)
    async def _handle_copilot_error(_: Request, exc: CopilotError) -> JSONResponse:
        status = _status_for(exc)
        return JSONResponse(
            status_code=status,
            content={
                "error": exc.__class__.__name__,
                "detail": str(exc),
                "status": status,
            },
        )

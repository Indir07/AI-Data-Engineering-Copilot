"""Domain exception hierarchy.

Business/infrastructure failures are raised as domain exceptions so the core
never leaks framework-specific errors (e.g. ``httpx.HTTPError``). The
presentation layer maps these to HTTP responses in one place
(``presentation/api/errors.py``), keeping transport concerns out of the domain.
"""

from __future__ import annotations


class CopilotError(Exception):
    """Base class for all application errors."""


class ConfigurationError(CopilotError):
    """Invalid or unsupported configuration (e.g. unknown LLM provider)."""


class NotFoundError(CopilotError):
    """A requested resource does not exist."""


class LLMError(CopilotError):
    """The language model backend failed to produce a response."""


class LLMTimeoutError(LLMError):
    """The language model backend did not respond within the timeout."""


class RetrievalError(CopilotError):
    """The RAG/vector-store layer failed (used from Phase 5)."""

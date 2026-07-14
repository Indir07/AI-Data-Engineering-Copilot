"""LLM provider factory (Strategy selection).

Turns configuration into a concrete ``LLMPort``. Adding a new backend (e.g. an
OpenAI-compatible endpoint) means adding a branch here and a new adapter — no
changes to the application or domain. This is the single seam where model
runtime choice lives (see ADR-0005).
"""

from __future__ import annotations

from copilot.config.settings import Settings
from copilot.domain.exceptions import ConfigurationError
from copilot.domain.ports.llm import LLMPort
from copilot.infrastructure.llm.ollama_provider import OllamaProvider


def create_llm(settings: Settings) -> LLMPort:
    if settings.llm_provider == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            default_model=settings.llm_model,
            timeout=float(settings.llm_request_timeout),
            default_temperature=settings.llm_temperature,
            default_max_tokens=settings.llm_max_tokens,
        )
    raise ConfigurationError(f"Unsupported LLM provider: {settings.llm_provider!r}")

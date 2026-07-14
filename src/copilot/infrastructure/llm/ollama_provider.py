"""Ollama adapter implementing :class:`LLMPort`.

Talks to a local Ollama server over its ``/api/chat`` HTTP endpoint (see
ADR-0002). All transport errors are translated into domain exceptions so callers
never see ``httpx`` types. An ``httpx.Client`` can be injected for testing.
"""

from __future__ import annotations

from collections.abc import Sequence

import httpx

from copilot.domain.exceptions import LLMError, LLMTimeoutError
from copilot.domain.value_objects.completion import CompletionResult
from copilot.domain.value_objects.message import Message


class OllamaProvider:
    """Concrete ``LLMPort`` backed by a local Ollama runtime."""

    def __init__(
        self,
        *,
        base_url: str,
        default_model: str,
        timeout: float = 120.0,
        default_temperature: float = 0.1,
        default_max_tokens: int = 2048,
        client: httpx.Client | None = None,
    ) -> None:
        self._default_model = default_model
        self._default_temperature = default_temperature
        self._default_max_tokens = default_max_tokens
        self._client = client or httpx.Client(base_url=base_url, timeout=timeout)

    def complete(
        self,
        messages: Sequence[Message],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        payload = {
            "model": model or self._default_model,
            "messages": [{"role": m.role.value, "content": m.content} for m in messages],
            "stream": False,
            "options": {
                "temperature": (
                    temperature if temperature is not None else self._default_temperature
                ),
                "num_predict": max_tokens or self._default_max_tokens,
            },
        }

        try:
            response = self._client.post("/api/chat", json=payload)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(f"Ollama request timed out: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise LLMError(
                f"Ollama returned {exc.response.status_code}: {exc.response.text[:200]}"
            ) from exc
        except httpx.HTTPError as exc:
            raise LLMError(f"Ollama request failed: {exc}") from exc

        try:
            data = response.json()
            content = data["message"]["content"]
        except (ValueError, KeyError, TypeError) as exc:
            raise LLMError(f"Malformed Ollama response: {exc}") from exc

        return CompletionResult(
            content=content,
            model=data.get("model", payload["model"]),
            prompt_tokens=data.get("prompt_eval_count"),
            completion_tokens=data.get("eval_count"),
        )

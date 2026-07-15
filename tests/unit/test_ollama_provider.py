"""Unit tests for OllamaProvider using an injected httpx MockTransport.

No real Ollama server is needed: we simulate its /api/chat responses and assert
both happy-path parsing and domain-exception mapping.
"""

from __future__ import annotations

import httpx
import pytest

from copilot.domain.exceptions import LLMError, LLMTimeoutError
from copilot.domain.value_objects.message import Message, Role
from copilot.infrastructure.llm.ollama_provider import OllamaProvider


def _provider_with(handler: httpx.MockTransport) -> OllamaProvider:
    client = httpx.Client(transport=handler, base_url="http://ollama:11434")
    return OllamaProvider(base_url="http://ollama:11434", default_model="qwen", client=client)


@pytest.mark.unit
def test_happy_path_parses_content_and_tokens() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/chat"
        return httpx.Response(
            200,
            json={
                "model": "qwen",
                "message": {"role": "assistant", "content": "SELECT 1;"},
                "prompt_eval_count": 11,
                "eval_count": 3,
            },
        )

    provider = _provider_with(httpx.MockTransport(handler))
    result = provider.complete([Message(Role.USER, "hi")])

    assert result.content == "SELECT 1;"
    assert result.model == "qwen"
    assert result.total_tokens == 14


@pytest.mark.unit
def test_http_500_maps_to_llm_error() -> None:
    provider = _provider_with(httpx.MockTransport(lambda req: httpx.Response(500, text="boom")))
    with pytest.raises(LLMError):
        provider.complete([Message(Role.USER, "hi")])


@pytest.mark.unit
def test_timeout_maps_to_llm_timeout_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("slow", request=request)

    provider = _provider_with(httpx.MockTransport(handler))
    with pytest.raises(LLMTimeoutError):
        provider.complete([Message(Role.USER, "hi")])


@pytest.mark.unit
def test_malformed_body_maps_to_llm_error() -> None:
    provider = _provider_with(
        httpx.MockTransport(lambda req: httpx.Response(200, json={"unexpected": True}))
    )
    with pytest.raises(LLMError):
        provider.complete([Message(Role.USER, "hi")])

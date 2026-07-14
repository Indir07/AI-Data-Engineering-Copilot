"""In-memory test doubles implementing domain ports.

``FakeLLM`` satisfies ``LLMPort`` structurally (no inheritance needed), which is
exactly why the port is a Protocol: fast, deterministic unit tests with zero
network and zero Ollama.
"""

from __future__ import annotations

from collections.abc import Sequence

from copilot.domain.value_objects.completion import CompletionResult
from copilot.domain.value_objects.message import Message


class FakeLLM:
    """A scripted ``LLMPort`` that records the messages it was called with."""

    def __init__(self, reply: str = "fake reply", model: str = "fake-model") -> None:
        self.reply = reply
        self.model = model
        self.calls: list[list[Message]] = []

    def complete(
        self,
        messages: Sequence[Message],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        self.calls.append(list(messages))
        return CompletionResult(
            content=self.reply,
            model=model or self.model,
            prompt_tokens=len(messages),
            completion_tokens=len(self.reply.split()),
        )

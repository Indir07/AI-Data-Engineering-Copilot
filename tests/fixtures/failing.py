"""LLM doubles that fail, for exercising error-handling paths."""

from __future__ import annotations

from collections.abc import Sequence

from copilot.domain.exceptions import LLMError, LLMTimeoutError
from copilot.domain.value_objects.completion import CompletionResult
from copilot.domain.value_objects.message import Message


class RaisingLLM:
    """Always raises ``LLMError`` (simulates a backend failure)."""

    def complete(self, messages: Sequence[Message], **_: object) -> CompletionResult:
        raise LLMError("backend exploded")


class TimingOutLLM:
    """Always raises ``LLMTimeoutError``."""

    def complete(self, messages: Sequence[Message], **_: object) -> CompletionResult:
        raise LLMTimeoutError("backend too slow")

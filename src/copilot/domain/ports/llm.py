"""LLM port — the domain's contract for any language-model backend.

Defined as a ``Protocol`` (structural typing) so adapters do **not** need to
import or subclass anything from the domain to satisfy it — they just implement
the method. This is the Dependency Inversion Principle: the application depends
on this abstraction, and infrastructure (Ollama, or any OpenAI-compatible
endpoint) provides the concrete implementation.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from copilot.domain.value_objects.completion import CompletionResult
from copilot.domain.value_objects.message import Message


@runtime_checkable
class LLMPort(Protocol):
    """Synchronous chat-completion contract."""

    def complete(
        self,
        messages: Sequence[Message],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """Return a completion for ``messages``.

        Implementations must raise :class:`copilot.domain.exceptions.LLMError`
        (or a subclass) on backend failure — never a transport-specific error.
        """
        ...

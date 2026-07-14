"""LLM completion result value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompletionResult:
    """The outcome of a single LLM call.

    Token counts are optional because not every provider reports them; the
    domain does not depend on their presence.
    """

    content: str
    model: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    @property
    def total_tokens(self) -> int | None:
        if self.prompt_tokens is None or self.completion_tokens is None:
            return None
        return self.prompt_tokens + self.completion_tokens

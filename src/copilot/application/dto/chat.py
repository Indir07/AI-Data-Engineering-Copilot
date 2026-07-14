"""Application-layer DTOs for the chat use case.

DTOs decouple the use case from the transport schema. The API layer owns Pydantic
request/response models; it maps them to/from these plain dataclasses so the
application never depends on FastAPI.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from copilot.domain.value_objects.message import Message


@dataclass(frozen=True, slots=True)
class ChatRequestDTO:
    """Input to :class:`copilot.application.use_cases.chat.ChatUseCase`."""

    prompt: str
    system: str | None = None
    history: list[Message] = field(default_factory=list)
    model: str | None = None
    temperature: float | None = None

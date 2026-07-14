"""Chat message value objects.

Value objects are immutable and compared by value. A ``Message`` is the atomic
unit of an LLM conversation; keeping it in the domain (not tied to any provider
SDK) means every layer speaks the same vocabulary and adapters translate at the
edge.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    """Who authored a message."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True, slots=True)
class Message:
    """An immutable chat message."""

    role: Role
    content: str

    def __post_init__(self) -> None:
        if not self.content or not self.content.strip():
            raise ValueError("Message.content must be non-empty")

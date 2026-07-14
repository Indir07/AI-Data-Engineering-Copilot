"""Conversation entity.

Unlike a value object, an entity has identity (``id``) and a lifecycle: the same
conversation accrues messages over time. Kept framework-free; persistence is an
infrastructure concern (Phase 4) reached through the ``ConversationRepository``
port.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from copilot.domain.value_objects.message import Message, Role


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Conversation:
    """An ordered exchange of messages with stable identity."""

    id: str = field(default_factory=lambda: str(uuid4()))
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=_utcnow)
    title: str | None = None

    def add(self, role: Role, content: str) -> Message:
        message = Message(role=role, content=content)
        self.messages.append(message)
        return message

    def with_system_prompt(self, prompt: str) -> "Conversation":
        """Return the conversation guaranteed to start with a system prompt."""
        if not self.messages or self.messages[0].role is not Role.SYSTEM:
            self.messages.insert(0, Message(role=Role.SYSTEM, content=prompt))
        return self

    def ensure_title(self, fallback: str) -> None:
        """Derive a short title from the first user message if unset."""
        if self.title:
            return
        for message in self.messages:
            if message.role is Role.USER:
                self.title = message.content[:60].strip() or fallback
                return
        self.title = fallback

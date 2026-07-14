"""Repository ports — the domain's contract for persistence.

Repositories express persistence in domain terms ("save this Conversation"),
hiding SQL, ORMs, and databases behind an interface. The application depends on
these Protocols; infrastructure provides SQLAlchemy adapters. Swapping SQLite for
Postgres — or an ORM repo for an in-memory fake in tests — never touches the core.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from copilot.domain.entities.conversation import Conversation


@runtime_checkable
class ConversationRepository(Protocol):
    """Persistence contract for :class:`Conversation` aggregates."""

    def get(self, conversation_id: str) -> Conversation | None:
        """Return the conversation, or ``None`` if it does not exist."""
        ...

    def save(self, conversation: Conversation) -> None:
        """Create or update the conversation (upsert by id)."""
        ...

    def list(self, limit: int = 50) -> list[Conversation]:
        """Return recent conversations, newest first."""
        ...

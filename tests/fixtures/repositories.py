"""In-memory ConversationRepository double for fast unit tests.

Copies on the way in and out so tests exercise the same "detached aggregate"
semantics the SQL adapter provides (mutating a returned object must not silently
change stored state).
"""

from __future__ import annotations

import copy

from copilot.domain.entities.conversation import Conversation


class InMemoryConversationRepository:
    def __init__(self) -> None:
        self._store: dict[str, Conversation] = {}

    def get(self, conversation_id: str) -> Conversation | None:
        stored = self._store.get(conversation_id)
        return copy.deepcopy(stored) if stored is not None else None

    def save(self, conversation: Conversation) -> None:
        self._store[conversation.id] = copy.deepcopy(conversation)

    def list(self, limit: int = 50) -> list[Conversation]:
        ordered = sorted(self._store.values(), key=lambda c: c.created_at, reverse=True)
        return [copy.deepcopy(c) for c in ordered[:limit]]

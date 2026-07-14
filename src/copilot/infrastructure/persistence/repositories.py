"""SQLAlchemy implementation of the ConversationRepository port.

Maps ORM rows ↔ domain entities. All ORM/session usage is confined here; callers
receive plain domain objects.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from copilot.domain.entities.conversation import Conversation
from copilot.domain.value_objects.message import Message, Role
from copilot.infrastructure.persistence.database import session_scope
from copilot.infrastructure.persistence.models import ConversationModel, MessageModel


class SqlAlchemyConversationRepository:
    """Persist conversations in a relational database via SQLAlchemy."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    # --- mapping helpers ---
    @staticmethod
    def _to_domain(model: ConversationModel) -> Conversation:
        return Conversation(
            id=model.id,
            created_at=model.created_at,
            title=model.title,
            messages=[Message(role=Role(m.role), content=m.content) for m in model.messages],
        )

    # --- port methods ---
    def get(self, conversation_id: str) -> Conversation | None:
        with session_scope(self._session_factory) as session:
            model = session.get(ConversationModel, conversation_id)
            return self._to_domain(model) if model is not None else None

    def save(self, conversation: Conversation) -> None:
        with session_scope(self._session_factory) as session:
            model = session.get(ConversationModel, conversation.id)
            if model is None:
                model = ConversationModel(
                    id=conversation.id,
                    title=conversation.title,
                    created_at=conversation.created_at,
                )
                session.add(model)
            else:
                model.title = conversation.title
                model.messages.clear()
                session.flush()

            for position, message in enumerate(conversation.messages):
                model.messages.append(
                    MessageModel(
                        position=position,
                        role=message.role.value,
                        content=message.content,
                    )
                )

    def list(self, limit: int = 50) -> list[Conversation]:
        with session_scope(self._session_factory) as session:
            stmt = (
                select(ConversationModel)
                .order_by(ConversationModel.created_at.desc())
                .limit(limit)
            )
            return [self._to_domain(m) for m in session.execute(stmt).scalars().all()]

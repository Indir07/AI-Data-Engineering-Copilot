"""SQLAlchemy ORM models.

These are an infrastructure detail: they never leave this layer. The repository
maps them to/from domain entities so the domain stays free of the ORM.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from copilot.infrastructure.persistence.database import Base


class ConversationModel(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    messages: Mapped[list[MessageModel]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="MessageModel.position",
        lazy="selectin",
    )


class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    conversation: Mapped[ConversationModel] = relationship(back_populates="messages")

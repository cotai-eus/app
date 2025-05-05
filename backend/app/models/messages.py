import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, Boolean, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMPTZ
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401

class Message(Base):
    """
    Modelo SQLAlchemy para Mensagens.
    """
    __tablename__ = "messages"

    message_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    # Remetente da mensagem
    sender_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    # Destinatário da mensagem
    receiver_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True), server_default=func.timezone('utc', func.now())
    )

    # Relacionamentos com remetente e destinatário
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

    # __table_args__ pode incluir índices compostos se necessário
    # Ex: Index('idx_messages_sender_receiver', 'sender_id', 'receiver_id') # Já criado pelos index=True acima
import uuid
from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Message(Base):
    """
    # Modelo para mensagens entre usuários
    # Model for messages between users
    """
    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    receiver_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Não precisamos de updated_at aqui, mensagens não são atualizadas
    # We don't need updated_at here, messages aren't updated
    updated_at: Mapped[datetime] = None
    
    # Relacionamentos
    # Relationships
    sender: Mapped["User"] = relationship(
        back_populates="sent_messages", foreign_keys=[sender_id]
    )
    receiver: Mapped["User"] = relationship(
        back_populates="received_messages", foreign_keys=[receiver_id]
    )


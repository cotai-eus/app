import uuid
from sqlalchemy import Column, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Message(Base):
    """
    Modelo para mensagens entre usuários.
    """
    __tablename__ = "messages"
    
    # Substituindo o ID padrão pelo específico messages.message_id
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        name="message_id"
    )
    
    # Chaves estrangeiras para remetente e destinatário
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )
    
    receiver_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Conteúdo da mensagem
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Status de leitura
    is_read: Mapped[bool] = mapped_column(Boolean, server_default=expression.false(), nullable=False)
    
    # Relacionamentos
    sender: Mapped["User"] = relationship(back_populates="sent_messages", foreign_keys=[sender_id])
    receiver: Mapped["User"] = relationship(back_populates="received_messages", foreign_keys=[receiver_id])
import uuid
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class CalendarEvent(Base):
    """
    Modelo para eventos de calendário.
    """
    __tablename__ = "calendar_events"
    
    # Substituindo o ID padrão pelo específico calendar_events.event_id
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        name="event_id"
    )
    
    # Chave estrangeira para usuário
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Informações do evento
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Horários
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Recorrência
    is_recurring: Mapped[bool] = mapped_column(Boolean, server_default=expression.false(), nullable=False)
    
    # Relacionamentos
    user: Mapped["User"] = relationship(back_populates="calendar_events")
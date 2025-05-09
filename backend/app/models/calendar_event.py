from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from app.db.base import Base

class CalendarEvent(Base):
    """Modelo para eventos de calendário."""
    
    __tablename__ = "calendar_event"
    
    event_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    startTime: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    endTime: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    type: Mapped[str] = mapped_column(
        String(20), nullable=False, 
        comment="Tipo: prazo, reuniao, licitacao, outro"
    )
    priority: Mapped[str] = mapped_column(
        String(10), nullable=False, default="media",
        comment="Prioridade: baixa, media, alta"
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Relacionamento
    user = relationship("User", back_populates="calendar_events")


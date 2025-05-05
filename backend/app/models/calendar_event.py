import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class CalendarEvent(Base):
    """
    # Modelo para eventos de calendário
    # Model for calendar events
    """
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_time: Mapped[datetime] = mapped_column(nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="other")  # deadline, meeting, visit, other
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relacionamentos
    # Relationships
    user: Mapped["User"] = relationship(back_populates="calendar_events")


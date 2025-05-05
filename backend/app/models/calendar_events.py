import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Text, Boolean, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMPTZ
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401

class CalendarEvent(Base):
    """
    Modelo SQLAlchemy para Eventos de Calendário.
    """
    __tablename__ = "calendar_events"

    event_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    start_time: Mapped[datetime] = mapped_column(TIMESTAMPTZ(timezone=True), nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMPTZ(timezone=True), nullable=False)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    # Para recorrência complexa, um campo JSONB ou tabela separada seria melhor
    # recurrence_rule: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True), server_default=func.timezone('utc', func.now())
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True),
        server_default=func.timezone('utc', func.now()),
        onupdate=func.timezone('utc', func.now()),
    )

    # Relacionamento com o usuário
    user: Mapped["User"] = relationship(back_populates="calendar_events")

    # __table_args__ pode incluir índices
    # Ex: Index('idx_calendar_events_user_id_start_time', 'user_id', 'start_time') # Já criado pelos index=True acima
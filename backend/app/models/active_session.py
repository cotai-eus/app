import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class ActiveSession(Base):
    """
    # Modelo para sessões ativas dos usuários
    # Model for active user sessions
    """
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    device_info: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)  # IPv6 support
    last_accessed_at: Mapped[datetime] = mapped_column(nullable=False)
    
    # Não precisamos de updated_at aqui, usamos last_accessed_at
    # We don't need updated_at here, we use last_accessed_at
    updated_at: Mapped[datetime] = None
    
    # Relacionamentos
    # Relationships
    user: Mapped["User"] = relationship(back_populates="active_sessions")

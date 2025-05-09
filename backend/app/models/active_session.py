from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from app.db.base import Base

class ActiveSession(Base):
    """Modelo para sessões ativas de usuário."""
    
    __tablename__ = "active_session"
    
    session_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    device_info: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)  # IPv6 compatible
    last_accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    is_revoked: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="active_sessions")

    # Create index on user_id
    __table_args__ = (
        Index('ix_active_session_user_id', user_id),
    )

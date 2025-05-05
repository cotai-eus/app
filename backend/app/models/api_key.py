import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class ApiKey(Base):
    """
    # Modelo para chaves de API
    # Model for API keys
    """
    key_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    prefix: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    hashed_key: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Relacionamentos
    # Relationships
    user: Mapped["User"] = relationship(back_populates="api_keys")

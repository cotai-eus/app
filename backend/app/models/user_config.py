from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from app.db.base import Base

class UserConfig(Base):
    """Modelo para configurações do usuário."""
    
    __tablename__ = "user_config"
    
    config_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    theme: Mapped[str] = mapped_column(default="system")
    ui_density: Mapped[str] = mapped_column(default="normal")
    notifications: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Relacionamento
    user = relationship("User", back_populates="config")

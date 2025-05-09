from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, CITEXT

from app.db.base import Base

class User(Base):
    """Modelo de usuário."""
    
    __tablename__ = "user"
    
    user_id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    config = relationship("UserConfig", back_populates="user", uselist=False, cascade="all, delete-orphan")
    uploaded_documents = relationship("Document", back_populates="uploaded_by")
    calendar_events = relationship("CalendarEvent", back_populates="user", cascade="all, delete-orphan")
    bids = relationship("Bid", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")
    active_sessions = relationship("ActiveSession", back_populates="user", cascade="all, delete-orphan")


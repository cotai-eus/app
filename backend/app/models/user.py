import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, Text, TIMESTAMP, func, Index
from sqlalchemy.dialects.postgresql import UUID, CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .contact import Contact  # noqa F401
    from .message import Message  # noqa F401
    from .calendar_event import CalendarEvent  # noqa F401
    from .form_response import FormResponse  # noqa F401
    from .user_photo import UserPhoto  # noqa F401
    from .bid import Bid  # noqa F401
    from .api_key import ApiKey  # noqa F401
    from .active_session import ActiveSession  # noqa F401
    from .document import Document  # noqa F401

class User(Base):
    """
    Modelo SQLAlchemy para a tabela 'users'.
    """
    __tablename__ = "users"

    # Colunas da tabela
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    username: Mapped[str] = mapped_column(CITEXT, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(CITEXT, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default='true')
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false')
    last_login: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())  # onupdate é um fallback

    # Relacionamentos (definidos com back_populates para bidirecionalidade)
    bids: Mapped[List["Bid"]] = relationship("Bid", back_populates="user", cascade="all, delete-orphan")
    contacts: Mapped[List["Contact"]] = relationship("Contact", back_populates="user", cascade="all, delete-orphan")
    sent_messages: Mapped[List["Message"]] = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender", cascade="all, delete-orphan")
    received_messages: Mapped[List["Message"]] = relationship("Message", foreign_keys="[Message.receiver_id]", back_populates="receiver", cascade="all, delete-orphan")
    calendar_events: Mapped[List["CalendarEvent"]] = relationship("CalendarEvent", back_populates="user", cascade="all, delete-orphan")
    form_responses: Mapped[List["FormResponse"]] = relationship("FormResponse", back_populates="user", cascade="all, delete-orphan")
    photos: Mapped[List["UserPhoto"]] = relationship("UserPhoto", back_populates="user", cascade="all, delete-orphan")
    api_keys: Mapped[List["ApiKey"]] = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")
    active_sessions: Mapped[List["ActiveSession"]] = relationship("ActiveSession", back_populates="user", cascade="all, delete-orphan")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="user", cascade="all, delete-orphan")

    # Índices explícitos (embora unique=True e index=True já criem índices)
    __table_args__ = (
        Index('idx_users_email', 'email'),  # Exemplo redundante, mas demonstra como adicionar
    )

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}')>"


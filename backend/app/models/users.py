import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, CITEXT
from sqlalchemy.sql import expression
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class User(Base):
    """
    Modelo de usuário no sistema.
    """
    __tablename__ = "users"
    
    # Substituindo o ID padrão pelo específico users.user_id
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        name="user_id"
    )
    
    # Campos de autenticação
    username: Mapped[str] = mapped_column(CITEXT, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(CITEXT, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Informações de perfil
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Estado da conta
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=expression.true(), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default=expression.false(), nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    contacts: Mapped[List["Contact"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sent_messages: Mapped[List["Message"]] = relationship(
        "Message", 
        foreign_keys="[Message.sender_id]", 
        back_populates="sender", 
        cascade="all, delete-orphan"
    )
    received_messages: Mapped[List["Message"]] = relationship(
        "Message", 
        foreign_keys="[Message.receiver_id]", 
        back_populates="receiver", 
        cascade="all, delete-orphan"
    )
    calendar_events: Mapped[List["CalendarEvent"]] = relationship(back_populates="user", cascade="all, delete-orphan")


    photos: Mapped[List["UserPhoto"]] = relationship(back_populates="user", cascade="all, delete-orphan")    form_responses: Mapped[List["FormResponse"]] = relationship(back_populates="user", cascade="all, delete-orphan")
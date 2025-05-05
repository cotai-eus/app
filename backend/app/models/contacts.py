import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint, func, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, CITEXT, TIMESTAMPTZ
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401

class Contact(Base):
    """
    Modelo SQLAlchemy para Contatos.
    """
    __tablename__ = "contacts"

    # Chave primária UUID gerada automaticamente pelo PostgreSQL
    contact_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    # Chave estrangeira para o usuário dono do contato
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    first_name: Mapped[Optional[str]] = mapped_column(Text)
    last_name: Mapped[Optional[str]] = mapped_column(Text)
    # Email case-insensitive
    email: Mapped[Optional[str]] = mapped_column(CITEXT)
    phone: Mapped[Optional[str]] = mapped_column(String)
    company: Mapped[Optional[str]] = mapped_column(Text)
    # Timestamp de criação com fuso horário UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True), server_default=func.timezone('utc', func.now())
    )
    # Timestamp da última atualização com fuso horário UTC
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True),
        server_default=func.timezone('utc', func.now()),
        onupdate=func.timezone('utc', func.now()), # Atualiza automaticamente no update
    )

    # Relacionamento com o usuário
    user: Mapped["User"] = relationship(back_populates="contacts")

    # Constraint para garantir que um usuário não tenha contatos duplicados pelo email
    __table_args__ = (
        UniqueConstraint('user_id', 'email', name='uq_user_contact_email'),
        # Adicionar outros índices se necessário
        # Index('idx_contacts_user_id', 'user_id'), # Já criado pelo index=True acima
    )
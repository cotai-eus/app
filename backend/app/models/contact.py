import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, TIMESTAMP, func, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa F401

class Contact(Base):
    """
    # Modelo para contatos dos usuários
    # Model for user contacts
    """
    __tablename__ = "contacts"

    contact_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(CITEXT, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="contacts")

    # Constraints e Índices
    __table_args__ = (
        UniqueConstraint('user_id', 'email', name='uq_contacts_user_id_email'),
    )

    def __repr__(self) -> str:
        return f"<Contact(contact_id={self.contact_id}, user_id={self.user_id}, email='{self.email}')>"


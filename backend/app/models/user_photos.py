import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMPTZ
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401

class UserPhoto(Base):
    """
    Modelo SQLAlchemy para Fotos de Usuários.
    (Exemplo, pode não ser necessário se avatar_url for suficiente)
    """
    __tablename__ = "user_photos"

    photo_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    # URL da foto, assumindo armazenamento externo (S3, etc.)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    uploaded_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True), server_default=func.timezone('utc', func.now())
    )

    # Relacionamento com o usuário
    user: Mapped["User"] = relationship(back_populates="photos")
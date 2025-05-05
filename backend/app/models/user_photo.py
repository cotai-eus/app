import uuid
from sqlalchemy import Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base_class import Base
import datetime

if TYPE_CHECKING:
    from .user import User # noqa F401

class UserPhoto(Base):
    """
    Modelo SQLAlchemy para a tabela 'user_photos'.
    Armazena referências a fotos de usuários (e.g., avatares, uploads).
    """
    __tablename__ = "user_photos"

    photo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    # URL da foto, geralmente apontando para um serviço de armazenamento (S3, etc.)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    uploaded_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relacionamento com User
    user: Mapped["User"] = relationship("User", back_populates="photos")

    def __repr__(self) -> str:
        return f"<UserPhoto(photo_id={self.photo_id}, user_id={self.user_id}, url='{self.url[:30]}...')>"


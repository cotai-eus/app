import uuid
from sqlalchemy import Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Dict, Any, TYPE_CHECKING
from app.db.base_class import Base
import datetime

if TYPE_CHECKING:
    from .form_response import FormResponse # noqa F401

class Form(Base):
    """
    Modelo SQLAlchemy para a tabela 'forms'.
    Representa a estrutura/template de um formulário.
    """
    __tablename__ = "forms"

    form_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    # user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id")) # Descomente se formulários forem por usuário
    title: Mapped[str] = mapped_column(Text, nullable=False)
    # Armazena a definição da estrutura do formulário (campos, tipos, labels, etc.)
    structure: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()) # Gerenciado por trigger

    # Relacionamento com FormResponse
    responses: Mapped[List["FormResponse"]] = relationship("FormResponse", back_populates="form", cascade="all, delete-orphan")

    # user: Mapped["User" | None] = relationship("User") # Descomente se user_id for usado

    def __repr__(self) -> str:
        return f"<Form(form_id={self.form_id}, title='{self.title}')>"


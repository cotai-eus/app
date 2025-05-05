import uuid
from datetime import datetime
from typing import List, Dict, Any, TYPE_CHECKING, Optional

from sqlalchemy import Text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMPTZ, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .form_responses import FormResponse  # noqa: F401
    # from .users import User # Descomentar se forms forem ligados a usuários

class Form(Base):
    """
    Modelo SQLAlchemy para Formulários (Templates).
    """
    __tablename__ = "forms"

    form_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    # user_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True) # Se formulários forem específicos de usuário
    title: Mapped[str] = mapped_column(Text, nullable=False)
    # Estrutura do formulário (campos, tipos, labels) armazenada como JSON
    structure: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True), server_default=func.timezone('utc', func.now())
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True),
        server_default=func.timezone('utc', func.now()),
        onupdate=func.timezone('utc', func.now()),
    )

    # Relacionamento com as respostas do formulário
    responses: Mapped[List["FormResponse"]] = relationship(back_populates="form")
    # user: Mapped[Optional["User"]] = relationship() # Se formulários forem específicos de usuário

class FormResponse(Base):
    """
    Modelo para respostas a formulários.
    """
    __tablename__ = "form_responses"
    
    # Substituindo o ID padrão pelo específico form_responses.response_id
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        name="response_id"
    )
    
    # Chaves estrangeiras
    form_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        ForeignKey("forms.form_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    source_pdf_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True
    )
    
    # Respostas do formulário
    answers: Mapped[dict] = mapped_column(JSONB, nullable=False)
    
    # Status da resposta
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    
    # Timestamp de processamento
    processed_at: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True
    )
    
    # Relacionamentos
    form: Mapped["Form"] = relationship(back_populates="responses")
    user: Mapped["User"] = relationship(back_populates="form_responses")
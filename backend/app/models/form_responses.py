import uuid
from datetime import datetime
from typing import Dict, Any, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMPTZ, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401
    from .forms import Form  # noqa: F401
    # from .documents import Document # Se houver uma tabela de documentos

class FormResponse(Base):
    """
    Modelo SQLAlchemy para Respostas de Formulários.
    """
    __tablename__ = "form_responses"

    response_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    form_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("forms.form_id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True) # Usuário que submeteu/processou
    # ID opcional do PDF fonte, assumindo que existe uma tabela 'documents' ou similar
    source_pdf_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("documents.document_id"), nullable=True) # Ajustar nome da tabela/coluna se necessário
    # Respostas do formulário armazenadas como JSON
    answers: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    # Status do processamento da resposta
    status: Mapped[str] = mapped_column(Text, default='pending', index=True) # Ex: pending, processing, review_required, completed
    submitted_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True), server_default=func.timezone('utc', func.now())
    )
    processed_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMPTZ(timezone=True))

    # Relacionamentos
    form: Mapped["Form"] = relationship(back_populates="responses")
    user: Mapped["User"] = relationship(back_populates="form_responses")
    # source_pdf: Mapped[Optional["Document"]] = relationship() # Se houver tabela de documentos
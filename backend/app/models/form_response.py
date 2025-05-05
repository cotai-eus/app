import uuid
from sqlalchemy import Text, TIMESTAMP, func, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Dict, Any, TYPE_CHECKING
from app.db.base_class import Base
import datetime

if TYPE_CHECKING:
    from .user import User # noqa F401
    from .form import Form # noqa F401

class FormResponse(Base):
    """
    Modelo SQLAlchemy para a tabela 'form_responses'.
    Armazena as respostas submetidas para um formulário específico.
    """
    __tablename__ = "form_responses"

    response_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    form_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("forms.form_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    # Opcional: ID do documento PDF original usado para preenchimento via IA
    source_pdf_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True)) # Poderia referenciar uma tabela 'documents'
    # Armazena as respostas como um JSON {"field_name": "value", ...}
    answers: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    # Status do processamento da resposta (especialmente se via IA)
    status: Mapped[str] = mapped_column(Text, default='pending', server_default='pending') # e.g., 'pending', 'processing', 'review_required', 'completed'
    submitted_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    processed_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    # Relacionamentos
    form: Mapped["Form"] = relationship("Form", back_populates="responses")
    user: Mapped["User"] = relationship("User", back_populates="form_responses")

    # Índices (já criados por index=True nas colunas FK)
    # __table_args__ = (
    #     Index('idx_form_responses_form_id', 'form_id'),
    #     Index('idx_form_responses_user_id', 'user_id'),
    # )

    def __repr__(self) -> str:
        return f"<FormResponse(response_id={self.response_id}, form_id={self.form_id}, user_id={self.user_id}, status='{self.status}')>"


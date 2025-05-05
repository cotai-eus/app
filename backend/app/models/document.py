import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Document(Base):
    """
    # Modelo para documentos/arquivos enviados
    # Model for uploaded documents/files
    """
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    processing_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="pending"  # pending, processing, completed, error
    )
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    llm_analysis: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    processed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Relacionamentos
    # Relationships
    user: Mapped["User"] = relationship(back_populates="documents")
    bids: Mapped[list["Bid"]] = relationship(back_populates="source_document")

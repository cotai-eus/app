import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Bid(Base):
    """
    # Modelo para licitações/editais
    # Model for bids/tenders
    """
    bid_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    internal_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    organization: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ua: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    publication_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    deadline_date: Mapped[datetime] = mapped_column(nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, default="novos"
    )  # novos, em_analise, pronto_para_assinar, enviado, ganhos, perdidos
    source_document_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("document.document_id", ondelete="SET NULL"), nullable=True
    )
    analysis_result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Relacionamentos
    # Relationships
    user: Mapped["User"] = relationship(back_populates="bids")
    source_document: Mapped[Optional["Document"]] = relationship(back_populates="bids")

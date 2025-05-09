from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from app.db.base import Base

class Bid(Base):
    """Modelo para licitações."""
    
    __tablename__ = "bid"
    
    bid_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    publication_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deadline_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="recebidos", index=True,
        comment="Status: recebidos, analisados, enviados, respondidos, ganho, perdido"
    )
    status_changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False
    )
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("document.document_id", ondelete="SET NULL"),
        nullable=True
    )
    analysis_result: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON, nullable=True,
        comment="Resultado da análise realizada por IA"
    )
    
    # Relacionamentos
    user = relationship("User", back_populates="bids")
    source_document = relationship("Document", back_populates="bids")
    documents = relationship("Document", back_populates="related_bid", foreign_keys="Document.related_bid_id")

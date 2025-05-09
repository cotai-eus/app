from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Text, Integer, Column, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, TEXT, JSON

from app.db.base import Base

class Document(Base):
    """Modelo para documentos/editais."""
    
    __tablename__ = "document"
    
    document_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    platform: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    document_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    document_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    processing_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending",
        comment="Status: pending, processing, completed, error"
    )
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    extracted_text: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    llm_analysis: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    uploaded_by_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False
    )
    related_bid_id: Mapped[Optional[UUID]] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("bid.bid_id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Relacionamentos
    uploaded_by = relationship("User", back_populates="uploaded_documents")
    related_bid = relationship("Bid", back_populates="documents", foreign_keys=[related_bid_id])
    bids = relationship("Bid", back_populates="source_document", foreign_keys="Bid.source_document_id")

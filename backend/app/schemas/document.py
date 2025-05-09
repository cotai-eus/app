from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

# Base schema
class DocumentBase(BaseModel):
    """Esquema base para documentos/editais."""
    title: str
    description: Optional[str] = None
    platform: str
    document_type: str
    document_number: str
    entity: str

# Create schema
class DocumentCreate(DocumentBase):
    """Esquema para criação de um documento/edital."""
    pass

# Update schema
class DocumentUpdate(BaseModel):
    """Esquema para atualização de um documento/edital."""
    title: Optional[str] = None
    description: Optional[str] = None
    platform: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    entity: Optional[str] = None

# Public schema (response)
class DocumentPublic(DocumentBase):
    """Esquema público para documentos/editais."""
    document_id: UUID
    file_name: str
    file_size: int
    mime_type: str
    processing_status: str
    processed_at: Optional[datetime] = None
    uploaded_by_id: UUID
    related_bid_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

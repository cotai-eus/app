from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

# Base schema
class DocumentBase(BaseModel):
    """Esquema base para documentos."""
    title: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

# Create schema
class DocumentCreate(DocumentBase):
    """Esquema para criação de documentos."""
    pass

# Update schema
class DocumentUpdate(BaseModel):
    """Esquema para atualização de documentos."""
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

# Database schema
class DocumentInDB(DocumentBase):
    """Esquema para documentos armazenados no banco de dados."""
    document_id: UUID
    user_id: UUID
    bid_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Document with analysis schema
class DocumentWithAnalysis(DocumentBase):
    """Esquema para documentos com resultados de análise."""
    document_id: UUID
    user_id: UUID
    analysis_results: Optional[Dict[str, Any]] = None
    analysis_status: Optional[str] = None
    analysis_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Public schema (response)
class DocumentPublic(DocumentBase):
    """Esquema público para documentos."""
    document_id: UUID
    user_id: UUID
    bid_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

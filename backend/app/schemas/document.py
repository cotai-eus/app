from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    """
    # Campos base para documento
    # Base fields for document
    """
    file_name: str
    content_type: str


class DocumentCreate(DocumentBase):
    """
    # Campos para criação de documento
    # Fields for document creation
    """
    file_path: str
    size_bytes: int
    processing_status: str = "pending"


class DocumentUpdate(BaseModel):
    """
    # Campos para atualização de documento
    # Fields for document update
    """
    processing_status: Optional[str] = None
    extracted_text: Optional[str] = None
    llm_analysis: Optional[Dict] = None
    processed_at: Optional[datetime] = None


class DocumentInDB(DocumentBase):
    """
    # Modelo de documento no banco de dados
    # Document model in the database
    """
    document_id: UUID
    user_id: UUID
    file_path: str
    size_bytes: int
    processing_status: str
    extracted_text: Optional[str] = None
    llm_analysis: Optional[Dict] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DocumentPublic(DocumentBase):
    """
    # Modelo de documento para resposta pública
    # Document model for public response
    """
    document_id: UUID
    size_bytes: int
    processing_status: str
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DocumentWithAnalysis(DocumentPublic):
    """
    # Modelo de documento com resultados da análise
    # Document model with analysis results
    """
    llm_analysis: Optional[Dict] = None

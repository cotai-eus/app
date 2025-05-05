from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BidBase(BaseModel):
    """
    # Campos base para licitação
    # Base fields for bid
    """
    title: Optional[str] = None
    organization: Optional[str] = None
    number: Optional[str] = None
    description: Optional[str] = None
    ua: Optional[str] = None
    publication_date: Optional[datetime] = None
    deadline_date: Optional[datetime] = None
    status: Optional[str] = None


class BidCreate(BidBase):
    """
    # Campos para criação de licitação
    # Fields for bid creation
    """
    title: str
    organization: str
    number: str
    deadline_date: datetime
    status: str = "novos"  # Default status
    internal_code: Optional[str] = None  # Generated if not provided
    source_document_id: Optional[UUID] = None


class BidUpdate(BidBase):
    """
    # Campos para atualização de licitação
    # Fields for bid update
    """
    pass


class BidInDB(BidBase):
    """
    # Modelo de licitação no banco de dados
    # Bid model in the database
    """
    bid_id: UUID
    user_id: UUID
    internal_code: str
    source_document_id: Optional[UUID] = None
    analysis_result: Optional[Dict] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BidPublic(BidBase):
    """
    # Modelo de licitação para resposta pública
    # Bid model for public response
    """
    bid_id: UUID
    internal_code: str
    source_document_id: Optional[UUID] = None
    analysis_result: Optional[Dict] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BidStatusUpdate(BaseModel):
    """
    # Atualização de status da licitação
    # Bid status update
    """
    status: str = Field(..., description="Novo status da licitação")


class BidSignRequest(BaseModel):
    """
    # Solicitação para assinar uma licitação
    # Request to sign a bid
    """
    password: str = Field(..., description="Senha do usuário para confirmar a ação")

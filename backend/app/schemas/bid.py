from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

# Base schema
class BidBase(BaseModel):
#    """Esquema base para licitações."""
    id: int
    title: str
    description: Optional[str] = None
    number: Optional[str] = None
    organization: Optional[str] = None
    publication_date: Optional[datetime] = None
    deadline_date: Optional[datetime] = None
    status: Optional[str] = Field("recebidos", description="recebidos, analisados, enviados, respondidos, ganho, perdido")

# Create schema
class BidCreate(BidBase):
    """Esquema para criação de uma licitação."""
    pass

# Update schema
class BidUpdate(BaseModel):
    """Esquema para atualização de uma licitação."""
    title: Optional[str] = None
    description: Optional[str] = None
    number: Optional[str] = None
    organization: Optional[str] = None
    publication_date: Optional[datetime] = None
    deadline_date: Optional[datetime] = None
    status: Optional[str] = None

# Status update schema (para Kanban)
class BidStatusUpdate(BaseModel):
    """Esquema para atualização de status de uma licitação."""
    status: str = Field(..., description="recebidos, analisados, enviados, respondidos, ganho, perdido")

# Database schema
class BidInDB(BidBase):
    """Esquema para licitações armazenadas no banco de dados."""
    bid_id: UUID
    user_id: UUID
    source_document_id: Optional[UUID] = None
    status_changed_at: datetime
    analysis_result: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Public schema (response)
class BidPublic(BidBase):
    """Esquema público para licitações."""
    bid_id: UUID
    user_id: UUID
    source_document_id: Optional[UUID] = None
    status_changed_at: datetime
    analysis_result: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Bid Sign Request schema
class BidSignRequest(BaseModel):
    """Esquema para solicitação de assinatura de licitação."""
    bid_id: UUID
    document_id: UUID
    signature_type: str = Field(..., description="digital, eletronica")
    requester_id: UUID
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

# Dashboard stats schema
class BidDashboardStats(BaseModel):
    """Estatísticas para o dashboard."""
    active_bids: int
    published_notices: int
    upcoming_deadlines: int
    success_rate: int

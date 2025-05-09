from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class ActiveSessionBase(BaseModel):
    """Esquema base para sessões ativas."""
    device_info: str
    ip_address: str

class ActiveSessionCreate(ActiveSessionBase):
    """Esquema para criação de uma sessão ativa."""
    user_id: UUID

class ActiveSessionPublic(ActiveSessionBase):
    """Esquema público para sessões ativas."""
    session_id: UUID
    user_id: UUID
    last_accessed_at: datetime
    is_revoked: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

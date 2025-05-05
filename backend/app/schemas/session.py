from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ActiveSessionBase(BaseModel):
    """
    # Campos base para sessão ativa
    # Base fields for active session
    """
    device_info: str
    location: Optional[str] = None
    ip_address: str


class ActiveSessionCreate(ActiveSessionBase):
    """
    # Campos para criação de sessão ativa
    # Fields for active session creation
    """
    pass


class ActiveSessionInDB(ActiveSessionBase):
    """
    # Modelo de sessão ativa no banco de dados
    # Active session model in the database
    """
    session_id: UUID
    user_id: UUID
    last_accessed_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ActiveSessionPublic(ActiveSessionBase):
    """
    # Modelo de sessão ativa para resposta pública
    # Active session model for public response
    """
    session_id: UUID
    last_accessed_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

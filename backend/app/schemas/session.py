from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

# Base schema
class ActiveSessionBase(BaseModel):
    """Esquema base para sessões ativas."""
    session_token: str
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    is_active: bool = True

# Create schema
class ActiveSessionCreate(ActiveSessionBase):
    """Esquema para criação de sessões ativas."""
    user_id: UUID

# Update schema
class ActiveSessionUpdate(BaseModel):
    """Esquema para atualização de sessões ativas."""
    is_active: Optional[bool] = None
    last_activity: Optional[datetime] = None

# Database schema
class ActiveSessionInDB(ActiveSessionBase):
    """Esquema para sessões ativas armazenadas no banco de dados."""
    session_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    last_activity: datetime
    
    class Config:
        from_attributes = True

# Public schema (response)
class ActiveSessionPublic(ActiveSessionBase):
    """Esquema público para sessões ativas."""
    session_id: UUID
    user_id: UUID
    created_at: datetime
    last_activity: datetime
    
    class Config:
        from_attributes = True

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ApiKeyBase(BaseModel):
    """
    # Campos base para chave de API
    # Base fields for API key
    """
    name: str = Field(..., min_length=1, max_length=100)


class ApiKeyCreate(ApiKeyBase):
    """
    # Campos para criação de chave de API
    # Fields for API key creation
    """
    pass


class ApiKeyCreateResponse(ApiKeyBase):
    """
    # Resposta de criação de chave de API
    # API key creation response
    """
    key_id: UUID
    prefix: str
    key: str  # Plain key (only returned once at creation)


class ApiKeyInDB(ApiKeyBase):
    """
    # Modelo de chave de API no banco de dados
    # API key model in the database
    """
    key_id: UUID
    user_id: UUID
    prefix: str
    hashed_key: str
    last_used_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ApiKeyPublic(ApiKeyBase):
    """
    # Modelo de chave de API para resposta pública
    # API key model for public response
    """
    key_id: UUID
    prefix: str
    last_used_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

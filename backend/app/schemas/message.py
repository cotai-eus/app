from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    message_id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
    created_at: datetime
    is_read: bool = False


class MessageBase(BaseModel):
    """
    # Campos base para mensagem
    # Base fields for message
    """
    content: str = Field(..., min_length=1)


class MessageCreate(BaseModel):
    receiver_id: UUID
    content: str


class MessageUpdate(BaseModel):
    """
    # Campos para atualização de mensagem
    # Fields for message update
    """
    is_read: bool = Field(default=True)


class MessageInDB(MessageBase):
    """
    # Modelo de mensagem no banco de dados
    # Message model in the database
    """
    message_id: UUID
    sender_id: UUID
    receiver_id: UUID
    is_read: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MessagePublic(MessageBase):
    """
    # Modelo de mensagem para resposta pública
    # Message model for public response
    """
    message_id: UUID
    sender_id: UUID
    receiver_id: UUID
    is_read: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


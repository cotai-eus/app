import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.base import BaseSchema, IdMixin, TimestampMixin

class MessageBase(BaseSchema):
    """
    Schema base para dados de mensagem.
    """
    content: str
    is_read: bool = False


class MessageCreate(MessageBase):
    """
    Schema para criação de mensagem.
    """
    receiver_id: uuid.UUID


class MessageUpdate(BaseSchema):
    """
    Schema para atualização de mensagem.
    """
    is_read: Optional[bool] = None


class MessageInDBBase(MessageBase, IdMixin):
    """
    Schema para mensagem em banco de dados.
    """
    sender_id: uuid.UUID
    receiver_id: uuid.UUID
    created_at: datetime


class Message(MessageInDBBase):
    """
    Schema para retorno de mensagem nas APIs.
    """
    pass


class MessageInDB(MessageInDBBase):
    """
    Schema para uso interno.
    """
    pass
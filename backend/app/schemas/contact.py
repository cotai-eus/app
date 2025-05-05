from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class ContactBase(BaseModel):
    """
    # Base schema for Contact
    """
    contact_id: UUID
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None


class Contact(ContactBase):
    """
    # Contact schema
    """
    pass


class ContactCreate(ContactBase):
    """
    # Campos para criação de contato
    # Fields for contact creation
    """
    pass


class ContactUpdate(ContactBase):
    """
    # Campos para atualização de contato
    # Fields for contact update
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ContactInDB(Contact):
    """
    # Modelo de contato no banco de dados
    # Contact model in the database
    """
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ContactPublic(Contact):
    """
    # Modelo de contato para resposta pública
    # Contact model for public response
    """
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ContactWithRecentMessage(ContactPublic):
    """
    # Modelo de contato com a mensagem mais recente
    # Contact model with the most recent message
    """
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
    unread_count: int = 0


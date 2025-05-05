import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Schema base com campos comuns
class ContactBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None # Validação de email
    phone: Optional[str] = None
    company: Optional[str] = None

# Schema para criação de contato (recebido na API)
class ContactCreate(ContactBase):
    email: EmailStr # Email é obrigatório na criação neste exemplo

# Schema para atualização de contato (recebido na API, todos os campos opcionais)
class ContactUpdate(ContactBase):
    pass

# Schema para leitura de contato (retornado pela API)
class ContactRead(ContactBase):
    contact_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True # Pydantic v1 compatibility, use from_attributes = True for v2
        # from_attributes = True # Para Pydantic v2+
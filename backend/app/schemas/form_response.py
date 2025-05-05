from pydantic import BaseModel, Field, ConfigDict
import uuid
import datetime
from typing import Optional, Dict, Any

# --- Schema Base ---
class FormResponseBase(BaseModel):
    """ Campos base para uma resposta de formulário. """
    # As respostas são um JSON mapeando nome do campo para valor. Ex: {"nome": "João Silva", "email": "joao@example.com"}
    answers: Dict[str, Any] = Field(..., description="Respostas do formulário no formato JSON")

# --- Schema para Criação (pode ser usado pela API ou internamente pelo processo AI) ---
class FormResponseCreate(FormResponseBase):
    """ Schema para criar uma nova resposta de formulário. """
    form_id: uuid.UUID = Field(..., description="ID do formulário ao qual esta resposta pertence")
    user_id: uuid.UUID = Field(..., description="ID do usuário que submeteu ou processou a resposta")
    source_pdf_id: Optional[uuid.UUID] = Field(None, description="ID opcional do PDF fonte (se aplicável)")
    status: str = Field('pending', description="Status inicial da resposta")

# --- Schema para Atualização (usado internamente, ex: para atualizar status) ---
class FormResponseUpdate(BaseModel):
    """ Schema para atualizar uma resposta de formulário. """
    model_config = ConfigDict(extra='ignore')

    answers: Optional[Dict[str, Any]] = None
    status: Optional[str] = None # e.g., 'processing', 'review_required', 'completed'
    processed_at: Optional[datetime.datetime] = None

# --- Schema para Leitura (Resposta da API) ---
class FormResponse(FormResponseBase):
    """ Schema completo para retornar dados de uma resposta de formulário. """
    response_id: uuid.UUID
    form_id: uuid.UUID
    user_id: uuid.UUID
    source_pdf_id: Optional[uuid.UUID] = None
    status: str
    submitted_at: datetime.datetime
    processed_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True) # Modo ORM

# --- Schema para verificar status ---
class FormResponseStatus(BaseModel):
    """ Schema simples para retornar o status de uma resposta. """
    response_id: uuid.UUID
    status: str
    processed_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)


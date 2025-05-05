from pydantic import BaseModel, Field, ConfigDict
import uuid
import datetime
from typing import Optional, Dict, Any

# --- Schema Base ---
class FormBase(BaseModel):
    """ Campos base para um formulário (template). """
    title: str = Field(..., description="Título do formulário")
    # A estrutura define os campos do formulário. Ex: {"fields": [{"name": "nome", "type": "text", "label": "Nome Completo"}]}
    structure: Dict[str, Any] = Field(..., description="Estrutura JSON definindo os campos do formulário")

# --- Schema para Criação ---
class FormCreate(FormBase):
    """ Schema para criar um novo template de formulário. """
    pass

# --- Schema para Atualização ---
class FormUpdate(BaseModel):
    """ Schema para atualizar um template de formulário. """
    model_config = ConfigDict(extra='ignore')

    title: Optional[str] = None
    structure: Optional[Dict[str, Any]] = None

# --- Schema para Leitura (Resposta da API) ---
class Form(FormBase):
    """ Schema completo para retornar dados de um template de formulário. """
    form_id: uuid.UUID
    # user_id: Optional[uuid.UUID] # Se for por usuário
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True) # Modo ORM


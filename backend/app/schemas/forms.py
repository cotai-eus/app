import uuid
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.base import BaseSchema, IdMixin, TimestampMixin

class FormBase(BaseSchema):
    """
    Schema base para dados de formulário.
    """
    title: str
    structure: Dict[str, Any]


class FormCreate(FormBase):
    """
    Schema para criação de formulário.
    """
    pass


class FormUpdate(BaseSchema):
    """
    Schema para atualização de formulário.
    """
    title: Optional[str] = None
    structure: Optional[Dict[str, Any]] = None


class FormInDBBase(FormBase, IdMixin, TimestampMixin):
    """
    Schema para formulário em banco de dados.
    """
    pass


class Form(FormInDBBase):
    """
    Schema para retorno de formulário nas APIs.
    """
    pass


class FormInDB(FormInDBBase):
    """
    Schema para uso interno.
    """
    pass


class FormResponseBase(BaseSchema):
    """
    Schema base para dados de resposta de formulário.
    """
    answers: Dict[str, Any]
    status: str = "pending"


class FormResponseCreate(FormResponseBase):
    """
    Schema para criação de resposta de formulário.
    """
    form_id: uuid.UUID
    source_pdf_id: Optional[uuid.UUID] = None


class FormResponseUpdate(BaseSchema):
    """
    Schema para atualização de resposta de formulário.
    """
    answers: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class FormResponseInDBBase(FormResponseBase, IdMixin):
    """
    Schema para resposta de formulário em banco de dados.
    """
    form_id: uuid.UUID
    user_id: uuid.UUID
    source_pdf_id: Optional[uuid.UUID] = None
    submitted_at: datetime
    processed_at: Optional[datetime] = None


class FormResponse(FormResponseInDBBase):
    """
    Schema para retorno de resposta de formulário nas APIs.
    """
    pass


class FormResponseInDB(FormResponseInDBBase):
    """
    Schema para uso interno.
    """
    pass


class DocumentProcessRequest(BaseSchema):
    """
    Schema para solicitação de processamento de documento.
    """
    form_id: uuid.UUID
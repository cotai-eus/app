from pydantic import BaseModel, Field, ConfigDict, field_validator
import uuid
import datetime
from typing import Optional

# --- Schema Base ---
class CalendarEventBase(BaseModel):
    """ Campos base para um evento de calendário. """
    title: str = Field(..., description="Título do evento")
    description: Optional[str] = Field(None, description="Descrição do evento")
    start_time: datetime.datetime = Field(..., description="Data e hora de início do evento (com timezone)")
    end_time: datetime.datetime = Field(..., description="Data e hora de fim do evento (com timezone)")
    is_recurring: bool = Field(False, description="Indica se o evento é recorrente")

    @field_validator('end_time')
    @classmethod
    def end_time_must_be_after_start_time(cls, v: datetime.datetime, info) -> datetime.datetime:
        """ Valida se a hora de fim é posterior à hora de início. """
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('A hora de fim deve ser posterior à hora de início')
        return v

# --- Schema para Criação ---
class CalendarEventCreate(CalendarEventBase):
    """ Schema para criar um novo evento. """
    # user_id será definido pelo usuário autenticado
    pass

# --- Schema para Atualização ---
class CalendarEventUpdate(BaseModel):
    """ Schema para atualizar um evento. Todos os campos são opcionais. """
    model_config = ConfigDict(extra='ignore')

    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    is_recurring: Optional[bool] = None

    # Adicionar validação complexa se start/end forem atualizados juntos
    # @model_validator(mode='after')
    # def check_times(self) -> 'CalendarEventUpdate':
    #     if self.start_time and self.end_time and self.end_time <= self.start_time:
    #         raise ValueError('end_time must be after start_time')
    #     # Precisa carregar o objeto original para validar contra ele se apenas um for fornecido
    #     return self


# --- Schema para Leitura (Resposta da API) ---
class CalendarEvent(CalendarEventBase):
    """ Schema completo para retornar dados de um evento. """
    event_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True) # Modo ORM


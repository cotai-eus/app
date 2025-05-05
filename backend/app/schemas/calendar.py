from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CalendarEventBase(BaseModel):
    """
    # Campos base para evento de calendário
    # Base fields for calendar event
    """
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    type: str = "other"  # deadline, meeting, visit, other
    is_recurring: bool = False


class CalendarEventCreate(CalendarEventBase):
    """
    # Campos para criação de evento de calendário
    # Fields for calendar event creation
    """
    @field_validator("end_time")
    def end_time_after_start_time(cls, v, values):
        if "start_time" in values.data and v <= values.data["start_time"]:
            raise ValueError("O horário de término deve ser após o horário de início")
        return v


class CalendarEventUpdate(BaseModel):
    """
    # Campos para atualização de evento de calendário
    # Fields for calendar event update
    """
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    type: Optional[str] = None
    is_recurring: Optional[bool] = None
    
    @field_validator("end_time")
    def end_time_after_start_time(cls, v, values):
        if v and "start_time" in values.data and values.data["start_time"] and v <= values.data["start_time"]:
            raise ValueError("O horário de término deve ser após o horário de início")
        return v


class CalendarEventInDB(CalendarEventBase):
    """
    # Modelo de evento de calendário no banco de dados
    # Calendar event model in the database
    """
    event_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CalendarEventPublic(CalendarEventBase):
    """
    # Modelo de evento de calendário para resposta pública
    # Calendar event model for public response
    """
    event_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

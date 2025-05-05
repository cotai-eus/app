import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.base import BaseSchema, IdMixin, TimestampMixin

class CalendarEventBase(BaseSchema):
    """
    Schema base para dados de evento de calendário.
    """
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_recurring: bool = False


class CalendarEventCreate(CalendarEventBase):
    """
    Schema para criação de evento de calendário.
    """
    pass


class CalendarEventUpdate(BaseSchema):
    """
    Schema para atualização de evento de calendário.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_recurring: Optional[bool] = None


class CalendarEventInDBBase(CalendarEventBase, IdMixin, TimestampMixin):
    """
    Schema para evento de calendário em banco de dados.
    """
    user_id: uuid.UUID


class CalendarEvent(CalendarEventInDBBase):
    """
    Schema para retorno de evento de calendário nas APIs.
    """
    pass


class CalendarEventInDB(CalendarEventInDBBase):
    """
    Schema para uso interno.
    """
    pass
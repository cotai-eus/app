from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

# Base schema
class CalendarEventBase(BaseModel):
    """Esquema base para eventos de calendário."""
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    all_day: bool = False
    location: Optional[str] = None
    event_type: Optional[str] = None

# Create schema
class CalendarEventCreate(CalendarEventBase):
    """Esquema para criação de um evento de calendário."""
    pass

# Update schema
class CalendarEventUpdate(BaseModel):
    """Esquema para atualização de um evento de calendário."""
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    all_day: Optional[bool] = None
    location: Optional[str] = None
    event_type: Optional[str] = None

# Database schema - The missing class that's causing the error
class CalendarEventInDB(CalendarEventBase):
    """Esquema para eventos de calendário armazenados no banco de dados."""
    event_id: UUID
    user_id: UUID
    bid_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Public schema (response)
class CalendarEventPublic(CalendarEventBase):
    """Esquema público para eventos de calendário."""
    event_id: UUID
    user_id: UUID
    bid_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

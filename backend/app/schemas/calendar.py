from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

# Base schema
class CalendarEventBase(BaseModel):
    """Esquema base para eventos de calendário."""
    title: str = Field(..., example="Prazo final para submissão de documentos")
    description: Optional[str] = Field(None, example="Entrega de documentação para o pregão eletrônico nº 56/2023")
    date: datetime = Field(..., example="2023-07-15T00:00:00Z")
    startTime: Optional[str] = Field(None, example="14:00", pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    endTime: Optional[str] = Field(None, example="15:30", pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    type: str = Field(..., example="prazo", description="prazo, reuniao, licitacao, outro")
    priority: str = Field("media", example="alta", description="baixa, media, alta")

# Create schema
class CalendarEventCreate(CalendarEventBase):
    """Esquema para criação de um evento."""
    pass

# Update schema
class CalendarEventUpdate(BaseModel):
    """Esquema para atualização de um evento."""
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    type: Optional[str] = None
    priority: Optional[str] = None

# Public schema (response)
class CalendarEventPublic(CalendarEventBase):
    """Esquema público para eventos de calendário."""
    event_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

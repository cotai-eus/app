from typing import Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class NotificationEvent(BaseModel):
    novaLicitacao: bool = True
    prazoProximo: bool = True
    mensagemRecebida: bool = True
    sistema: bool = True

class NotificationSchedule(BaseModel):
    inicio: str = Field("08:00", pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    fim: str = Field("18:00", pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    diasUteis: bool = True

class NotificationPreferences(BaseModel):
    email: NotificationEvent
    app: NotificationEvent
    sms: NotificationEvent
    horarios: NotificationSchedule

class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = Field(None, description="light, dark, system")
    ui_density: Optional[str] = Field(None, description="compact, normal, comfortable")

class UserPreferences(BaseModel):
    config_id: UUID
    user_id: UUID
    theme: str = "system"
    ui_density: str = "normal"
    notifications: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

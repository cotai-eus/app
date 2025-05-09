from datetime import datetime  # Import datetime correctly
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from uuid import UUID

# Schema for notification preferences
class NotificationPreferences(BaseModel):
    """Esquema para preferências de notificação."""
    email_notifications: bool = True
    push_notifications: bool = True
    sms_notifications: bool = False
    notification_frequency: str = "daily"  # daily, weekly, immediate
    
    class Config:
        from_attributes = True

# Schema for user preferences
class UserPreferences(BaseModel):
    """Esquema para preferências do usuário."""
    user_id: UUID
    theme: str = "light"
    language: str = "pt-BR"
    notifications: NotificationPreferences
    created_at: datetime  # This will now work
    updated_at: datetime  # This will now work
    
    class Config:
        from_attributes = True

# Schema for updating user preferences
class UserPreferencesUpdate(BaseModel):
    """Esquema para atualização das preferências do usuário."""
    theme: Optional[str] = None
    language: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    
    class Config:
        from_attributes = True
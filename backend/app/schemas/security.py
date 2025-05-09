from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserSession(BaseModel):
    id: str
    device: str
    ip: str
    location: str
    lastActive: datetime
    current: bool

class SecuritySettings(BaseModel):
    two_factor_enabled: bool = False

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class ApiKeyCreate(BaseModel):
    name: str
    permissions: list[str]

class ApiKey(BaseModel):
    id: str
    name: str
    key: str
    createdAt: datetime
    lastUsed: Optional[datetime] = None
    permissions: list[str]

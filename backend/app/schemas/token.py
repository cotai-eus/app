from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.schemas.user import UserPublic


class Token(BaseModel):
    """
    # Resposta do endpoint de token
    # Token endpoint response
    """
    access_token: str
    refresh_token: str
    token_type: str
    user: UserPublic


class TokenPayload(BaseModel):
    """
    # Payload do token JWT
    # JWT token payload
    """
    sub: Optional[str] = None
    exp: Optional[datetime] = None
    type: Optional[str] = None

    @property
    def user_id(self) -> str:
        return self.sub


class LoginRequest(BaseModel):
    """
    # Solicitação de login
    # Login request
    """
    username: str  # Email ou nome de usuário / Email or username
    password: str
    remember_me: bool = False


class RefreshToken(BaseModel):
    """
    # Refresh token
    """
    refresh_token: str
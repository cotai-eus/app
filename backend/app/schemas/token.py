from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    # Resposta do endpoint de token
    # Token endpoint response
    """
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    # Payload do token JWT
    # JWT token payload
    """
    sub: str
    exp: datetime
    
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
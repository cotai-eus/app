import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

from app.schemas.base import BaseSchema, IdMixin, TimestampMixin

class UserBase(BaseSchema):
    """
    Schema base para dados do usuário.
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: bool = False


class UserCreate(UserBase):
    """
    Schema para criação de usuário.
    """
    username: str
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    """
    Schema para atualização de usuário.
    """
    password: Optional[str] = None


class UserInDBBase(UserBase, IdMixin, TimestampMixin):
    """
    Schema para usuário em banco de dados.
    """
    username: str
    email: EmailStr
    last_login: Optional[datetime] = None


class User(UserInDBBase):
    """
    Schema para retorno de usuário nas APIs.
    """
    pass


class UserInDB(UserInDBBase):
    """
    Schema para usuário com hash de senha para uso interno.
    """
    password_hash: str
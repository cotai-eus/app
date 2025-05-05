from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """
    # Campos base para usuário
    # Base fields for user
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    """
    # Campos para criação de usuário
    # Fields for user creation
    """
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    
    @field_validator("username")
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("O nome de usuário deve conter apenas letras e números")
        return v


class UserCreateDB(UserCreate):
    """
    # Modelo para criação de usuário no banco de dados (com hash de senha)
    # Model for creating a user in the database (with password hash)
    """
    password_hash: str
    password: None = None


class UserUpdate(UserBase):
    """
    # Campos para atualização de usuário (por admin)
    # Fields for user update (by admin)
    """
    password: Optional[str] = Field(None, min_length=8) # Admin might reset password
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserUpdateMe(UserBase):
    """
    # Campos para atualização do próprio usuário
    # Fields for updating own user profile
    """
    password: Optional[str] = Field(None, min_length=8) # User can change their own password
    # Inherits email, username, first_name, last_name, avatar_url from UserBase
    # Does not include is_active or is_admin


class UserUpdateDB(BaseModel):
    """
    # Modelo para atualização de usuário no banco de dados
    # Model for updating a user in the database
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password_hash: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserInDB(UserBase):
    """
    # Modelo de usuário completo no banco de dados
    # Complete user model in the database
    """
    user_id: UUID
    is_admin: bool = False
    password_hash: str
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserPublic(UserBase):
    """
    # Modelo de usuário para resposta pública
    # User model for public response
    """
    user_id: UUID
    is_admin: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserWithPassword(UserPublic):
    """
    # Modelo de usuário incluindo hash de senha (apenas para uso interno)
    # User model including password hash (for internal use only)
    """
    password_hash: str


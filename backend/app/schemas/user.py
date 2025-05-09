from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Base schema
class UserBase(BaseModel):
    """Esquema base para usuários."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: bool = False

# Create schema
class UserCreate(UserBase):
    """Esquema para criação de um usuário."""
    username: str
    email: EmailStr
    password: str
    full_name: str
    avatar_url: Optional[str] = None

# Database Create schema
class UserCreateDB(UserBase):
    """Esquema para criação de usuário no banco de dados."""
    email: str
    password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False

# Update schema
class UserUpdate(UserBase):
    """Esquema para atualização de um usuário."""
    password: Optional[str] = None
    avatar_url: Optional[str] = None

# Update schema for user's own profile
class UserUpdateMe(BaseModel):
    """Esquema para usuário atualizar o próprio perfil."""
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    
    class Config:
        from_attributes = True

# Database Update schema
class UserUpdateDB(BaseModel):
    """Esquema para atualização de usuário no banco de dados."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

# User with password schema
class UserWithPassword(UserBase):
    """Esquema para usuário com senha."""
    password: str
    email: str
    is_active: bool = True
    is_superuser: bool = False

# Database schema
class UserInDB(UserBase):
    """Esquema para usuários armazenados no banco de dados."""
    user_id: UUID
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Public schema (response)
class UserPublic(UserBase):
    """Esquema público para usuários."""
    user_id: UUID
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Profile schemas for frontend integration
class UserProfile(BaseModel):
    """Esquema para perfil do usuário."""
    id: str
    nome: str
    email: str
    cpf: str
    telefone: str
    cargo: str
    departamento: str
    avatarUrl: Optional[str] = None

class UserProfileUpdate(BaseModel):
    """Esquema para atualização do perfil do usuário."""
    nome: str
    email: str
    cpf: str
    telefone: str
    cargo: str
    departamento: str


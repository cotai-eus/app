from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import decode_token
from app.crud.crud_user import user as crud_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import TokenPayload

# Define o esquema de autenticação OAuth2 com o endpoint de obtenção de token
# Defines the OAuth2 authentication scheme with the token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    # Obtém o usuário atual através do token JWT
    # Gets the current user from the JWT token
    
    Args:
        db: Sessão do banco de dados
        token: Token JWT de autenticação
        
    Returns:
        O objeto de usuário autenticado
        
    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    try:
        token_data = decode_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await crud_user.get(db, id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo",
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    # Verifica se o usuário atual está ativo
    # Checks if the current user is active
    
    Args:
        current_user: Usuário atual obtido do token
        
    Returns:
        O objeto de usuário ativo
        
    Raises:
        HTTPException: Se o usuário não estiver ativo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo",
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    # Verifica se o usuário atual é um administrador
    # Checks if the current user is an administrator
    
    Args:
        current_user: Usuário atual obtido do token
        
    Returns:
        O objeto de usuário administrador
        
    Raises:
        HTTPException: Se o usuário não for um administrador
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissões insuficientes",
        )
    return current_user


async def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    # Verifica se o usuário atual está ativo e é um administrador
    # Checks if the current user is active and an administrator

    Args:
        current_user: Usuário atual obtido do token

    Returns:
        O objeto de usuário ativo e administrador

    Raises:
        HTTPException: Se o usuário não estiver ativo ou não for um administrador
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo"
        )
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissões insuficientes",
        )
    return current_user
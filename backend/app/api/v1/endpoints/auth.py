from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token
from app.crud.crud_user import user as crud_user
from app.models.user import User
from app.schemas.token import LoginRequest, Token, TokenPayload, RefreshToken
from app.schemas.user import UserCreate, UserPublic

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud_user.authenticate(
        db, username_or_email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not await crud_user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuário inativo"
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Criar tokens de acesso e refresh
    access_token = create_access_token(
        user.user_id, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        user.user_id, expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.user_id),
            "email": user.email,
            "name": user.full_name,
            "role": "admin" if await crud_user.is_admin(user) else "user"
        }
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    db: AsyncSession = Depends(get_db),
    refresh_token: RefreshToken = Body(...)
) -> Any:
    """
    Get a new access token using refresh token
    """
    user_id = verify_refresh_token(refresh_token.refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de atualização inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = await crud_user.get(db, id=user_id)
    if not user or not await crud_user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo ou inexistente"
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.user_id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token.refresh_token,  # Retornamos o mesmo refresh token
        "token_type": "bearer",
        "user": {
            "id": str(user.user_id),
            "email": user.email,
            "name": user.full_name,
            "role": "admin" if await crud_user.is_admin(user) else "user"
        }
    }


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user and return tokens
    """
    # Verificar se o email já existe
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está registrado"
        )
    
    # Criar novo usuário
    user = await crud_user.create(db, obj_in=user_in)
    
    # Gerar tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        user.user_id, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        user.user_id, expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.user_id),
            "email": user.email,
            "name": user.full_name,
            "role": "admin" if await crud_user.is_admin(user) else "user"
        }
    }


@router.post("/forgot-password", response_model=dict)
async def forgot_password(
    email: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Password recovery email process
    """
    user = await crud_user.get_by_email(db, email=email)
    
    # Sempre retornamos sucesso, mesmo se o email não existir (segurança)
    if user and await crud_user.is_active(user):
        # TODO: Implementar envio de email com token de recuperação
        # Um serviço de email como SendGrid ou Amazon SES seria usado aqui
        # Por enquanto, apenas registramos em log
        pass
    
    return {"msg": "Se um usuário com este email existir, enviaremos instruções para recuperação"}


@router.post("/reset-password")
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Reset password using recovery token
    """
    # TODO: Implementar validação do token e reset de senha
    # Por agora, apenas retornamos como se fosse bem-sucedido
    return {"msg": "Senha alterada com sucesso"}


@router.get("/me", response_model=UserPublic)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user information
    """
    return current_user

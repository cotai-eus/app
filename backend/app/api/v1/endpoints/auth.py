from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.crud.crud_user import user as crud_user
from app.models.user import User
from app.schemas.token import LoginRequest, Token
from app.schemas.user import UserCreate, UserPublic

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    # Endpoint para obtenção de token de acesso OAuth2
    # OAuth2 compatible token login endpoint
    
    Args:
        db: Sessão do banco de dados
        form_data: Dados do formulário de login OAuth2
        
    Returns:
        Token de acesso JWT
    """
    user = await crud_user.authenticate(
        db, identifier=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou senha incorretos",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuário inativo"
        )
    
    # Atualiza último login
    # Updates last login time
    await crud_user.update(db, db_obj=user, obj_in={"last_login": "now()"})
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.user_id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db),
    login_data: LoginRequest = Body(...)
) -> Any:
    """
    # Login com email/nome de usuário e senha
    # Login with email/username and password
    
    Args:
        db: Sessão do banco de dados
        login_data: Dados de login
        
    Returns:
        Token de acesso JWT
    """
    user = await crud_user.authenticate(
        db, identifier=login_data.username, password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou senha incorretos",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuário inativo"
        )
    
    # Atualiza último login
    # Updates last login time
    await crud_user.update(db, db_obj=user, obj_in={"last_login": "now()"})
    
    # Se o usuário selecionou "lembrar de mim", aumenta o tempo de expiração do token
    # If the user selected "remember me", increase the token expiration time
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    if login_data.remember_me:
        # Aumenta para 30 dias se "lembrar de mim" estiver ativado
        # Increase to 30 days if "remember me" is enabled
        access_token_expires = timedelta(days=30)
    
    return {
        "access_token": create_access_token(
            user.user_id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/signup", response_model=UserPublic)
async def register(
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate = Body(...)
) -> Any:
    """
    # Cria um novo usuário
    # Create a new user
    
    Args:
        db: Sessão do banco de dados
        user_in: Dados do usuário a ser criado
        
    Returns:
        O usuário criado
    """
    # Verifica se já existe um usuário com este email
    # Check if a user with this email already exists
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está sendo usado por outro usuário",
        )
    
    # Verifica se já existe um usuário com este nome de usuário
    # Check if a user with this username already exists
    user = await crud_user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este nome de usuário já está sendo usado",
        )
    
    # Cria o usuário
    # Create the user
    user = await crud_user.create(db, obj_in=user_in)
    return user


@router.post("/test-token", response_model=UserPublic)
async def test_token(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    # Endpoint de teste para validar o token
    # Test endpoint to validate the token
    
    Args:
        current_user: Usuário atual obtido do token
        
    Returns:
        O usuário atual
    """
    return current_user

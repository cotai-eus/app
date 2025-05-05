import os
import secrets
import uuid
from datetime import datetime
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.active_session import ActiveSession
from app.models.api_key import ApiKey
from app.models.user import User
from app.schemas.api_key import ApiKeyCreate, ApiKeyCreateResponse, ApiKeyPublic
from app.schemas.session import ActiveSessionPublic

router = APIRouter()

# Criar instâncias CRUD para chaves de API e sessões ativas
# Create CRUD instances for API keys and active sessions
crud_api_key = CRUDBase(ApiKey)
crud_session = CRUDBase(ActiveSession)


@router.get("/api-keys", response_model=List[ApiKeyPublic])
async def read_api_keys(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter chaves de API do usuário atual
    # Get API keys of the current user
    
    Args:
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Lista de chaves de API
    """
    # Filtrar chaves pelo ID do usuário atual
    # Filter keys by current user ID
    stmt = select(ApiKey).where(ApiKey.user_id == current_user.user_id)
    result = await db.execute(stmt)
    
    return result.scalars().all()


@router.post("/api-keys", response_model=ApiKeyCreateResponse)
async def create_api_key(
    db: AsyncSession = Depends(get_db),
    api_key_in: ApiKeyCreate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Criar uma nova chave de API
    # Create a new API key
    
    Args:
        db: Sessão do banco de dados
        api_key_in: Dados da chave de API a ser criada
        current_user: Usuário atual obtido do token
        
    Returns:
        A chave de API criada com o valor completo (visível apenas uma vez)
    """
    # Gerar chave aleatória
    # Generate random key
    key = secrets.token_urlsafe(32)
    prefix = key[:8]
    
    # Hash da chave para armazenamento
    # Hash the key for storage
    hashed_key = get_password_hash(key)
    
    # Criar objeto de chave de API incluindo o ID do usuário atual
    # Create API key object including the current user ID
    api_key_data = api_key_in.model_dump()
    api_key_data["user_id"] = current_user.user_id
    api_key_data["prefix"] = prefix
    api_key_data["hashed_key"] = hashed_key
    
    # Criar a chave de API
    # Create the API key
    db_api_key = ApiKey(**api_key_data)
    db.add(db_api_key)
    await db.commit()
    await db.refresh(db_api_key)
    
    # Retornar com a chave completa (visível apenas uma vez)
    # Return with full key (visible only once)
    return ApiKeyCreateResponse(
        key_id=db_api_key.key_id,
        name=db_api_key.name,
        prefix=db_api_key.prefix,
        key=key
    )


@router.delete("/api-keys/{key_id}", response_model=ApiKeyPublic)
async def delete_api_key(
    key_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Excluir uma chave de API
    # Delete an API key
    
    Args:
        key_id: ID da chave de API
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        A chave de API excluída
    """
    api_key = await crud_api_key.get(db, id=key_id)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chave de API não encontrada",
        )
    
    # Verificar se a chave pertence ao usuário atual
    # Check if the key belongs to the current user
    if api_key.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a esta chave de API",
        )
    
    # Excluir a chave
    # Delete the key
    api_key = await crud_api_key.remove(db, id=key_id)
    return api_key


@router.get("/sessions", response_model=List[ActiveSessionPublic])
async def read_active_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter sessões ativas do usuário atual
    # Get active sessions of the current user
    
    Args:
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Lista de sessões ativas
    """
    # Filtrar sessões pelo ID do usuário atual
    # Filter sessions by current user ID
    stmt = select(ActiveSession).where(ActiveSession.user_id == current_user.user_id)
    result = await db.execute(stmt)
    
    return result.scalars().all()


@router.post("/sessions/current", response_model=ActiveSessionPublic)
async def register_current_session(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Registrar a sessão atual
    # Register the current session
    
    Args:
        request: Objeto de solicitação HTTP
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        A sessão ativa criada
    """
    # Obter informações do cliente
    # Get client information
    user_agent = request.headers.get("user-agent", "Unknown")
    ip_address = request.client.host
    
    # Criar objeto de sessão
    # Create session object
    session_data = {
        "user_id": current_user.user_id,
        "device_info": user_agent,
        "ip_address": ip_address,
        "last_accessed_at": datetime.utcnow()
    }
    
    # Criar a sessão
    # Create the session
    db_session = ActiveSession(**session_data)
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    
    return db_session


@router.delete("/sessions/{session_id}", response_model=ActiveSessionPublic)
async def delete_active_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Encerrar uma sessão ativa
    # End an active session
    
    Args:
        session_id: ID da sessão
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        A sessão encerrada
    """
    session = await crud_session.get(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada",
        )
    
    # Verificar se a sessão pertence ao usuário atual
    # Check if the session belongs to the current user
    if session.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a esta sessão",
        )
    
    # Excluir a sessão
    # Delete the session
    session = await crud_session.remove(db, id=session_id)
    return session

    op.create_index(op.f('ix_active_session_user_id'), 'active_session', ['user_id'], unique=False)

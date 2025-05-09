from typing import Any, List
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.api.deps import get_current_user, get_db
from app.models.api_key import ApiKey
from app.models.user import User
from app.schemas.security import ApiKeyCreate, ApiKey as ApiKeySchema

router = APIRouter()

@router.post("", response_model=ApiKeySchema, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    *,
    db: AsyncSession = Depends(get_db),
    api_key_in: ApiKeyCreate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Criar uma nova chave API
    # Create a new API key
    """
    # Gerar chave segura
    key = f"{uuid4()}-{uuid4()}"
    
    # Criar registro da chave API
    db_api_key = ApiKey(
        name=api_key_in.name,
        key=key,
        permissions=api_key_in.permissions,
        user_id=current_user.user_id,
    )
    
    db.add(db_api_key)
    await db.commit()
    await db.refresh(db_api_key)
    
    # Retornar o objeto completo incluindo a chave
    return {
        "id": str(db_api_key.key_id),
        "name": db_api_key.name,
        "key": key,  # Retornar a chave apenas uma vez durante a criação
        "createdAt": db_api_key.created_at,
        "lastUsed": db_api_key.last_used,
        "permissions": db_api_key.permissions,
    }

@router.get("", response_model=List[ApiKeySchema])
async def get_api_keys(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter todas as chaves API do usuário
    # Get all API keys of the user
    """
    stmt = select(ApiKey).where(ApiKey.user_id == current_user.user_id)
    result = await db.execute(stmt)
    api_keys = result.scalars().all()
    
    # Retornar as chaves, mas sem exibir o valor completo da chave
    return [{
        "id": str(key.key_id),
        "name": key.name,
        "key": f"{key.key[:8]}...{key.key[-8:]}",  # Mostrar apenas parte da chave
        "createdAt": key.created_at,
        "lastUsed": key.last_used,
        "permissions": key.permissions,
    } for key in api_keys]

@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    *,
    db: AsyncSession = Depends(get_db),
    key_id: UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """
    # Excluir uma chave API
    # Delete an API key
    """
    stmt = select(ApiKey).where(ApiKey.key_id == key_id)
    result = await db.execute(stmt)
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chave API não encontrada",
        )
    
    # Verificar se a chave pertence ao usuário
    if api_key.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a esta chave API",
        )
    
    # Excluir a chave
    await db.delete(api_key)
    await db.commit()

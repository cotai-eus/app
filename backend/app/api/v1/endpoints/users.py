from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Import directly from app.api.deps instead of using the bridge
from app.api.deps import get_current_admin_user, get_current_user, get_db
from app.crud.crud_user import user as crud_user
from app.models.user import User
from app.schemas.user import UserPublic, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter informações do usuário atual
    # Get current user information
    
    Args:
        current_user: Usuário atual obtido do token
        
    Returns:
        Informações do usuário atual
    """
    return current_user


@router.put("/me", response_model=UserPublic)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar informações do usuário atual
    # Update current user information
    
    Args:
        db: Sessão do banco de dados
        user_in: Dados de atualização do usuário
        current_user: Usuário atual obtido do token
        
    Returns:
        Informações atualizadas do usuário
    """
    # Verificar se o email está sendo alterado e se já existe
    if user_in.email and user_in.email != current_user.email:
        user_by_email = await crud_user.get_by_email(db, email=user_in.email)
        if user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email já está em uso."
            )
    
    # Atualizar avatar se fornecido
    if hasattr(user_in, 'avatar_url') and user_in.avatar_url:
        # Poderia integrar com um serviço de armazenamento como S3
        # Por enquanto, apenas aceitamos o URL
        pass
        
    user = await crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("", response_model=List[UserPublic])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    # Obter lista de usuários (apenas administradores)
    # Get list of users (admin only)
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros para pular
        limit: Número máximo de registros para retornar
        current_user: Usuário atual (admin) obtido do token
        
    Returns:
        Lista de usuários
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    # Obter detalhes de um usuário específico (apenas administradores)
    # Get details of a specific user (admin only)
    
    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        current_user: Usuário atual (admin) obtido do token
        
    Returns:
        Detalhes do usuário solicitado
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    return user


@router.put("/{user_id}", response_model=UserPublic)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str,
    user_in: UserUpdate = Body(...),
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    # Atualizar informações de um usuário específico (apenas administradores)
    # Update information of a specific user (admin only)
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário
        user_in: Dados de atualização do usuário
        current_user: Usuário atual (admin) obtido do token
        
    Returns:
        Informações atualizadas do usuário
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    user = await crud_user.update(db, db_obj=user, obj_in=user_in)
    return user

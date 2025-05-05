from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from uuid import UUID
import logging

from app import crud, models
from app.api import deps
from app.schemas.user import UserPublic, UserCreate, UserUpdate, UserUpdateMe
from app.models.user import User  # Add this import

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
    # current_user: models.User = Depends(deps.get_current_active_admin), # Descomente para exigir admin
) -> Any:
    """
    Cria um novo usuário.
    (Restringir a administradores se necessário).
    """
    # Comentário em português: Verifica se já existe usuário com o mesmo email ou username.
    existing_user_email = await crud.user.get_by_email(db, email=user_in.email)
    if existing_user_email:
        log.warning(f"Tentativa de criar usuário com email já existente: {user_in.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um usuário com este email já existe no sistema.",
        )
    existing_user_username = await crud.user.get_by_username(db, username=user_in.username)
    if existing_user_username:
        log.warning(f"Tentativa de criar usuário com username já existente: {user_in.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um usuário com este nome de usuário já existe no sistema.",
        )

    # Comentário em português: Cria o usuário usando o CRUD.
    user = await crud.user.create(db=db, obj_in=user_in)
    log.info(f"Novo usuário criado: {user.email} (ID: {user.user_id})")
    return user

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém os dados do usuário atualmente autenticado.
    """
    # Comentário em português: Retorna o usuário obtido pela dependência.
    return current_user

@router.put("/me", response_model=UserPublic)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserUpdateMe,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Atualiza os dados do próprio usuário autenticado.
    """
    # Comentário em português: Verifica se o novo email já está em uso por outro usuário.
    if user_in.email and user_in.email != current_user.email:
        existing_user = await crud.user.get_by_email(db, email=user_in.email)
        if existing_user and existing_user.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email já está sendo usado por outra conta.",
            )

    # Comentário em português: Atualiza o usuário usando o CRUD.
    # O método update do CRUDUser lida com o hashing da nova senha, se fornecida.
    updated_user = await crud.user.update(db=db, db_obj=current_user, obj_in=user_in)
    log.info(f"Usuário atualizou seu perfil: {updated_user.email}")
    return updated_user


@router.get("/", response_model=List[UserPublic])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=200, description="Número máximo de registros a retornar"),
    current_user: models.User = Depends(deps.get_current_active_admin), # Requer admin
) -> Any:
    """
    Obtém uma lista de usuários (requer privilégios de administrador).
    """
    # Comentário em português: Busca múltiplos usuários usando o CRUD com paginação.
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserPublic) # Changed User to UserPublic
async def read_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user), # Qualquer usuário ativo pode ver outros? Ou só admin?
) -> Any:
    """
    Obtém um usuário específico pelo seu ID.
    (Ajustar permissões conforme necessário - admin ou usuário logado).
    """
    # Comentário em português: Busca o usuário pelo ID fornecido.
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Comentário em português: Verifica permissão - o próprio usuário ou um admin podem ver.
    if user.user_id != current_user.user_id and not current_user.is_admin:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    return user


@router.put("/{user_id}", response_model=UserPublic) # Changed User to UserPublic
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: UUID,
    user_in: UserUpdate, # Schema sem senha
    current_user: models.User = Depends(deps.get_current_active_admin), # Requer admin
) -> Any:
    """
    Atualiza um usuário existente (requer privilégios de administrador).
    Não permite atualizar senha por esta rota.
    """
    # Comentário em português: Busca o usuário a ser atualizado.
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O usuário com este ID não existe no sistema",
        )

    # Comentário em português: Atualiza o usuário usando o CRUD.
    updated_user = await crud.user.update(db=db, db_obj=user, obj_in=user_in)
    log.info(f"Admin {current_user.email} atualizou usuário {updated_user.email} (ID: {user_id})")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_admin), # Requer admin
) -> None:
    """
    Exclui um usuário (requer privilégios de administrador).
    """
    # Comentário em português: Busca o usuário a ser excluído.
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    if user.user_id == current_user.user_id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administradores não podem excluir a si mesmos")

    # Comentário em português: Remove o usuário usando o CRUD.
    await crud.user.remove(db=db, id=user_id)
    log.info(f"Admin {current_user.email} excluiu usuário {user.email} (ID: {user_id})")
    # Nenhum conteúdo é retornado no sucesso (204 No Content)


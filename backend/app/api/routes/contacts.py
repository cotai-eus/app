from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models, crud
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.ContactRead, status_code=status.HTTP_201_CREATED)
async def create_contact(
    *,
    db: AsyncSession = Depends(deps.get_db),
    contact_in: schemas.ContactCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Cria um novo contato para o usuário logado.
    """
    # Verificar se já existe um contato com o mesmo email para este usuário (se necessário)
    # ... lógica de verificação ...
    try:
        contact = await crud.contact.create_with_user(db=db, obj_in=contact_in, user_id=current_user.user_id)
    except Exception as e: # Capturar erro de constraint UNIQUE, por exemplo
        # Idealmente, capturar IntegrityError específico do DBAPI
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Não foi possível criar contato. Verifique os dados (possível email duplicado). Erro: {e}",
        )
    return contact

@router.get("/", response_model=List[schemas.ContactRead])
async def read_contacts(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Recupera a lista de contatos do usuário logado.
    """
    contacts = await crud.contact.get_multi_by_user(
        db=db, user_id=current_user.user_id, skip=skip, limit=limit
    )
    return contacts

@router.get("/{contact_id}", response_model=schemas.ContactRead)
async def read_contact(
    *,
    db: AsyncSession = Depends(deps.get_db),
    contact_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Recupera um contato específico pelo ID.
    """
    contact = await crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado")
    # Verificar se o contato pertence ao usuário logado
    if contact.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este contato")
    return contact

@router.put("/{contact_id}", response_model=schemas.ContactRead)
async def update_contact(
    *,
    db: AsyncSession = Depends(deps.get_db),
    contact_id: UUID,
    contact_in: schemas.ContactUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Atualiza um contato existente.
    """
    contact = await crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado")
    if contact.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este contato")

    contact = await crud.contact.update(db=db, db_obj=contact, obj_in=contact_in)
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    *,
    db: AsyncSession = Depends(deps.get_db),
    contact_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> None:
    """
    Deleta um contato.
    """
    contact = await crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado")
    if contact.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a deletar este contato")

    await crud.contact.remove(db=db, id=contact_id)
    # Nenhum conteúdo é retornado no sucesso (204)
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from uuid import UUID
import logging

from app import crud, models, schemas
from app.api import deps

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/", response_model=schemas.Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(
    *,
    db: AsyncSession = Depends(deps.get_db),
    contact_in: schemas.ContactCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Cria um novo contato para o usuário autenticado.
    """
    # Comentário em português: Cria o contato associado ao usuário logado.
    try:
        contact = await crud.contact.create_with_owner(db=db, obj_in=contact_in, user_id=current_user.user_id)
        log.info(f"Usuário {current_user.email} criou contato {contact.contact_id}")
        return contact
    except Exception as e: # Captura erro de constraint (e.g., email duplicado para o mesmo user)
        await db.rollback()
        log.error(f"Erro ao criar contato para {current_user.email}: {e}")
        # Verifica se o erro é de violação de constraint única (depende do DB e driver)
        # if "UniqueViolationError" in str(type(e.__cause__)): # Exemplo com psycopg
        if hasattr(e, 'orig') and 'unique constraint' in str(e.orig).lower(): # Tentativa genérica
             raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail="Um contato com este e-mail já existe para este usuário.",
             )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar contato."
        )


@router.get("/", response_model=List[schemas.Contact])
async def read_contacts(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém a lista de contatos do usuário autenticado.
    """
    # Comentário em português: Busca os contatos do usuário logado com paginação.
    contacts = await crud.contact.get_multi_by_owner(
        db=db, user_id=current_user.user_id, skip=skip, limit=limit
    )
    return contacts

@router.get("/{contact_id}", response_model=schemas.Contact)
async def read_contact(
    *,
    db: AsyncSession = Depends(deps.get_db),
    contact_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém um contato específico pelo ID.
    """
    # Comentário em português: Busca o contato pelo ID.
    contact = await crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado")
    # Comentário em português: Verifica se o contato pertence ao usuário logado.
    if contact.user_id != current_user.user_id:
        log.warning(f"Usuário {current_user.email} tentou acessar contato {contact_id} de outro usuário.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")
    return contact

@router.put("/{contact_id}", response_model=schemas.Contact)
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
    # Comentário em português: Busca o contato a ser atualizado.
    contact = await crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado")
    # Comentário em português: Verifica se o contato pertence ao usuário logado.
    if contact.user_id != current_user.user_id:
        log.warning(f"Usuário {current_user.email} tentou atualizar contato {contact_id} de outro usuário.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Comentário em português: Atualiza o contato usando o CRUD.
    try:
        updated_contact = await crud.contact.update(db=db, db_obj=contact, obj_in=contact_in)
        log.info(f"Usuário {current_user.email} atualizou contato {contact_id}")
        return updated_contact
    except Exception as e: # Captura erro de constraint
        await db.rollback()
        log.error(f"Erro ao atualizar contato {contact_id} para {current_user.email}: {e}")
        if hasattr(e, 'orig') and 'unique constraint' in str(e.orig).lower():
             raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail="Um contato com este e-mail já existe para este usuário.",
             )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar contato."
        )


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    *,
    db: AsyncSession = Depends(deps.get_db),
    contact_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> None:
    """
    Exclui um contato.
    """
    # Comentário em português: Busca o contato a ser excluído.
    contact = await crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado")
    # Comentário em português: Verifica se o contato pertence ao usuário logado.
    if contact.user_id != current_user.user_id:
        log.warning(f"Usuário {current_user.email} tentou excluir contato {contact_id} de outro usuário.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Comentário em português: Remove o contato usando o CRUD.
    await crud.contact.remove(db=db, id=contact_id)
    log.info(f"Usuário {current_user.email} excluiu contato {contact_id}")
    # Retorna 204 No Content


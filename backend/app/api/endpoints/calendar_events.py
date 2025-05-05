from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from uuid import UUID
import datetime
import logging

from app import crud, models, schemas
from app.api import deps

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/", response_model=schemas.CalendarEvent, status_code=status.HTTP_201_CREATED)
async def create_calendar_event(
    *,
    db: AsyncSession = Depends(deps.get_db),
    event_in: schemas.CalendarEventCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Cria um novo evento de calendário para o usuário autenticado.
    """
    # Comentário em português: Cria o evento associado ao usuário logado.
    event = await crud.calendar_event.create_with_owner(
        db=db, obj_in=event_in, user_id=current_user.user_id
    )
    log.info(f"Usuário {current_user.email} criou evento {event.event_id} ('{event.title}')")
    return event

@router.get("/", response_model=List[schemas.CalendarEvent])
async def read_calendar_events(
    *,
    db: AsyncSession = Depends(deps.get_db),
    start_time: datetime.datetime = Query(..., description="Início do intervalo de busca (ISO 8601 com timezone)"),
    end_time: datetime.datetime = Query(..., description="Fim do intervalo de busca (ISO 8601 com timezone)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=2000), # Limite maior para calendário
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém a lista de eventos de calendário do usuário autenticado dentro de um intervalo de tempo.
    """
    # Comentário em português: Valida se o intervalo de tempo é razoável (opcional).
    if end_time <= start_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A data/hora final deve ser posterior à inicial.")
    # if (end_time - start_time) > datetime.timedelta(days=90): # Limita a busca a 90 dias, por exemplo
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O intervalo de busca não pode exceder 90 dias.")

    # Comentário em português: Busca os eventos do usuário no intervalo especificado.
    events = await crud.calendar_event.get_multi_by_owner_and_time_range(
        db=db, user_id=current_user.user_id, start_time=start_time, end_time=end_time, skip=skip, limit=limit
    )
    return events

@router.get("/{event_id}", response_model=schemas.CalendarEvent)
async def read_calendar_event(
    *,
    db: AsyncSession = Depends(deps.get_db),
    event_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém um evento de calendário específico pelo ID.
    """
    # Comentário em português: Busca o evento pelo ID.
    event = await crud.calendar_event.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    # Comentário em português: Verifica se o evento pertence ao usuário logado.
    if event.user_id != current_user.user_id:
        log.warning(f"Usuário {current_user.email} tentou acessar evento {event_id} de outro usuário.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")
    return event

@router.put("/{event_id}", response_model=schemas.CalendarEvent)
async def update_calendar_event(
    *,
    db: AsyncSession = Depends(deps.get_db),
    event_id: UUID,
    event_in: schemas.CalendarEventUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Atualiza um evento de calendário existente.
    """
    # Comentário em português: Busca o evento a ser atualizado.
    event = await crud.calendar_event.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    # Comentário em português: Verifica se o evento pertence ao usuário logado.
    if event.user_id != current_user.user_id:
        log.warning(f"Usuário {current_user.email} tentou atualizar evento {event_id} de outro usuário.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Comentário em português: Atualiza o evento usando o CRUD.
    # Validação de start/end time pode ser necessária aqui se forem atualizados parcialmente.
    # O schema Pydantic já valida se ambos forem fornecidos juntos.
    updated_event = await crud.calendar_event.update(db=db, db_obj=event, obj_in=event_in)
    log.info(f"Usuário {current_user.email} atualizou evento {event_id}")
    return updated_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calendar_event(
    *,
    db: AsyncSession = Depends(deps.get_db),
    event_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> None:
    """
    Exclui um evento de calendário.
    """
    # Comentário em português: Busca o evento a ser excluído.
    event = await crud.calendar_event.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    # Comentário em português: Verifica se o evento pertence ao usuário logado.
    if event.user_id != current_user.user_id:
        log.warning(f"Usuário {current_user.email} tentou excluir evento {event_id} de outro usuário.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Comentário em português: Remove o evento usando o CRUD.
    await crud.calendar_event.remove(db=db, id=event_id)
    log.info(f"Usuário {current_user.email} excluiu evento {event_id}")
    # Retorna 204 No Content


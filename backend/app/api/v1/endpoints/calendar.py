from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.base import CRUDBase
from app.models.calendar_event import CalendarEvent
from app.models.user import User
from app.schemas.calendar import CalendarEventCreate, CalendarEventPublic, CalendarEventUpdate

router = APIRouter()

# Criar instância CRUD para eventos de calendário
# Create CRUD instance for calendar events
crud_event = CRUDBase(CalendarEvent)


@router.get("/events", response_model=List[CalendarEventPublic])
async def read_calendar_events(
    db: AsyncSession = Depends(get_db),
    start_date: Optional[datetime] = Query(None, description="Data inicial para filtrar eventos"),
    end_date: Optional[datetime] = Query(None, description="Data final para filtrar eventos"),
    type: Optional[str] = Query(None, description="Tipo de evento"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter eventos de calendário do usuário atual com possibilidade de filtro
    # Get calendar events of the current user with filtering options
    
    Args:
        db: Sessão do banco de dados
        start_date: Data/hora inicial opcional para filtrar eventos
        end_date: Data/hora final opcional para filtrar eventos
        type: Tipo opcional de evento para filtrar
        skip: Número de registros para pular
        limit: Número máximo de registros para retornar
        current_user: Usuário atual obtido do token
        
    Returns:
        Lista de eventos de calendário
    """
    # Construir consulta base
    # Build base query
    stmt = select(CalendarEvent).where(CalendarEvent.user_id == current_user.user_id)
    
    # Adicionar filtros conforme necessário
    # Add filters as needed
    if start_date:
        stmt = stmt.where(CalendarEvent.start_time >= start_date)
    
    if end_date:
        stmt = stmt.where(CalendarEvent.end_time <= end_date)
    
    if type:
        stmt = stmt.where(CalendarEvent.type == type)
    
    # Ordenar, paginar e executar a consulta
    # Sort, paginate, and execute the query
    stmt = stmt.order_by(CalendarEvent.start_time).offset(skip).limit(limit)
    result = await db.execute(stmt)
    
    return result.scalars().all()


@router.post("/events", response_model=CalendarEventPublic)
async def create_calendar_event(
    db: AsyncSession = Depends(get_db),
    event_in: CalendarEventCreate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Criar um novo evento de calendário
    # Create a new calendar event
    
    Args:
        db: Sessão do banco de dados
        event_in: Dados do evento a ser criado
        current_user: Usuário atual obtido do token
        
    Returns:
        O evento de calendário criado
    """
    # Criar objeto de evento incluindo o ID do usuário atual
    # Create event object including the current user ID
    event_data = event_in.model_dump()
    event_data["user_id"] = current_user.user_id
    
    # Criar o evento
    # Create the event
    db_event = CalendarEvent(**event_data)
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


@router.get("/events/{event_id}", response_model=CalendarEventPublic)
async def read_calendar_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter detalhes de um evento de calendário específico
    # Get details of a specific calendar event
    
    Args:
        event_id: ID do evento
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Detalhes do evento solicitado
    """
    event = await crud_event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado",
        )
    
    # Verificar se o evento pertence ao usuário atual
    # Check if the event belongs to the current user
    if event.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este evento",
        )
    
    return event


@router.put("/events/{event_id}", response_model=CalendarEventPublic)
async def update_calendar_event(
    event_id: UUID,
    event_in: CalendarEventUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar detalhes de um evento de calendário
    # Update details of a calendar event
    
    Args:
        event_id: ID do evento
        event_in: Dados de atualização do evento
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Evento atualizado
    """
    event = await crud_event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado",
        )
    
    # Verificar se o evento pertence ao usuário atual
    # Check if the event belongs to the current user
    if event.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este evento",
        )
    
    # Verificar se o horário de término é posterior ao de início
    # Check if end time is after start time
    if event_in.start_time and event_in.end_time and event_in.start_time >= event_in.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O horário de término deve ser após o horário de início",
        )
    elif event_in.start_time and not event_in.end_time and event_in.start_time >= event.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O horário de término deve ser após o horário de início",
        )
    elif not event_in.start_time and event_in.end_time and event.start_time >= event_in.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O horário de término deve ser após o horário de início",
        )
    
    # Atualizar o evento
    # Update the event
    event = await crud_event.update(db, db_obj=event, obj_in=event_in)
    return event


@router.delete("/events/{event_id}", response_model=CalendarEventPublic)
async def delete_calendar_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Excluir um evento de calendário
    # Delete a calendar event
    
    Args:
        event_id: ID do evento
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        O evento excluído
    """
    event = await crud_event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado",
        )
    
    # Verificar se o evento pertence ao usuário atual
    # Check if the event belongs to the current user
    if event.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este evento",
        )
    
    # Excluir o evento
    # Delete the event
    event = await crud_event.remove(db, id=event_id)
    return event

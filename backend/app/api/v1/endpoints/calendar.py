from datetime import datetime, timedelta
from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.base import CRUDBase
from app.models.calendar_event import CalendarEvent
from app.models.user import User
from app.schemas.calendar import CalendarEventCreate, CalendarEventPublic, CalendarEventUpdate

router = APIRouter()

# CRUD instance for calendar events
crud_event = CRUDBase(CalendarEvent)

@router.get("/events", response_model=List[CalendarEventPublic])
async def read_calendar_events(
    db: AsyncSession = Depends(get_db),
    start_date: Optional[datetime] = Query(None, description="Data inicial para filtrar eventos"),
    end_date: Optional[datetime] = Query(None, description="Data final para filtrar eventos"),
    type: Optional[str] = Query(None, description="Tipo de evento (prazo, reuniao, licitacao, outro)"),
    priority: Optional[str] = Query(None, description="Prioridade do evento (baixa, media, alta)"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter eventos de calendário do usuário atual com possibilidade de filtro
    # Get calendar events of the current user with filtering options
    """
    # Construir consulta base
    stmt = select(CalendarEvent).where(CalendarEvent.user_id == current_user.user_id)
    
    # Adicionar filtros conforme necessário
    if start_date:
        stmt = stmt.where(CalendarEvent.date >= start_date)
    
    if end_date:
        stmt = stmt.where(CalendarEvent.date <= end_date)
    
    if type:
        stmt = stmt.where(CalendarEvent.type == type)
        
    if priority:
        stmt = stmt.where(CalendarEvent.priority == priority)
    
    # Ordenar, paginar e executar a consulta
    stmt = stmt.order_by(CalendarEvent.date).offset(skip).limit(limit)
    result = await db.execute(stmt)
    
    return result.scalars().all()


@router.post("/eventos", response_model=CalendarEventPublic)
async def create_calendar_event(
    db: AsyncSession = Depends(get_db),
    event_in: CalendarEventCreate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Criar um novo evento de calendário
    # Create a new calendar event
    """
    # Validação de datas
    if event_in.startTime and event_in.endTime and event_in.startTime > event_in.endTime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O horário de término deve ser após o horário de início"
        )
    
    # Criar objeto de evento incluindo o ID do usuário atual
    event_data = event_in.model_dump()
    event_data["user_id"] = current_user.user_id
    
    # Criar o evento
    db_event = CalendarEvent(**event_data)
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


@router.get("/eventos/{event_id}", response_model=CalendarEventPublic)
async def read_calendar_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter detalhes de um evento de calendário específico
    # Get details of a specific calendar event
    """
    event = await crud_event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado",
        )
    
    # Verificar se o evento pertence ao usuário atual
    if event.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este evento",
        )
    
    return event


@router.put("/eventos/{event_id}", response_model=CalendarEventPublic)
async def update_calendar_event(
    event_id: UUID,
    event_in: CalendarEventUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar detalhes de um evento de calendário
    # Update details of a calendar event
    """
    event = await crud_event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado",
        )
    
    # Verificar se o evento pertence ao usuário atual
    if event.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este evento",
        )
    
    # Verificar se o horário de término é posterior ao de início
    if event_in.startTime and event_in.endTime and event_in.startTime >= event_in.endTime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O horário de término deve ser após o horário de início",
        )
    
    # Atualizar o evento
    event = await crud_event.update(db, db_obj=event, obj_in=event_in)
    return event


@router.delete("/eventos/{event_id}", response_model=CalendarEventPublic)
async def delete_calendar_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Excluir um evento de calendário
    # Delete a calendar event
    """
    event = await crud_event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado",
        )
    
    # Verificar se o evento pertence ao usuário atual
    if event.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este evento",
        )
    
    # Excluir o evento
    event = await crud_event.remove(db, id=event_id)
    return event


@router.get("/prazos-proximos", response_model=List[CalendarEventPublic])
async def get_upcoming_deadlines(
    db: AsyncSession = Depends(get_db),
    days: int = Query(7, ge=1, le=30, description="Número de dias no futuro"),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter prazos importantes nos próximos dias
    # Get important deadlines in the next days
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    future_date = today + timedelta(days=days)
    
    # Buscar eventos do tipo 'prazo' dentro do período
    stmt = select(CalendarEvent).where(
        and_(
            CalendarEvent.user_id == current_user.user_id,
            CalendarEvent.type == 'prazo',
            CalendarEvent.date >= today,
            CalendarEvent.date <= future_date
        )
    ).order_by(CalendarEvent.date)
    
    result = await db.execute(stmt)
    return result.scalars().all()

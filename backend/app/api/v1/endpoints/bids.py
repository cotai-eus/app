from typing import Any, List, Optional
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.bid import Bid
from app.models.user import User
from app.schemas.bid import BidCreate, BidPublic, BidUpdate, BidStatusUpdate, BidDashboardStats

router = APIRouter()

@router.post("", response_model=BidPublic, status_code=status.HTTP_201_CREATED)
async def create_bid(
    *,
    db: AsyncSession = Depends(get_db),
    bid_in: BidCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Criar uma nova licitação
    # Create a new bid
    """
    # Criar a licitação
    bid = Bid(**bid_in.model_dump(), user_id=current_user.user_id)
    db.add(bid)
    await db.commit()
    await db.refresh(bid)
    
    return bid

@router.get("", response_model=List[BidPublic])
async def read_bids(
    db: AsyncSession = Depends(get_db),
    status: Optional[str] = Query(None, description="Filtrar por status da licitação"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter licitações
    # Get bids
    """
    # Construir consulta
    query = select(Bid)
    
    # Filtrar por status se fornecido
    if status:
        query = query.where(Bid.status == status)
    
    # Aplicar paginação
    query = query.offset(skip).limit(limit).order_by(Bid.deadline_date)
    
    # Executar consulta
    result = await db.execute(query)
    bids = result.scalars().all()
    
    return bids

@router.get("/dashboard-stats", response_model=BidDashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter estatísticas para o dashboard
    # Get dashboard statistics
    """
    # Consulta para contar licitações ativas
    active_query = select(func.count()).where(Bid.status.in_(['recebidos', 'analisados', 'enviados']))
    active_result = await db.execute(active_query)
    active_count = active_result.scalar_one()
    
    # Consulta para contar editais publicados
    published_query = select(func.count()).select_from(Bid)
    published_result = await db.execute(published_query)
    published_count = published_result.scalar_one()
    
    # Consulta para contar prazos próximos (próximos 7 dias)
    from datetime import datetime, timedelta
    today = datetime.now().date()
    upcoming_deadline = today + timedelta(days=7)
    
    deadlines_query = select(func.count()).where(
        (Bid.deadline_date >= today) & 
        (Bid.deadline_date <= upcoming_deadline)
    )
    deadlines_result = await db.execute(deadlines_query)
    deadlines_count = deadlines_result.scalar_one()
    
    # Cálculo da taxa de sucesso
    success_query = select(func.count()).where(Bid.status == 'ganho')
    success_result = await db.execute(success_query)
    success_count = success_result.scalar_one()
    
    closed_query = select(func.count()).where(Bid.status.in_(['ganho', 'perdido']))
    closed_result = await db.execute(closed_query)
    closed_count = closed_result.scalar_one()
    
    success_rate = round((success_count / closed_count * 100) if closed_count > 0 else 0)
    
    return {
        "active_bids": active_count,
        "published_notices": published_count,
        "upcoming_deadlines": deadlines_count,
        "success_rate": success_rate
    }

@router.get("/{bid_id}", response_model=BidPublic)
async def read_bid(
    *,
    db: AsyncSession = Depends(get_db),
    bid_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter uma licitação específica
    # Get specific bid
    """
    # Buscar licitação
    bid = await db.get(Bid, bid_id)
    
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    return bid

@router.put("/{bid_id}", response_model=BidPublic)
async def update_bid(
    *,
    db: AsyncSession = Depends(get_db),
    bid_id: UUID,
    bid_in: BidUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar uma licitação
    # Update a bid
    """
    # Buscar licitação
    bid = await db.get(Bid, bid_id)
    
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Atualizar campos
    bid_data = bid_in.model_dump(exclude_unset=True)
    for field, value in bid_data.items():
        setattr(bid, field, value)
    
    # Salvar alterações
    db.add(bid)
    await db.commit()
    await db.refresh(bid)
    
    return bid

@router.patch("/{bid_id}/status", response_model=BidPublic)
async def update_bid_status(
    *,
    db: AsyncSession = Depends(get_db),
    bid_id: UUID,
    status_update: BidStatusUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar o status de uma licitação (para Kanban)
    # Update bid status (for Kanban)
    """
    # Buscar licitação
    bid = await db.get(Bid, bid_id)
    
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Validar status
    valid_statuses = ['recebidos', 'analisados', 'enviados', 'respondidos', 'ganho', 'perdido']
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Deve ser um dos: {', '.join(valid_statuses)}"
        )
    
    # Atualizar status
    bid.status = status_update.status
    bid.status_changed_at = datetime.now()
    
    # Salvar alterações
    db.add(bid)
    await db.commit()
    await db.refresh(bid)
    
    return bid

@router.delete("/{bid_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bid(
    *,
    db: AsyncSession = Depends(get_db),
    bid_id: UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """
    # Excluir uma licitação
    # Delete a bid
    """
    # Buscar licitação
    bid = await db.get(Bid, bid_id)
    
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Excluir licitação
    await db.delete(bid)
    await db.commit()

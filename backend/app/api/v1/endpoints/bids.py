from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.security import verify_password
from app.crud.base import CRUDBase
from app.models.bid import Bid
from app.models.user import User
from app.schemas.bid import BidCreate, BidPublic, BidSignRequest, BidStatusUpdate, BidUpdate

router = APIRouter()

# Criar instância CRUD para licitações
# Create CRUD instance for bids
crud_bid = CRUDBase(Bid)


@router.get("", response_model=List[BidPublic])
async def read_bids(
    db: AsyncSession = Depends(get_db),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter licitações do usuário atual com possibilidade de filtro por status
    # Get bids of the current user with possible status filtering
    
    Args:
        db: Sessão do banco de dados
        status: Status opcional para filtrar
        skip: Número de registros para pular
        limit: Número máximo de registros para retornar
        current_user: Usuário atual obtido do token
        
    Returns:
        Lista de licitações
    """
    if status:
        # Filtrar por status
        # Filter by status
        stmt = select(Bid).where(
            (Bid.user_id == current_user.user_id) & (Bid.status == status)
        ).offset(skip).limit(limit)
    else:
        # Retornar todas as licitações do usuário
        # Return all bids of the user
        stmt = select(Bid).where(
            Bid.user_id == current_user.user_id
        ).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=BidPublic)
async def create_bid(
    db: AsyncSession = Depends(get_db),
    bid_in: BidCreate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Criar uma nova licitação
    # Create a new bid
    
    Args:
        db: Sessão do banco de dados
        bid_in: Dados da licitação a ser criada
        current_user: Usuário atual obtido do token
        
    Returns:
        A licitação criada
    """
    # Gerar código interno se não fornecido
    # Generate internal code if not provided
    if not bid_in.internal_code:
        # Contar licitações existentes e gerar código no formato ED-XXXX
        # Count existing bids and generate code in format ED-XXXX
        stmt = select(Bid).where(Bid.user_id == current_user.user_id)
        result = await db.execute(stmt)
        count = len(result.scalars().all())
        bid_in.internal_code = f"ED-{count+1:04d}"
    
    # Criar objeto de licitação incluindo o ID do usuário atual
    # Create bid object including the current user ID
    bid_data = bid_in.model_dump()
    bid_data["user_id"] = current_user.user_id
    
    # Criar a licitação
    # Create the bid
    db_bid = Bid(**bid_data)
    db.add(db_bid)
    await db.commit()
    await db.refresh(db_bid)
    return db_bid


@router.get("/{bid_id}", response_model=BidPublic)
async def read_bid(
    bid_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter detalhes de uma licitação específica
    # Get details of a specific bid
    
    Args:
        bid_id: ID da licitação
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Detalhes da licitação solicitada
    """
    bid = await crud_bid.get(db, id=bid_id)
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada",
        )
    
    # Verificar se a licitação pertence ao usuário atual
    # Check if the bid belongs to the current user
    if bid.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a esta licitação",
        )
    
    return bid


@router.patch("/{bid_id}/status", response_model=BidPublic)
async def update_bid_status(
    bid_id: UUID,
    status_update: BidStatusUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar o status de uma licitação
    # Update the status of a bid
    
    Args:
        bid_id: ID da licitação
        status_update: Novo status
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Licitação atualizada
    """
    bid = await crud_bid.get(db, id=bid_id)
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada",
        )
    
    # Verificar se a licitação pertence ao usuário atual
    # Check if the bid belongs to the current user
    if bid.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a esta licitação",
        )
    
    # Verificar se o status é válido
    # Check if the status is valid
    valid_statuses = ["novos", "em_analise", "pronto_para_assinar", "enviado", "ganhos", "perdidos"]
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Deve ser um dos seguintes: {', '.join(valid_statuses)}",
        )
    
    # Atualizar o status
    # Update the status
    bid = await crud_bid.update(db, db_obj=bid, obj_in={"status": status_update.status})
    return bid


@router.put("/{bid_id}", response_model=BidPublic)
async def update_bid(
    bid_id: UUID,
    bid_in: BidUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar detalhes de uma licitação
    # Update details of a bid
    
    Args:
        bid_id: ID da licitação
        bid_in: Dados de atualização da licitação
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Licitação atualizada
    """
    bid = await crud_bid.get(db, id=bid_id)
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada",
        )
    
    # Verificar se a licitação pertence ao usuário atual
    # Check if the bid belongs to the current user
    if bid.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a esta licitação",
        )
    
    # Atualizar a licitação
    # Update the bid
    bid = await crud_bid.update(db, db_obj=bid, obj_in=bid_in)
    return bid


@router.post("/{bid_id}/sign", response_model=BidPublic)
async def sign_bid(
    bid_id: UUID,
    sign_request: BidSignRequest = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Assinar uma licitação (requer confirmação de senha)
    # Sign a bid (requires password confirmation)
    
    Args:
        bid_id: ID da licitação
        sign_request: Solicitação de assinatura com senha
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Licitação assinada e atualizada
    """
    # Verificar a senha do usuário
    # Verify the user's password
    if not verify_password(sign_request.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha incorreta",
        )
    
    bid = await crud_bid.get(db, id=bid_id)
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada",
        )
    
    # Verificar se a licitação pertence ao usuário atual
    # Check if the bid belongs to the current user
    if bid.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a esta licitação",
        )
    
    # Verificar se a licitação está com o status correto para assinatura
    # Check if the bid has the correct status for signing
    if bid.status != "pronto_para_assinar":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta licitação não está pronta para ser assinada",
        )
    
    # Atualizar o status para enviado
    # Update the status to sent
    bid = await crud_bid.update(db, db_obj=bid, obj_in={"status": "enviado"})
    return bid

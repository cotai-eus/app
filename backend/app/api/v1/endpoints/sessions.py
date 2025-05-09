from typing import Any, List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.active_session import ActiveSession
from app.models.user import User
from app.schemas.session import ActiveSessionPublic

router = APIRouter()

@router.get("", response_model=List[ActiveSessionPublic])
async def get_active_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter todas as sessões ativas do usuário
    # Get all active sessions for the user
    """
    query = select(ActiveSession).where(
        ActiveSession.user_id == current_user.user_id,
        ActiveSession.is_revoked == False
    ).order_by(ActiveSession.last_accessed_at.desc())
    
    result = await db.execute(query)
    sessions = result.scalars().all()
    
    return sessions

@router.post("/current", response_model=ActiveSessionPublic)
async def register_current_session(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Registrar a sessão atual do usuário
    # Register current user session
    """
    # Obter informações do cliente
    user_agent = request.headers.get("user-agent", "Unknown Device")
    ip = request.client.host if request.client else "Unknown"
    
    # Criar nova sessão
    session = ActiveSession(
        user_id=current_user.user_id,
        device_info=user_agent,
        ip_address=ip,
        last_accessed_at=datetime.utcnow(),
        is_revoked=False
    )
    
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return session

@router.delete("/{session_id}", status_code=status.HTTP_200_OK, response_model=ActiveSessionPublic)
async def revoke_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Revogar uma sessão específica
    # Revoke a specific session
    """
    # Buscar sessão
    query = select(ActiveSession).where(
        ActiveSession.session_id == session_id,
        ActiveSession.user_id == current_user.user_id
    )
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    
    # Revogar sessão
    session.is_revoked = True
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return session

@router.delete("", status_code=status.HTTP_200_OK)
async def revoke_all_sessions_except_current(
    current_session_id: UUID = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Revogar todas as sessões exceto a atual
    # Revoke all sessions except the current one
    """
    # Verificar se a sessão atual pertence ao usuário
    current_query = select(ActiveSession).where(
        ActiveSession.session_id == current_session_id,
        ActiveSession.user_id == current_user.user_id
    )
    current_result = await db.execute(current_query)
    current_session = current_result.scalar_one_or_none()
    
    if not current_session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sessão atual inválida"
        )
    
    # Buscar e revogar todas as outras sessões
    query = select(ActiveSession).where(
        ActiveSession.user_id == current_user.user_id,
        ActiveSession.session_id != current_session_id,
        ActiveSession.is_revoked == False
    )
    result = await db.execute(query)
    other_sessions = result.scalars().all()
    
    # Revogar cada sessão
    for session in other_sessions:
        session.is_revoked = True
        db.add(session)
    
    await db.commit()
    
    return {"detail": f"Revogadas {len(other_sessions)} sessões"}

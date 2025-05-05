from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.base import CRUDBase
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate, MessagePublic, MessageUpdate

router = APIRouter()

# Criar instância CRUD para mensagens
# Create CRUD instance for messages
crud_message = CRUDBase(Message)


@router.get("", response_model=List[MessagePublic])
async def read_messages(
    db: AsyncSession = Depends(get_db),
    contact_id: Optional[UUID] = Query(None, description="ID do usuário do contato"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter mensagens do usuário atual, opcionalmente filtrando por contato
    # Get messages of the current user, optionally filtering by contact
    
    Args:
        db: Sessão do banco de dados
        contact_id: ID opcional do contato para filtrar mensagens
        skip: Número de registros para pular
        limit: Número máximo de registros para retornar
        current_user: Usuário atual obtido do token
        
    Returns:
        Lista de mensagens
    """
    if contact_id:
        # Filtrar mensagens entre o usuário atual e o contato específico
        # Filter messages between current user and specific contact
        stmt = select(Message).where(
            ((Message.sender_id == current_user.user_id) & (Message.receiver_id == contact_id)) |
            ((Message.sender_id == contact_id) & (Message.receiver_id == current_user.user_id))
        ).order_by(Message.created_at).offset(skip).limit(limit)
    else:
        # Retornar todas as mensagens enviadas ou recebidas pelo usuário atual
        # Return all messages sent or received by current user
        stmt = select(Message).where(
            (Message.sender_id == current_user.user_id) |
            (Message.receiver_id == current_user.user_id)
        ).order_by(Message.created_at).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    messages = result.scalars().all()
    
    # Marcar as mensagens recebidas como lidas
    # Mark received messages as read
    for message in messages:
        if message.receiver_id == current_user.user_id and not message.is_read:
            message.is_read = True
    
    await db.commit()
    return messages


@router.post("", response_model=MessagePublic)
async def create_message(
    db: AsyncSession = Depends(get_db),
    message_in: MessageCreate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Enviar uma nova mensagem
    # Send a new message
    
    Args:
        db: Sessão do banco de dados
        message_in: Dados da mensagem a ser enviada
        current_user: Usuário atual obtido do token
        
    Returns:
        A mensagem enviada
    """
    # Verificar se o destinatário existe
    # Check if recipient exists
    receiver = await crud_user.get(db, id=message_in.receiver_id)
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destinatário não encontrado",
        )
    
    # Criar objeto de mensagem
    # Create message object
    message_data = message_in.model_dump()
    message_data["sender_id"] = current_user.user_id
    
    # Criar a mensagem
    # Create the message
    db_message = Message(**message_data)
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message


@router.patch("/{message_id}/read", response_model=MessagePublic)
async def mark_message_as_read(
    message_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Marcar uma mensagem como lida
    # Mark a message as read
    
    Args:
        message_id: ID da mensagem
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        A mensagem atualizada
    """
    message = await crud_message.get(db, id=message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensagem não encontrada",
        )
    
    # Verificar se o usuário atual é o destinatário da mensagem
    # Check if current user is the message recipient
    if message.receiver_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a esta mensagem",
        )
    
    # Marcar como lida
    # Mark as read
    message_update = MessageUpdate(is_read=True)
    message = await crud_message.update(db, db_obj=message, obj_in=message_update)
    return message


@router.get("/unread-count", response_model=int)
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter contagem de mensagens não lidas
    # Get unread messages count
    
    Args:
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Contagem de mensagens não lidas
    """
    # Contar mensagens não lidas recebidas pelo usuário atual
    # Count unread messages received by current user
    stmt = select(Message).where(
        (Message.receiver_id == current_user.user_id) &
        (Message.is_read == False)  # noqa: E712
    )
    
    result = await db.execute(stmt)
    unread_messages = result.scalars().all()
    
    return len(unread_messages)

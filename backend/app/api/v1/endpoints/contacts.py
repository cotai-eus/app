from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.base import CRUDBase
from app.models.contact import Contact
from app.models.message import Message
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactPublic, ContactUpdate, ContactWithRecentMessage

router = APIRouter()

# Criar instância CRUD para contatos
# Create CRUD instance for contacts
crud_contact = CRUDBase(Contact)


@router.get("", response_model=List[ContactPublic])
async def read_contacts(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter contatos do usuário atual
    # Get contacts of the current user
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros para pular
        limit: Número máximo de registros para retornar
        current_user: Usuário atual obtido do token
        
    Returns:
        Lista de contatos
    """
    # Filtrar contatos pelo ID do usuário atual
    # Filter contacts by current user ID
    stmt = select(Contact).where(
        Contact.user_id == current_user.user_id
    ).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=ContactPublic)
async def create_contact(
    db: AsyncSession = Depends(get_db),
    contact_in: ContactCreate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Criar um novo contato
    # Create a new contact
    
    Args:
        db: Sessão do banco de dados
        contact_in: Dados do contato a ser criado
        current_user: Usuário atual obtido do token
        
    Returns:
        O contato criado
    """
    # Verificar se já existe um contato com o mesmo email (se fornecido)
    # Check if there is already a contact with the same email (if provided)
    if contact_in.email:
        stmt = select(Contact).where(
            (Contact.user_id == current_user.user_id) & (Contact.email == contact_in.email)
        )
        result = await db.execute(stmt)
        existing_contact = result.scalars().first()
        
        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um contato com este email",
            )
    
    # Criar objeto de contato incluindo o ID do usuário atual
    # Create contact object including the current user ID
    contact_data = contact_in.model_dump()
    contact_data["user_id"] = current_user.user_id
    
    # Criar o contato
    # Create the contact
    db_contact = Contact(**contact_data)
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact


@router.get("/with-messages", response_model=List[ContactWithRecentMessage])
async def read_contacts_with_messages(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter contatos com a mensagem mais recente e contagem de não lidas
    # Get contacts with the most recent message and unread count
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros para pular
        limit: Número máximo de registros para retornar
        current_user: Usuário atual obtido do token
        
    Returns:
        Lista de contatos com informações de mensagens
    """
    # Obter todos os contatos do usuário
    # Get all user contacts
    stmt = select(Contact).where(
        Contact.user_id == current_user.user_id
    ).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    contacts = result.scalars().all()
    
    # Para cada contato, buscar a mensagem mais recente e contar não lidas
    # For each contact, find the most recent message and count unread ones
    contact_with_messages = []
    for contact in contacts:
        # Buscar usuário associado ao contato
        # Find user associated with the contact
        user_stmt = select(User).where(User.email == contact.email) if contact.email else None
        contact_user = None
        
        if user_stmt:
            user_result = await db.execute(user_stmt)
            contact_user = user_result.scalars().first()
        
        if not contact_user:
            # Se não encontrou usuário pelo email, pular para o próximo contato
            # If no user found by email, skip to next contact
            continue
        
        # Buscar mensagens entre o usuário atual e o contato
        # Find messages between current user and contact
        message_stmt = select(Message).where(
            ((Message.sender_id == current_user.user_id) & (Message.receiver_id == contact_user.user_id)) |
            ((Message.sender_id == contact_user.user_id) & (Message.receiver_id == current_user.user_id))
        ).order_by(Message.created_at.desc())
        
        message_result = await db.execute(message_stmt)
        messages = message_result.scalars().all()
        
        # Contar mensagens não lidas e obter a mais recente
        # Count unread messages and get the most recent one
        unread_count = 0
        last_message = None
        last_message_time = None
        
        if messages:
            last_message = messages[0].content
            last_message_time = messages[0].created_at
            
            # Contar mensagens não lidas enviadas pelo contato ao usuário atual
            # Count unread messages sent by the contact to current user
            for msg in messages:
                if msg.sender_id == contact_user.user_id and msg.receiver_id == current_user.user_id and not msg.is_read:
                    unread_count += 1
        
        # Adicionar à lista de resultados
        # Add to results list
        contact_data = ContactWithRecentMessage(
            **contact.__dict__,
            last_message=last_message,
            last_message_time=last_message_time,
            unread_count=unread_count
        )
        contact_with_messages.append(contact_data)
    
    return contact_with_messages


@router.get("/{contact_id}", response_model=ContactPublic)
async def read_contact(
    contact_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter detalhes de um contato específico
    # Get details of a specific contact
    
    Args:
        contact_id: ID do contato
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Detalhes do contato solicitado
    """
    contact = await crud_contact.get(db, id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contato não encontrado",
        )
    
    # Verificar se o contato pertence ao usuário atual
    # Check if the contact belongs to the current user
    if contact.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este contato",
        )
    
    return contact


@router.put("/{contact_id}", response_model=ContactPublic)
async def update_contact(
    contact_id: UUID,
    contact_in: ContactUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar detalhes de um contato
    # Update details of a contact
    
    Args:
        contact_id: ID do contato
        contact_in: Dados de atualização do contato
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Contato atualizado
    """
    contact = await crud_contact.get(db, id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contato não encontrado",
        )
    
    # Verificar se o contato pertence ao usuário atual
    # Check if the contact belongs to the current user
    if contact.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este contato",
        )
    
    # Se o email for alterado, verificar se não há duplicação
    # If email is changed, check for duplication
    if contact_in.email and contact_in.email != contact.email:
        stmt = select(Contact).where(
            (Contact.user_id == current_user.user_id) & 
            (Contact.email == contact_in.email) & 
            (Contact.contact_id != contact_id)
        )
        result = await db.execute(stmt)
        existing_contact = result.scalars().first()
        
        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um contato com este email",
            )
    
    # Atualizar o contato
    # Update the contact
    contact = await crud_contact.update(db, db_obj=contact, obj_in=contact_in)
    return contact


@router.delete("/{contact_id}", response_model=ContactPublic)
async def delete_contact(
    contact_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Excluir um contato
    # Delete a contact
    
    Args:
        contact_id: ID do contato
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        O contato excluído
    """
    contact = await crud_contact.get(db, id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contato não encontrado",
        )
    
    # Verificar se o contato pertence ao usuário atual
    # Check if the contact belongs to the current user
    if contact.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este contato",
        )
    
    # Excluir o contato
    # Delete the contact
    contact = await crud_contact.remove(db, id=contact_id)
    return contact

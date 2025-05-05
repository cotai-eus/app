from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from uuid import UUID
import logging

from app import crud, models, schemas
from app.api import deps

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/", response_model=schemas.Message, status_code=status.HTTP_201_CREATED)
async def send_message(
    *,
    db: AsyncSession = Depends(deps.get_db),
    message_in: schemas.MessageCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Envia uma nova mensagem para outro usuário.
    """
    # Comentário em português: Verifica se o destinatário existe.
    receiver = await crud.user.get(db, id=message_in.receiver_id)
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário destinatário não encontrado.")
    if receiver.user_id == current_user.user_id:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível enviar mensagem para si mesmo.")

    # Comentário em português: Cria a mensagem usando o CRUD, definindo o remetente.
    message = await crud.message.create_with_sender(
        db=db, obj_in=message_in, sender_id=current_user.user_id
    )
    log.info(f"Mensagem enviada de {current_user.email} para {receiver.email} (ID: {message.message_id})")
    # Aqui poderia disparar uma notificação (e.g., via WebSockets ou push)
    return message

@router.get("/conversation/{other_user_id}", response_model=List[schemas.Message])
async def get_conversation_with_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    other_user_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém a conversa (mensagens trocadas) entre o usuário autenticado e outro usuário.
    """
    # Comentário em português: Verifica se o outro usuário existe.
    other_user = await crud.user.get(db, id=other_user_id)
    if not other_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    # Comentário em português: Busca a conversa usando o CRUD.
    messages = await crud.message.get_conversation(
        db=db, user1_id=current_user.user_id, user2_id=other_user_id, skip=skip, limit=limit
    )
    # Opcional: Marcar mensagens recebidas como lidas aqui? Ou em endpoint específico?
    # Por simplicidade, vamos assumir que ler a conversa marca como lido.
    # messages_to_mark_read = [m.message_id for m in messages if m.receiver_id == current_user.user_id and not m.is_read]
    # if messages_to_mark_read:
    #     # Implementar um crud.message.mark_list_as_read(db, message_ids=...) seria mais eficiente
    #     for msg_id in messages_to_mark_read:
    #         await crud.message.mark_as_read(db=db, message_id=msg_id)
    #     # Recarregar mensagens? Ou atualizar o status no objeto retornado?
    #     # Para simplificar, retornamos o estado antes da marcação como lida.

    return messages

@router.get("/{message_id}", response_model=schemas.Message)
async def read_message(
    *,
    db: AsyncSession = Depends(deps.get_db),
    message_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém uma mensagem específica pelo ID.
    """
    # Comentário em português: Busca a mensagem pelo ID.
    message = await crud.message.get(db=db, id=message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensagem não encontrada")
    # Comentário em português: Verifica se o usuário logado é o remetente ou o destinatário.
    if message.sender_id != current_user.user_id and message.receiver_id != current_user.user_id:
        log.warning(f"Usuário {current_user.email} tentou acessar mensagem {message_id} não autorizada.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Opcional: Marcar como lida se o current_user for o receiver
    if message.receiver_id == current_user.user_id and not message.is_read:
        message = await crud.message.mark_as_read(db=db, message_id=message_id) or message

    return message

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    *,
    db: AsyncSession = Depends(deps.get_db),
    message_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> None:
    """
    Exclui uma mensagem.
    (Considerar lógica: só o remetente pode excluir? Soft delete?)
    """
    # Comentário em português: Busca a mensagem a ser excluída.
    message = await crud.message.get(db=db, id=message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensagem não encontrada")
    # Comentário em português: Permite que remetente ou destinatário excluam (hard delete neste caso).
    if message.sender_id != current_user.user_id and message.receiver_id != current_user.user_id:
        log.warning(f"Usuário {current_user.email} tentou excluir mensagem {message_id} não autorizada.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Comentário em português: Remove a mensagem usando o CRUD.
    await crud.message.remove(db=db, id=message_id)
    log.info(f"Usuário {current_user.email} excluiu mensagem {message_id}")
    # Retorna 204 No Content


from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.message import MessageCreate # MessageUpdate não é comum aqui

# Mensagens geralmente não são atualizadas, então UpdateSchemaType pode ser omitido ou ser um schema vazio
class CRUDMessage(CRUDBase[Message, MessageCreate, MessageCreate]): # Usando MessageCreate como placeholder para Update
    """ Operações CRUD específicas para o modelo Message. """

    async def get(self, db: AsyncSession, id: UUID) -> Optional[Message]:
        """ Sobrescreve get para usar message_id como chave primária. """
        stmt = select(self.model).where(self.model.message_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_with_sender(
        self, db: AsyncSession, *, obj_in: MessageCreate, sender_id: UUID
    ) -> Message:
        """
        Cria uma nova mensagem com o remetente especificado.

        :param db: Sessão do banco de dados.
        :param obj_in: Schema MessageCreate com os dados da mensagem.
        :param sender_id: ID do usuário remetente.
        :return: Objeto Message criado.
        """
        # Comentário em português: Cria uma mensagem, definindo o sender_id.
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, sender_id=sender_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_conversation(
        self, db: AsyncSession, *, user1_id: UUID, user2_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """
        Obtém as mensagens trocadas entre dois usuários, com paginação.

        :param db: Sessão do banco de dados.
        :param user1_id: ID do primeiro usuário.
        :param user2_id: ID do segundo usuário.
        :param skip: Número de registros a pular.
        :param limit: Número máximo de registros a retornar.
        :return: Lista de objetos Message ordenados por data de criação.
        """
        # Comentário em português: Busca mensagens onde os usuários são remetente/destinatário em qualquer ordem.
        stmt = (
            select(self.model)
            .where(
                or_(
                    (self.model.sender_id == user1_id) & (self.model.receiver_id == user2_id),
                    (self.model.sender_id == user2_id) & (self.model.receiver_id == user1_id),
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(self.model.created_at.desc()) # Mais recentes primeiro
        )
        result = await db.execute(stmt)
        # Retorna em ordem cronológica (mais antigas primeiro) se necessário reverter
        return list(result.scalars().all())[::-1] # Inverte a lista para ordem cronológica

    async def mark_as_read(self, db: AsyncSession, *, message_id: UUID) -> Optional[Message]:
        """ Marca uma mensagem como lida. """
        # Comentário em português: Atualiza o status is_read da mensagem.
        message = await self.get(db, id=message_id)
        if message and not message.is_read:
            message.is_read = True
            db.add(message)
            await db.commit()
            await db.refresh(message)
        return message

    async def remove(self, db: AsyncSession, *, id: UUID) -> Optional[Message]:
         """ Sobrescreve remove para usar message_id. """
         # Comentário em português: A remoção de mensagens pode ter lógicas diferentes
         # (soft delete, remoção apenas para um usuário, etc.). Aqui é hard delete.
         obj = await self.get(db=db, id=id)
         if obj:
             await db.delete(obj)
             await db.commit()
         return obj

# Instância do CRUD para mensagens
message = CRUDMessage(Message)

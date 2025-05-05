from typing import List, Optional
from uuid import UUID
import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.calendar_event import CalendarEvent
from app.schemas.calendar_event import CalendarEventCreate, CalendarEventUpdate

class CRUDCalendarEvent(CRUDBase[CalendarEvent, CalendarEventCreate, CalendarEventUpdate]):
    """ Operações CRUD específicas para o modelo CalendarEvent. """

    async def get(self, db: AsyncSession, id: UUID) -> Optional[CalendarEvent]:
        """ Sobrescreve get para usar event_id como chave primária. """
        stmt = select(self.model).where(self.model.event_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: CalendarEventCreate, user_id: UUID
    ) -> CalendarEvent:
        """
        Cria um novo evento de calendário associado a um usuário específico.

        :param db: Sessão do banco de dados.
        :param obj_in: Schema CalendarEventCreate com os dados do evento.
        :param user_id: ID do usuário proprietário do evento.
        :return: Objeto CalendarEvent criado.
        """
        # Comentário em português: Cria um evento, associando o user_id fornecido.
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner_and_time_range(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        skip: int = 0,
        limit: int = 1000 # Limite maior para eventos
    ) -> List[CalendarEvent]:
        """
        Obtém eventos de um usuário dentro de um intervalo de tempo específico.

        :param db: Sessão do banco de dados.
        :param user_id: ID do usuário proprietário.
        :param start_time: Início do intervalo de tempo.
        :param end_time: Fim do intervalo de tempo.
        :param skip: Número de registros a pular.
        :param limit: Número máximo de registros a retornar.
        :return: Lista de objetos CalendarEvent.
        """
        # Comentário em português: Busca eventos do usuário que se sobrepõem ao intervalo [start_time, end_time].
        # A lógica é: (InícioEvento < FimIntervalo) E (FimEvento > InícioIntervalo)
        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.user_id == user_id,
                    self.model.start_time < end_time,
                    self.model.end_time > start_time
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(self.model.start_time) # Ordena por início do evento
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def remove(self, db: AsyncSession, *, id: UUID) -> Optional[CalendarEvent]:
         """ Sobrescreve remove para usar event_id. """
         obj = await self.get(db=db, id=id)
         if obj:
             await db.delete(obj)
             await db.commit()
         return obj

# Instância do CRUD para eventos de calendário
calendar_event = CRUDCalendarEvent(CalendarEvent)

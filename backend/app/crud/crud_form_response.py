from typing import List, Optional, Dict, Any
from uuid import UUID
import datetime
from sqlalchemy import select, update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.form_response import FormResponse
from app.schemas.form_response import FormResponseCreate, FormResponseUpdate

class CRUDFormResponse(CRUDBase[FormResponse, FormResponseCreate, FormResponseUpdate]):
    """ Operações CRUD específicas para o modelo FormResponse. """

    async def get(self, db: AsyncSession, id: UUID) -> Optional[FormResponse]:
        """ Sobrescreve get para usar response_id como chave primária. """
        stmt = select(self.model).where(self.model.response_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_with_form_and_user(
        self, db: AsyncSession, *, obj_in: FormResponseCreate # user_id e form_id já estão em obj_in
    ) -> FormResponse:
        """
        Cria uma nova resposta de formulário. Os IDs de usuário e formulário
        são fornecidos diretamente no schema de criação.

        :param db: Sessão do banco de dados.
        :param obj_in: Schema FormResponseCreate com os dados da resposta.
        :return: Objeto FormResponse criado.
        """
        # Comentário em português: Cria a resposta usando os dados do schema.
        # Assume-se que a validação (e.g., se o form_id e user_id existem)
        # é feita antes ou tratada por constraints do DB.
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_form(
        self, db: AsyncSession, *, form_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[FormResponse]:
        """ Obtém múltiplas respostas para um formulário específico. """
        # Comentário em português: Busca respostas associadas a um form_id.
        stmt = (
            select(self.model)
            .where(self.model.form_id == form_id)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.submitted_at.desc()) # Mais recentes primeiro
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_multi_by_user(
        self, db: AsyncSession, *, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[FormResponse]:
        """ Obtém múltiplas respostas submetidas por um usuário específico. """
        # Comentário em português: Busca respostas associadas a um user_id.
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.submitted_at.desc()) # Mais recentes primeiro
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def update_status(
        self, db: AsyncSession, *, response_id: UUID, status: str, processed_at: Optional[datetime.datetime] = None
    ) -> Optional[FormResponse]:
        """
        Atualiza o status e opcionalmente a data de processamento de uma resposta.
        Usa a API Core para eficiência.

        :param db: Sessão do banco de dados.
        :param response_id: ID da resposta a ser atualizada.
        :param status: Novo status.
        :param processed_at: Data/hora de processamento (opcional).
        :return: O objeto FormResponse atualizado ou None se não encontrado.
        """
        # Comentário em português: Atualiza o status e processed_at usando update direto.
        values_to_update: Dict[str, Any] = {"status": status}
        if processed_at is not None:
            values_to_update["processed_at"] = processed_at

        stmt = (
            sqlalchemy_update(self.model)
            .where(self.model.response_id == response_id)
            .values(**values_to_update)
            .execution_options(synchronize_session=False) # Não precisa sincronizar para esta operação simples
            .returning(self.model) # Retorna o objeto atualizado (requer suporte do dialeto, como PostgreSQL)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none() # Retorna o objeto atualizado ou None

    async def remove(self, db: AsyncSession, *, id: UUID) -> Optional[FormResponse]:
         """ Sobrescreve remove para usar response_id. """
         obj = await self.get(db=db, id=id)
         if obj:
             await db.delete(obj)
             await db.commit()
         return obj

# Instância do CRUD para respostas de formulário
form_response = CRUDFormResponse(FormResponse)

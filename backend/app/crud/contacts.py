from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.expression import func

from app.crud.base import CRUDBase
from app.models.contacts import Contact
from app.schemas.contacts import ContactCreate, ContactUpdate

class CRUDContact(CRUDBase[Contact, ContactCreate, ContactUpdate]):
    """
    Operações CRUD para Contatos.
    """

    async def get_multi_by_user(
        self, db: AsyncSession, *, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        """
        Obtém múltiplos contatos para um usuário específico.

        Args:
            db: Sessão de banco de dados.
            user_id: ID do usuário.
            skip: Número de registros a pular.
            limit: Número máximo de registros a retornar.

        Returns:
            Lista de contatos.
        """
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.created_at.desc()) # Exemplo de ordenação
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create_with_user(
        self, db: AsyncSession, *, obj_in: ContactCreate, user_id: UUID
    ) -> Contact:
        """
        Cria um novo contato associado a um usuário.

        Args:
            db: Sessão de banco de dados.
            obj_in: Dados para criar o contato.
            user_id: ID do usuário proprietário.

        Returns:
            O contato criado.
        """
        # Converte o schema Pydantic para um dicionário
        obj_in_data = obj_in.model_dump()
        # Cria a instância do modelo SQLAlchemy
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

# Instância do CRUD para ser usada nos endpoints da API
contact = CRUDContact(Contact)
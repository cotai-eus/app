from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

class CRUDContact(CRUDBase[Contact, ContactCreate, ContactUpdate]):
    """ Operações CRUD específicas para o modelo Contact. """

    async def get(self, db: AsyncSession, id: UUID) -> Optional[Contact]:
        """ Sobrescreve get para usar contact_id como chave primária. """
        stmt = select(self.model).where(self.model.contact_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: ContactCreate, user_id: UUID
    ) -> Contact:
        """
        Cria um novo contato associado a um usuário específico.

        :param db: Sessão do banco de dados.
        :param obj_in: Schema ContactCreate com os dados do contato.
        :param user_id: ID do usuário proprietário do contato.
        :return: Objeto Contact criado.
        """
        # Comentário em português: Cria um contato, associando o user_id fornecido.
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        """
        Obtém múltiplos contatos pertencentes a um usuário específico, com paginação.

        :param db: Sessão do banco de dados.
        :param user_id: ID do usuário proprietário.
        :param skip: Número de registros a pular.
        :param limit: Número máximo de registros a retornar.
        :return: Lista de objetos Contact.
        """
        # Comentário em português: Busca contatos pertencentes a um usuário específico.
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.last_name, self.model.first_name) # Ordena por nome
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def remove(self, db: AsyncSession, *, id: UUID) -> Optional[Contact]:
         """ Sobrescreve remove para usar contact_id. """
         obj = await self.get(db=db, id=id)
         if obj:
             await db.delete(obj)
             await db.commit()
         return obj

# Instância do CRUD para contatos
contact = CRUDContact(Contact)

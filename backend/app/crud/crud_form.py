from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.form import Form
from app.schemas.form import FormCreate, FormUpdate

class CRUDForm(CRUDBase[Form, FormCreate, FormUpdate]):
    """ Operações CRUD específicas para o modelo Form (templates de formulário). """

    async def get(self, db: AsyncSession, id: UUID) -> Optional[Form]:
        """ Sobrescreve get para usar form_id como chave primária. """
        stmt = select(self.model).where(self.model.form_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    # Se formulários fossem por usuário, adicionaríamos métodos como create_with_owner e get_multi_by_owner.
    # Como são globais (baseado no schema SQL), o get_multi padrão é suficiente.

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Form]:
        """ Sobrescreve get_multi para ordenar por título. """
        stmt = select(self.model).offset(skip).limit(limit).order_by(self.model.title)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def remove(self, db: AsyncSession, *, id: UUID) -> Optional[Form]:
         """ Sobrescreve remove para usar form_id. """
         obj = await self.get(db=db, id=id)
         if obj:
             # Comentário em português: Remover um form template também remove todas as respostas associadas (devido ao ON DELETE CASCADE).
             await db.delete(obj)
             await db.commit()
         return obj

# Instância do CRUD para formulários (templates)
form = CRUDForm(Form)

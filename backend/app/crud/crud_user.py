from typing import Any, Dict, Optional, Union, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Operações CRUD específicas para o modelo User.
    """

    async def get(self, db: AsyncSession, id: UUID) -> Optional[User]:
        """ Sobrescreve get para usar user_id como chave primária. """
        stmt = select(self.model).where(self.model.user_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """
        Busca um usuário pelo endereço de e-mail (case-insensitive devido ao CITEXT).

        :param db: Sessão do banco de dados.
        :param email: E-mail a ser buscado.
        :return: Objeto User ou None.
        """
        # Comentário em português: Busca usuário pelo email.
        stmt = select(self.model).where(self.model.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        """
        Busca um usuário pelo nome de usuário (case-insensitive devido ao CITEXT).

        :param db: Sessão do banco de dados.
        :param username: Nome de usuário a ser buscado.
        :return: Objeto User ou None.
        """
        # Comentário em português: Busca usuário pelo username.
        stmt = select(self.model).where(self.model.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        Cria um novo usuário, hasheando a senha antes de salvar.

        :param db: Sessão do banco de dados.
        :param obj_in: Schema UserCreate com os dados do novo usuário.
        :return: Objeto User criado.
        """
        # Comentário em português: Cria um usuário, garantindo que a senha seja hasheada.
        create_data = obj_in.model_dump()
        create_data["password_hash"] = get_password_hash(obj_in.password)
        del create_data["password"] # Remove a senha em texto plano
        db_obj = self.model(**create_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Atualiza um usuário. Se uma nova senha for fornecida, ela será hasheada.

        :param db: Sessão do banco de dados.
        :param db_obj: Objeto User a ser atualizado.
        :param obj_in: Schema UserUpdate ou dict com os dados de atualização.
        :return: Objeto User atualizado.
        """
        # Comentário em português: Atualiza o usuário. Hashea a nova senha se fornecida.
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            # Comentário em português: Hashea a nova senha e remove a senha em texto plano.
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password_hash"] = hashed_password

        # Comentário em português: Chama o método update da classe base com os dados preparados.
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(
        self, db: AsyncSession, *, username_or_email: str, password: str
    ) -> Optional[User]:
        """
        Autentica um usuário pela combinação de username/email e senha.

        :param db: Sessão do banco de dados.
        :param username_or_email: Username ou E-mail do usuário.
        :param password: Senha em texto plano.
        :return: Objeto User se a autenticação for bem-sucedida, senão None.
        """
        # Comentário em português: Tenta buscar o usuário pelo email ou username.
        user = await self.get_by_email(db, email=username_or_email)
        if not user:
            user = await self.get_by_username(db, username=username_or_email)

        # Comentário em português: Verifica se o usuário existe e se a senha está correta.
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        """ Verifica se o usuário está ativo. """
        return user.is_active

    async def is_admin(self, user: User) -> bool:
        """ Verifica se o usuário é administrador. """
        return user.is_admin

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """ Sobrescreve get_multi para ordenar por username por padrão. """
        stmt = select(self.model).offset(skip).limit(limit).order_by(self.model.username)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def remove(self, db: AsyncSession, *, id: UUID) -> Optional[User]:
         """ Sobrescreve remove para usar user_id. """
         obj = await self.get(db=db, id=id)
         if obj:
             await db.delete(obj)
             await db.commit()
         return obj

# Instância do CRUD para usuários
user = CRUDUser(User)


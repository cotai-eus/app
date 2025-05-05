from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, update, func
from sqlalchemy.dialects.postgresql import insert
import structlog

from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

logger = structlog.get_logger()

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Operações CRUD para usuários.
    """
    
    async def get_by_username_or_email(self, db: AsyncSession, username_or_email: str) -> Optional[User]:
        """
        Obtém um usuário pelo nome de usuário ou email.
        
        Args:
            db: Sessão de banco de dados
            username_or_email: Nome de usuário ou email do usuário
            
        Returns:
            O usuário encontrado ou None
        """
        stmt = select(User).where(
            or_(User.username == username_or_email, User.email == username_or_email)
        )
        result = await db.execute(stmt)
        return result.scalars().first()
    
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        Cria um novo usuário.
        
        Args:
            db: Sessão de banco de dados
            obj_in: Dados para criar o usuário
            
        Returns:
            O usuário criado
        """
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            avatar_url=obj_in.avatar_url,
            is_active=obj_in.is_active if obj_in.is_active is not None else True,
            is_admin=obj_in.is_admin if obj_in.is_admin is not None else False,
        )
        db.add(db_obj)
        try:
            await db.flush()
        except Exception as e:
            await db.rollback()
            logger.error("Erro ao criar usuário", error=str(e), username=obj_in.username, email=obj_in.email)
            raise ValueError(f"Não foi possível criar usuário: {e}")
            
        await db.refresh(db_obj)
        
        logger.info(
            "Usuario criado",
            user_id=str(db_obj.user_id),
            username=db_obj.username,
        )
        
        return db_obj
    
    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Atualiza um usuário.
        
        Args:
            db: Sessão de banco de dados
            db_obj: Usuário a ser atualizado
            obj_in: Dados para atualizar o usuário
            
        Returns:
            O usuário atualizado
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password_hash"] = hashed_password
            del update_data["password"]
        elif "password" in update_data:
            del update_data["password"]
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        
        logger.info(
            "Usuario atualizado",
            user_id=str(db_obj.user_id),
            updated_fields=list(update_data.keys())
        )
        
        return db_obj
        
    async def authenticate(
        self, db: AsyncSession, *, username_or_email: str, password: str
    ) -> Optional[User]:
        """
        Autentica um usuário.
        
        Args:
            db: Sessão de banco de dados
            username_or_email: Nome de usuário ou email
            password: Senha em texto plano
            
        Returns:
            O usuário autenticado ou None
        """
        user = await self.get_by_username_or_email(db, username_or_email=username_or_email)
        if not user:
            logger.warning("Falha na autenticação: Usuário não encontrado", identifier=username_or_email)
            return None
        if not user.is_active:
            logger.warning("Falha na autenticação: Usuário inativo", user_id=str(user.user_id))
            return None
        if not verify_password(password, user.password_hash):
            logger.warning("Falha na autenticação: Senha inválida", user_id=str(user.user_id))
            return None
            
        stmt = (
            update(User)
            .where(User.user_id == user.user_id)
            .values(last_login=func.timezone('utc', func.now()))
        )
        await db.execute(stmt)
        
        logger.info("Usuário autenticado com sucesso", user_id=str(user.user_id))
        return user
        
    def is_active(self, user: User) -> bool:
        """Verifica se um usuário está ativo."""
        return user.is_active
        
    def is_admin(self, user: User) -> bool:
        """Verifica se um usuário é administrador."""
        return user.is_admin

user = CRUDUser(User)
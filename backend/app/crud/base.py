from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    # Classe CRUD base com métodos padrão para operações de banco de dados
    # Base CRUD class with standard methods for database operations
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        # Inicializa a classe CRUD com o modelo SQLAlchemy
        # Initialize the CRUD class with SQLAlchemy model
        
        Args:
            model: Uma classe modelo SQLAlchemy
        """
        self.model = model
    
    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        # Obtém um registro pelo ID
        # Get a record by ID
        
        Args:
            db: Sessão de banco de dados
            id: ID do registro
            
        Returns:
            O registro encontrado ou None
        """
        stmt = select(self.model).where(getattr(self.model, self.model.__table__.primary_key.columns.keys()[0]) == id)
        result = await db.execute(stmt)
        return result.scalars().first()
    
    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        # Obtém vários registros com paginação
        # Get multiple records with pagination
        
        Args:
            db: Sessão de banco de dados
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            Lista de registros
        """
        stmt = select(self.model).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        # Cria um novo registro
        # Create a new record
        
        Args:
            db: Sessão de banco de dados
            obj_in: Dados do objeto a ser criado
            
        Returns:
            O registro criado
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        # Atualiza um registro
        # Update a record
        
        Args:
            db: Sessão de banco de dados
            db_obj: Objeto no banco de dados a ser atualizado
            obj_in: Dados de atualização
            
        Returns:
            O registro atualizado
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def remove(self, db: AsyncSession, *, id: Any) -> ModelType:
        """
        # Remove um registro
        # Remove a record
        
        Args:
            db: Sessão de banco de dados
            id: ID do registro
            
        Returns:
            O registro removido
        """
        stmt = select(self.model).where(getattr(self.model, self.model.__table__.primary_key.columns.keys()[0]) == id)
        result = await db.execute(stmt)
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj
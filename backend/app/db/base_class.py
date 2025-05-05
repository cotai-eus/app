from typing import Any
import uuid

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import DateTime, UUID, MetaData
from datetime import datetime

# Convenção de nomenclatura para constraints e índices do SQLAlchemy
# Ajuda a manter nomes consistentes e evita conflitos, especialmente com Alembic.
# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Metadados com a convenção de nomenclatura definida
metadata = MetaData(naming_convention=convention)

class Base(AsyncAttrs, DeclarativeBase):
    """
    Classe base para todos os modelos SQLAlchemy.
    
    Define comportamentos comuns como:
    - Nomes de tabela automáticos
    - IDs UUID para todos os modelos
    - Timestamps de criação e atualização
    """
    metadata = metadata

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Gera nome de tabela automático a partir do nome da classe
        return cls.__name__.lower()
    
    # Usar UUID como chave primária para todos os modelos
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    # Timestamps automáticos
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
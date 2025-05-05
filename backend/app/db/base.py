# Este arquivo serve como um ponto central para importar a Base e todos os modelos.
# Isso é crucial para que o Alembic possa detectar automaticamente as definições dos modelos.

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

# Convenção para nomes de indices e restrições para compatibilidade com Alembic
# Naming convention for indexes and constraints for Alembic compatibility
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(AsyncAttrs, DeclarativeBase):
    """
    # Classe base para todos os modelos SQLAlchemy com suporte assíncrono
    Base class for all SQLAlchemy models with async support
    """

    metadata = metadata

    # Adicione colunas padrão created_at e updated_at para todos os modelos
    # Add default created_at and updated_at columns to all models
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Gere automaticamente o nome da tabela a partir do nome da classe em minúsculas
    # Generate table name automatically from lowercase class name
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

from app.models.user import User
from app.models.contact import Contact
from app.models.message import Message
from app.models.calendar_event import CalendarEvent
from app.models.form import Form
from app.models.form_response import FormResponse
from app.models.user_photo import UserPhoto

# Você pode adicionar mais importações de modelos aqui conforme necessário
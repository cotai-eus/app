import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings
from app.db.base import Base

# Aqui importamos todos os modelos para que o Alembic possa detectá-los
# Here we import all models so Alembic can detect them
from app.models import (  # noqa: F401
    active_session, api_key, bid, calendar_event, contact, document, message, user
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Substitui a URL de conexão com a do .env
# Replace the connection URL with the one from .env
db_url = str(settings.DATABASE_URL)
if hasattr(settings, 'DATABASE_DRIVER') and settings.DATABASE_DRIVER:
    db_url = db_url.replace("postgresql://", f"postgresql+{settings.DATABASE_DRIVER}://")
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    """
    # Executa migrações em modo 'offline'.
    # Isso não requer nenhuma conexão com o banco de dados, apenas acesso ao arquivo de config.
    
    # Run migrations in 'offline' mode.
    # This does not require any connection to the database, just access to the config file.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """
    # Executa as migrações no contexto fornecido
    # Run migrations in the given context
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine and associate a
    connection with the context.
    """
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    # Run migrations in an async context
    asyncio.run(run_async_migrations(connectable))


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


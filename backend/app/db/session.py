from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# Garanta que a URL usada aqui tenha o prefixo correto
db_url_str = str(settings.DATABASE_URL)
if db_url_str.startswith("postgresql://"):
    # Substitui o driver padrão pelo assíncrono psycopg
    async_db_url = db_url_str.replace("postgresql://", "postgresql+psycopg://", 1)
elif not db_url_str.startswith("postgresql+psycopg://"):
    # Adicione mais lógica se outros formatos como psycopg forem possíveis
    raise ValueError(f"Formato de DATABASE_URL inesperado: {db_url_str}. Use 'postgresql+psycopg://'.")
else:
    async_db_url = db_url_str

# Use a URL corrigida
engine = create_async_engine(async_db_url, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Adicione este alias para compatibilidade com código existente
async_session_maker = AsyncSessionLocal

# Create a synchronous SessionLocal if needed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
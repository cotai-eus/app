import asyncio
import os
from typing import AsyncGenerator, Generator, Dict
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# --- Importações da Aplicação ---
try:
    from app.main import app as application
    from app.core.config import settings
    from app.db.base import Base
    from app.db.session import get_db
    from app.schemas.user import UserCreate
    from app.crud.crud_user import user as crud_user
    from app.models.user import User
    from app.core.security import create_access_token, get_password_hash
except ImportError as e:
    print(f"Erro ao importar módulos da aplicação em conftest.py: {e}")
    print("Verifique se os erros de importação internos da aplicação foram corrigidos.")
    raise e

# --- Configuração do Banco de Dados de Teste ---

# Test database URL - ensure this is different from your main database
TEST_DATABASE_URL = settings.TEST_DATABASE_URL or "postgresql+psycopg://postgres:postgres@db:5432/test_db"

# Create async engine for tests
engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# --- Fixtures ---

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Cria um event loop para a sessão de testes."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Fixture for getting the application
@pytest.fixture
def app() -> FastAPI:
    return application

# Database session fixture
@pytest.fixture
async def db() -> AsyncSession:
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
        # Clean up after test
        await session.rollback()

# Override the get_db dependency
@pytest.fixture
async def override_get_db(db: AsyncSession) -> Generator:
    # Override the get_db dependency to use the test database
    async def _override_get_db():
        try:
            yield db
        finally:
            await db.close()
    
    application.dependency_overrides[get_db] = _override_get_db
    yield
    del application.dependency_overrides[get_db]

# Test client
@pytest.fixture
async def client(app: FastAPI, override_get_db) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://test"
    ) as client:
        yield client

# --- Fixtures de Usuário e Autenticação ---

# Create a test user
@pytest.fixture
async def test_user(db: AsyncSession, override_get_db) -> User:
    # Create a user for testing
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123"),
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Create authentication headers for testing
@pytest.fixture
async def auth_headers(test_user: User) -> Dict[str, str]:
    access_token = create_access_token(
        data={"sub": test_user.username}
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest_asyncio.fixture(scope="function")
async def user_token_headers(client: AsyncClient, test_user: User) -> dict[str, str]:
    """Gera cabeçalhos de autenticação para o usuário de teste."""
    login_data = {"username": test_user.username, "password": "testpassword123"}
    response = await client.post(f"{settings.API_V1_STR}/auth/login", json=login_data)
    response.raise_for_status()
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture(scope="function")
async def superuser_token_headers(client: AsyncClient, superuser: User) -> dict[str, str]:
    """Gera cabeçalhos de autenticação para o superusuário de teste."""
    login_data = {"username": superuser.username, "password": settings.FIRST_SUPERUSER_PASSWORD}
    response = await client.post(f"{settings.API_V1_STR}/auth/login", json=login_data)
    response.raise_for_status()
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

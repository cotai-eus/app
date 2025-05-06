import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# --- Importações da Aplicação ---
try:
    from app.main import app
    from app.core.config import settings
    from app.db.base import Base
    from app.db.session import get_db
    from app.schemas.user import UserCreate
    from app.crud.crud_user import user as crud_user
    from app.models.user import User
except ImportError as e:
    print(f"Erro ao importar módulos da aplicação em conftest.py: {e}")
    print("Verifique se os erros de importação internos da aplicação foram corrigidos.")
    raise e

# --- Configuração do Banco de Dados de Teste ---

# Use psycopg (v3) driver explicitly for async connections
DB_DRIVER = "postgresql+psycopg"
DEFAULT_TEST_DB_URL = f"{DB_DRIVER}://postgres:postgres@db:5432/test_db"

def get_test_database_url() -> str:
    """Constructs the test database URL using the psycopg driver."""
    env_url = os.getenv("TEST_DATABASE_URL")
    if env_url:
        # Ensure the environment variable URL uses the correct driver if it's a postgres URL
        if env_url.startswith("postgresql://"):
            return env_url.replace("postgresql://", f"{DB_DRIVER}://", 1)
        elif env_url.startswith("postgresql+psycopg://"):
             return env_url.replace("postgresql+psycopg://", f"{DB_DRIVER}://", 1)
        return env_url # Assume it's correctly formatted if not standard postgres

    if settings.DATABASE_URL:
        # Convert PostgresDsn to string and ensure it uses the psycopg driver
        db_url_str = str(settings.DATABASE_URL)
        if db_url_str.startswith("postgresql://"):
             base_url = db_url_str.replace("postgresql://", f"{DB_DRIVER}://", 1)
        elif db_url_str.startswith("postgresql+psycopg://"):
             base_url = db_url_str.replace("postgresql+psycopg://", f"{DB_DRIVER}://", 1)
        elif db_url_str.startswith(f"{DB_DRIVER}://"):
             base_url = db_url_str
        else:
             # Fallback if the format is unexpected, might need adjustment
             print(f"Warning: Unexpected DATABASE_URL format in settings: {db_url_str}. Using default test DB URL.")
             return DEFAULT_TEST_DB_URL

        # Replace the database name for the test database
        # This assumes the database name is the last part after the final '/'
        parts = base_url.split('/')
        if len(parts) > 3 and settings.DATABASE_NAME: # Check if DB name likely exists in URL
            parts[-1] = f"{settings.DATABASE_NAME}_test"
            return "/".join(parts)
        else:
             # If DB name replacement is tricky, fallback or adjust logic
             print(f"Warning: Could not reliably replace database name in {base_url}. Using default test DB URL.")
             return DEFAULT_TEST_DB_URL
    else:
        return DEFAULT_TEST_DB_URL

TEST_DATABASE_URL = get_test_database_url()
print(f"Using test database URL: {TEST_DATABASE_URL}") # For debugging

# Create the async engine with the explicitly defined test URL
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

# --- Fixtures ---

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Cria um event loop para a sessão de testes."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database() -> AsyncGenerator[None, None]:
    """Cria e limpa as tabelas do banco de dados de teste."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def db_session(prepare_database: None) -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão de banco de dados transacional para cada teste."""
    async with TestingSessionLocal() as session:
        yield session
        # Rollback is handled by session context manager

@pytest_asyncio.fixture(scope="function", autouse=True)
def override_get_db(db_session: AsyncSession) -> Generator[None, None, None]:
    """Sobrescreve a dependência get_db para usar a sessão de teste."""
    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest_asyncio.fixture(scope="function")
async def client(override_get_db: None) -> AsyncGenerator[AsyncClient, None]:
    """Fornece um cliente HTTP assíncrono para interagir com a API."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# --- Fixtures de Usuário e Autenticação ---

@pytest_asyncio.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """Cria um usuário de teste padrão."""
    email = "testuser@example.com"
    password = "testpassword123"
    username = "testuser"
    first_name="Test"
    last_name="User"

    user = await crud_user.get_by_username(db=db_session, username=username)
    if not user:
        user_in = UserCreate(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user = await crud_user.create(db=db_session, obj_in=user_in)
    return user

@pytest_asyncio.fixture(scope="function")
async def superuser(db_session: AsyncSession) -> User:
    """Cria um superusuário de teste."""
    email = settings.FIRST_SUPERUSER_EMAIL
    password = settings.FIRST_SUPERUSER_PASSWORD
    username = "admin_test"
    first_name="Admin"
    last_name="Test"

    user = await crud_user.get_by_username(db=db_session, username=username)
    if not user:
        user_in = UserCreate(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_superuser=True # Set directly on creation if possible/desired
        )
        user = await crud_user.create(db=db_session, obj_in=user_in)
        # Ensure is_superuser is set if not done during creation or if user existed
        if not user.is_superuser:
             user = await crud_user.update(db=db_session, db_obj=user, obj_in={"is_superuser": True})
    elif not user.is_superuser:
         user = await crud_user.update(db=db_session, db_obj=user, obj_in={"is_superuser": True})

    return user


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

# ... (restante das fixtures, se houver) ...

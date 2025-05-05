import os
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Check if we're running in Docker environment or locally
IN_DOCKER = os.environ.get('DOCKER_ENV', '').lower() == 'true'

# Use the appropriate database URL based on environment
if IN_DOCKER:
    # When running in Docker, use the Docker service name
    DATABASE_URL = os.environ.get('DATABASE_URL', "postgresql+psycopg://postgres:postgres@db:5432/test_db")
else:
    # When running locally (outside Docker), use localhost
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL', "postgresql+psycopg://postgres:postgres@localhost:5432/test_db")

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_engine():
    # Create engine with the appropriate URL
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()

@pytest.fixture
async def prepare_database(test_engine):
    # Create tables
    from app.models.base import Base  # Adjust this import to your actual Base model location
    
    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        yield test_engine
        
        # Clean up after tests
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    except Exception as e:
        print(f"Database setup failed: {e}")
        # Fallback to in-memory SQLite if PostgreSQL connection fails
        memory_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
        async with memory_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield memory_engine
        await memory_engine.dispose()

@pytest.fixture
async def db_session(prepare_database):
    engine = prepare_database
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()

from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    # Configurações da aplicação carregadas a partir das variáveis de ambiente
    # ou do arquivo .env
    Application settings loaded from environment variables or .env file
    """
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Licitação Hub API"

    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias/days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "https://localhost:5173"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str = "test_db"  # Example
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    DATABASE_DRIVER: str = "psycopg_async"

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
            
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=info.data.get("DATABASE_USER", ""),
            password=info.data.get("DATABASE_PASSWORD", ""),
            host=info.data.get("DATABASE_HOST", ""),
            port=info.data.get("DATABASE_PORT", "5432"),
            path=f"/{info.data.get('DATABASE_NAME', 'app')}",
        )

    @property
    def database_url_with_driver(self) -> str:
        """Returns the database URL with the appropriate driver."""
        url = str(self.DATABASE_URL)
        if url.startswith("postgresql://") and self.DATABASE_DRIVER:
            return url.replace("postgresql://", f"postgresql+{self.DATABASE_DRIVER}://")
        return url

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: Optional[str] = None

    @field_validator("REDIS_URL", mode="before")
    def assemble_redis_connection(cls, v: Optional[str], info: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
            
        return f"redis://{info.data.get('REDIS_HOST', 'redis')}:{info.data.get('REDIS_PORT', 6379)}/0"

    # LLM Service
    LLM_PROVIDER: str = "openai"  # openai, gemini, etc.
    LLM_API_KEY: str
    LLM_MODEL: str = "gpt-4o"
    
    # Initial Admin User
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    
    # File Storage
    UPLOAD_DIRECTORY: str = "/app/uploads"


settings = Settings()

# Certifique-se de que a string final usada em session.py tenha o driver correto.
# Se PostgresDsn estiver removendo o driver, pode ser necessário ajustar
# como a URL é passada para create_async_engine em session.py,
# por exemplo, construindo a string manualmente lá se necessário.
# Exemplo de ajuste potencial em session.py se PostgresDsn causar problemas:
# ASYNC_DATABASE_URL = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+psycopg://", 1)
# engine = create_async_engine(ASYNC_DATABASE_URL, pool_pre_ping=True)
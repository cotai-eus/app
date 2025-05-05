import logging
import sys
import structlog
import time
import uuid
import os
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.redis.client import close_redis_connection, get_redis_client
import app.db.base  # noqa: F401
import app.tasks  # noqa: F401

# --- Configuração de Logging Estruturado com Structlog ---
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger(__name__)

# Middleware para logging de requisições
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar requisições HTTP
    """
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Adicionar request_id ao contexto do logger
        request_logger = logger.bind(request_id=request_id)
        
        request_logger.info(
            "Requisição iniciada",
            path=request.url.path,
            method=request.method,
        )
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        request_logger.info(
            "Requisição finalizada",
            status_code=response.status_code,
            duration=f"{process_time:.4f}s",
        )
        
        return response

# Criar diretório de upload se não existir
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

# --- Ciclo de Vida da Aplicação (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de contexto para o ciclo de vida da aplicação FastAPI.
    Executa código na inicialização e no desligamento.
    """
    logger.info("Iniciando aplicação...", project=settings.PROJECT_NAME)
    try:
        await get_redis_client()
        logger.info("Conexão Redis inicializada")
    except Exception as e:
        logger.error(f"Falha ao conectar ao Redis: {e}")
    yield
    logger.info("Desligando aplicação...")
    await close_redis_connection()
    await engine.dispose()
    logger.info("Conexões com banco de dados fechadas.")

# --- Criação da Instância FastAPI ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# --- Middlewares ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)

# --- Roteadores da API ---
app.include_router(api_router, prefix=settings.API_V1_STR)

# --- Rota Raiz (Health Check) ---
@app.get("/", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def root():
    """
    Endpoint raiz para verificação de saúde básica.
    """
    return {
        "message": "Bem-vindo à API Licitação Hub",
        "status": "online",
        "version": "1.0.0",
        "documentation": "/docs",
    }

# --- Manipuladores de Exceção Personalizados ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """ Manipulador para exceções HTTP padrão do FastAPI. """
    logger.warning(
        "HTTP Exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=getattr(exc, "headers", None),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """ Manipulador para erros de validação do Pydantic. """
    logger.warning(
        "Request Validation Error",
        errors=exc.errors(),
        path=request.url.path,
        method=request.method,
    )
    error_details = []
    for error in exc.errors():
        field = " -> ".join(map(str, error["loc"]))
        message = error["msg"]
        error_details.append({"field": field, "message": message})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Erro de validação na requisição", "errors": error_details},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """ Manipulador para exceções genéricas não tratadas. """
    logger.exception(
        "Unhandled Exception",
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocorreu um erro interno no servidor."},
    )

# --- Ponto de Entrada (para execução local com uvicorn) ---
def start():
    """
    Função para iniciar a aplicação via CLI
    """
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

if __name__ == "__main__":
    start()
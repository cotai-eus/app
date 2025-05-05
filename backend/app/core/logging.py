import logging
import sys
from typing import Any, Dict, Optional

import structlog
from structlog.types import EventDict, Processor

from app.core.config import settings

def add_app_context(
    logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Adiciona contexto da aplicação ao log.
    
    Args:
        logger: Logger do sistema
        method_name: Nome do método que gerou o log
        event_dict: Dicionário de eventos do log
        
    Returns:
        Dicionário de eventos atualizado
    """
    event_dict["environment"] = settings.ENVIRONMENT
    return event_dict

def configure_logging() -> None:
    """
    Configura o sistema de logging estruturado para a aplicação.
    """
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        add_app_context,
    ]

    if settings.ENVIRONMENT == "dev":
        # Console formatado colorido para ambiente de desenvolvimento
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer()
        ]
    else:
        # JSON para ambientes de produção e staging (facilita integração com ELK, etc.)
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configurar logger raiz para capturar logs de bibliotecas
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.handlers = [handler]
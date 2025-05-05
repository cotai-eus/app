import json
from typing import Any, Dict, List, Optional, Union

import redis.asyncio as redis
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Conexão de cliente Redis assíncrona
# Asynchronous Redis client connection
redis_client: Optional[redis.Redis] = None


async def get_redis_client() -> redis.Redis:
    """
    # Obtém ou inicializa um cliente Redis assíncrono
    # Gets or initializes an asynchronous Redis client
    
    Returns:
        redis.Redis: Cliente Redis assíncrono
    """
    global redis_client
    if redis_client is None:
        logger.info(f"Inicializando conexão Redis: {settings.REDIS_URL}")
        try:
            redis_client = redis.from_url(
                url=settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
            # Verificar conexão
            # Check connection
            await redis_client.ping()
            logger.info("Conexão Redis estabelecida com sucesso")
        except redis.ConnectionError as e:
            logger.error(f"Erro ao conectar ao Redis: {e}")
            raise
    return redis_client


async def close_redis_connection() -> None:
    """
    # Fecha a conexão Redis quando a aplicação é encerrada
    # Closes the Redis connection when the application shuts down
    """
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None
        logger.info("Conexão Redis fechada")


async def set_key(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """
    # Define um valor no Redis com expiração opcional
    # Sets a value in Redis with optional expiration
    
    Args:
        key: Chave Redis
        value: Valor a ser armazenado (será convertido para JSON)
        expire: Tempo de expiração em segundos (opcional)
        
    Returns:
        bool: True se bem-sucedido
    """
    client = await get_redis_client()
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        await client.set(key, value)
        if expire:
            await client.expire(key, expire)
        return True
    except Exception as e:
        logger.error(f"Erro ao definir chave Redis {key}: {e}")
        return False


async def get_key(key: str) -> Optional[str]:
    """
    # Obtém um valor do Redis pela chave
    # Gets a value from Redis by key
    
    Args:
        key: Chave Redis
        
    Returns:
        Optional[str]: O valor armazenado ou None se não encontrado
    """
    client = await get_redis_client()
    try:
        value = await client.get(key)
        return value
    except Exception as e:
        logger.error(f"Erro ao obter chave Redis {key}: {e}")
        return None


async def get_json(key: str) -> Optional[Union[Dict, List]]:
    """
    # Obtém um valor JSON do Redis pela chave
    # Gets a JSON value from Redis by key
    
    Args:
        key: Chave Redis
        
    Returns:
        Optional[Union[Dict, List]]: O valor JSON deserializado ou None
    """
    value = await get_key(key)
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            logger.error(f"Valor para chave {key} não é um JSON válido")
    return None


async def delete_key(key: str) -> bool:
    """
    # Exclui uma chave do Redis
    # Deletes a key from Redis
    
    Args:
        key: Chave Redis
        
    Returns:
        bool: True se excluída com sucesso
    """
    client = await get_redis_client()
    try:
        await client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Erro ao excluir chave Redis {key}: {e}")
        return False


async def add_to_cache_set(set_key: str, value: str) -> bool:
    """
    # Adiciona um valor a um conjunto Redis
    # Adds a value to a Redis set
    
    Args:
        set_key: Chave do conjunto
        value: Valor a ser adicionado
        
    Returns:
        bool: True se adicionado com sucesso
    """
    client = await get_redis_client()
    try:
        await client.sadd(set_key, value)
        return True
    except Exception as e:
        logger.error(f"Erro ao adicionar ao conjunto Redis {set_key}: {e}")
        return False


async def is_in_cache_set(set_key: str, value: str) -> bool:
    """
    # Verifica se um valor existe em um conjunto Redis
    # Checks if a value exists in a Redis set
    
    Args:
        set_key: Chave do conjunto
        value: Valor a verificar
        
    Returns:
        bool: True se o valor estiver no conjunto
    """
    client = await get_redis_client()
    try:
        return bool(await client.sismember(set_key, value))
    except Exception as e:
        logger.error(f"Erro ao verificar membro do conjunto Redis {set_key}: {e}")
        return False

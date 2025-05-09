from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
import uuid

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.token import TokenPayload

# Contexto de criptografia para hashing de senha
# Cryptography context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, int], expires_delta: Optional[timedelta] = None
) -> str:
    """
    # Cria um novo token JWT de acesso
    # Create a new JWT access token
    
    Args:
        subject: O assunto do token (normalmente o ID do usuário)
        expires_delta: Tempo de expiração opcional
        
    Returns:
        Token JWT codificado
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token JWT de refresh para o usuário.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    to_encode = {
        "exp": expire, 
        "sub": str(subject), 
        "type": "refresh",
        "jti": str(uuid.uuid4()) # ID único do token para possibilitar revogação
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str) -> Optional[str]:
    """
    Verifica um token de refresh e retorna o user_id se válido.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            return None
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except jwt.JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    # Verifica se uma senha em texto puro corresponde ao hash armazenado
    # Verify if a plain text password matches the stored hash
    
    Args:
        plain_password: Senha em texto puro
        hashed_password: Hash da senha
        
    Returns:
        bool: True se corresponderem, caso contrário False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    # Gera um hash seguro para a senha fornecida
    # Generate a secure hash for the provided password
    
    Args:
        password: Senha em texto puro
        
    Returns:
        str: Hash da senha
    """
    return pwd_context.hash(password)


def decode_token(token: str) -> TokenPayload:
    """
    # Decodifica um token JWT e retorna seu payload
    # Decode a JWT token and return its payload
    
    Args:
        token: Token JWT
    
    Returns:
        TokenPayload: Payload do token decodificado
    
    Raises:
        ValueError: Se o token for inválido ou expirado
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(sub=payload["sub"], exp=payload["exp"])
    except (jwt.JWTError, ValidationError) as exc:
        raise ValueError("Token inválido") from exc
    
    return token_data
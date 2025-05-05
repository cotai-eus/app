from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.models import User # Importa o modelo User

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    response: Response, # Para definir cookies se necessário
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint de login OAuth2. Recebe username (ou email) e password.
    Retorna um Access Token JWT se a autenticação for bem-sucedida.
    """
    # Comentário em português: Autentica o usuário usando o CRUD.
    user = await crud.user.authenticate(
        db, username_or_email=form_data.username, password=form_data.password
    )
    if not user:
        log.warning(f"Falha na autenticação para o usuário: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not await crud.user.is_active(user):
        log.warning(f"Tentativa de login de usuário inativo: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo")

    # Comentário em português: Cria o token de acesso para o usuário autenticado.
    access_token = security.create_access_token(
        subject=user.user_id, # Usa o user_id como subject do token
    )

    # Comentário em português: Atualiza o campo last_login do usuário.
    # user.last_login = datetime.now(timezone.utc) # Descomente se quiser atualizar last_login
    # await db.commit()

    log.info(f"Usuário autenticado com sucesso: {user.email}")

    # Opcional: Definir o token como um cookie HttpOnly seguro
    # response.set_cookie(
    #     key="access_token",
    #     value=f"Bearer {access_token}",
    #     httponly=True,
    #     max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    #     expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    #     samesite="lax", # ou 'strict'
    #     secure=True, # Requer HTTPS
    # )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/test-token", response_model=schemas.UserPublic)
async def test_token(current_user: User = Depends(deps.get_current_user)):
    """
    Endpoint de teste para verificar se um token é válido.
    Retorna os dados do usuário associado ao token.
    """
    # Comentário em português: Se chegou aqui, o token é válido e get_current_user retornou o usuário.
    log.debug(f"Token testado com sucesso para o usuário: {current_user.email}")
    return current_user


import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.config import settings
from app.models import User # Importa o modelo User
from app.schemas import UserPublic # Importa o schema para comparar

pytestmark = pytest.mark.asyncio

# Update to correct endpoint
AUTH_LOGIN_ENDPOINT = f"{settings.API_V1_STR}/auth/login"

async def test_login_success(client: AsyncClient, test_user: User):
    """ Testa o login bem-sucedido com username e senha. """
    login_data = {
        "username": test_user.username,
        "password": "password123", # Senha definida no fixture test_user
    }
    response = await client.post(AUTH_LOGIN_ENDPOINT, json=login_data)  # Changed to json from data
    assert response.status_code == status.HTTP_200_OK
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

async def test_login_success_email(client: AsyncClient, test_user: User):
    """ Testa o login bem-sucedido com email e senha. """
    login_data = {
        "username": test_user.email, # Usa email no campo username
        "password": "password123",
    }
    response = await client.post(AUTH_LOGIN_ENDPOINT, json=login_data)  # Changed to json from data
    assert response.status_code == status.HTTP_200_OK
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

async def test_login_wrong_password(client: AsyncClient, test_user: User):
    """ Testa o login com senha incorreta. """
    login_data = {
        "username": test_user.username,
        "password": "wrongpassword",
    }
    response = await client.post(AUTH_LOGIN_ENDPOINT, json=login_data)  # Changed to json from data
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
    assert response.json()["detail"] == "Usuário ou senha incorretos"

async def test_login_user_not_found(client: AsyncClient):
    """ Testa o login com usuário inexistente. """
    login_data = {
        "username": "nonexistentuser",
        "password": "password123",
    }
    response = await client.post(AUTH_LOGIN_ENDPOINT, json=login_data)  # Changed to json from data
    assert response.status_code == status.HTTP_401_UNAUTHORIZED # Ainda retorna 401 por segurança
    assert "detail" in response.json()
    assert response.json()["detail"] == "Usuário ou senha incorretos"

async def test_test_token_valid(client: AsyncClient, test_user: User, auth_headers: dict):
    """ Testa o endpoint /test-token com um token válido. """
    response = await client.post(f"{settings.API_V1_STR}/auth/test-token", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    # Compara com o schema UserPublic ou User, dependendo do que /test-token retorna
    assert user_data["email"] == test_user.email
    assert user_data["username"] == test_user.username
    assert user_data["user_id"] == str(test_user.user_id) # Compara como string

async def test_test_token_invalid(client: AsyncClient):
    """ Testa o endpoint /test-token com um token inválido. """
    invalid_headers = {"Authorization": "Bearer invalidtoken"}
    response = await client.post(f"{settings.API_V1_STR}/auth/test-token", headers=invalid_headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
    assert response.json()["detail"] == "Não foi possível validar as credenciais"


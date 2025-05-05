import pytest
from fastapi import status
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user: dict):
    """
    # Teste de login bem-sucedido
    # Test successful login
    """
    response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": test_user["username"], "password": test_user["password"]}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: dict):
    """
    # Teste de login com senha incorreta
    # Test login with incorrect password
    """
    response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": test_user["username"], "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """
    # Teste de login com usuário inexistente
    # Test login with nonexistent user
    """
    response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": "nonexistentuser", "password": "password123"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_signup(client: AsyncClient):
    """
    # Teste de registro de novo usuário
    # Test new user registration
    """
    response = await client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
            "first_name": "New",
            "last_name": "User"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert "user_id" in response.json()
    assert response.json()["email"] == "newuser@example.com"
    assert response.json()["username"] == "newuser"
    assert "password" not in response.json()


@pytest.mark.asyncio
async def test_test_token(client: AsyncClient, user_token_headers: dict):
    """
    # Teste de validação de token
    # Test token validation
    """
    response = await client.post(
        f"{settings.API_V1_STR}/auth/test-token",
        headers=user_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert "user_id" in response.json()

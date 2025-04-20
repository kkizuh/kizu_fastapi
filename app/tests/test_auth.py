import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Регистрация
        response = await ac.post("/register", json={
            "username": "testuser1",
            "email": "test1@mail.com",
            "name": "Тест",
            "password": "123456"
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["username"] == "testuser1"

        # Логин
        response = await ac.post("/login", json={
            "username": "testuser1",
            "password": "123456"
        })
        assert response.status_code == 200
        token_data = response.json()
        assert token_data["token"]

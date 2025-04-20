import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_add_and_get_transactions():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Регистрация и логин
        await ac.post("/register", json={
            "username": "usertrx",
            "email": "trx@mail.com",
            "name": "Транзакционер",
            "password": "pass123"
        })
        login = await ac.post("/login", json={
            "username": "usertrx",
            "password": "pass123"
        })
        token = login.json()["token"]

        headers = {"Authorization": f"Bearer {token}"}

        # Добавление транзакции
        trx = {
            "title": "Кофе",
            "amount": 100,
            "type": "expense",
            "category": "еда",
            "date": "2025-04-20"
        }
        add_resp = await ac.post("/transactions", json=trx, headers=headers)
        assert add_resp.status_code == 200

        # Получение транзакций
        get_resp = await ac.get("/transactions", headers=headers)
        assert get_resp.status_code == 200
        assert len(get_resp.json()) > 0

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from db_app.api.main import app
from db_app.db.database import get_db, Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.anyio
async def test_get_all_currencies(async_client):
    response = await async_client.get("/currencies/currencies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_currency_by_char_code(async_client):
    response = await async_client.get("/currencies/currency/USD")
    if response.status_code == 404:
        assert response.json() == {"detail": "Currency not found"}
    else:
        assert response.status_code == 200
        assert response.json()["char_code"] == "USD"


@pytest.mark.anyio
async def test_manual_update(async_client):
    response = await async_client.post("/currencies/manual_update")
    assert response.status_code == 200
    assert response.json() == {"message": "Currency rates updated successfully"}


@pytest.mark.anyio
async def test_get_non_existing_currency(async_client):
    response = await async_client.get("/currencies/currency/NON_EXISTENT")
    assert response.status_code == 404
    assert response.json() == {"detail": "Currency not found"}

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.deps import get_db
from app.db.base import Base
from app.main import app


@pytest.fixture
async def test_client():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    TestingSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.asyncio
async def test_register_login_me_flow(test_client):
    register_response = await test_client.post(
        "/auth/register",
        json={
            "email": "test@email.com",
            "password": "123456",
        },
    )

    assert register_response.status_code == 201
    user = register_response.json()
    assert user["email"] == "test@email.com"
    assert user["role"] == "user"
    assert "password_hash" not in user

    login_response = await test_client.post(
        "/auth/login",
        data={
            "username": "test@email.com",
            "password": "123456",
        },
    )

    assert login_response.status_code == 200
    token_data = login_response.json()
    assert token_data["token_type"] == "bearer"
    assert token_data["access_token"]

    me_response = await test_client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token_data['access_token']}",
        },
    )

    assert me_response.status_code == 200
    me = me_response.json()
    assert me["email"] == "test@email.com"
    assert me["role"] == "user"
    assert "password_hash" not in me

@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(test_client):
    payload = {
        "email": "duplicate@email.com",
        "password": "123456",
    }

    first_response = await test_client.post("/auth/register", json=payload)
    second_response = await test_client.post("/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_login_with_wrong_password_returns_401(test_client):
    await test_client.post(
        "/auth/register",
        json={
            "email": "wrong-password@email.com",
            "password": "123456",
        },
    )

    response = await test_client.post(
        "/auth/login",
        data={
            "username": "wrong-password@email.com",
            "password": "wrong",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_without_token_returns_401(test_client):
    response = await test_client.get("/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_invalid_token_returns_401(test_client):
    response = await test_client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401

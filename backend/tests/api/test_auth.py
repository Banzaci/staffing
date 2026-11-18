
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.exc import IntegrityError

from app.api.public.v1.auth import router
from app.db.session import get_db


app = FastAPI()
app.include_router(router)


def mock_db_result(value):
    result = MagicMock()
    result.scalar_one_or_none.return_value = value
    return result


@pytest.mark.asyncio
async def test_register_success():
    db = AsyncMock()
    db.execute.return_value = mock_db_result(None)

    async def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db

    try:
        with patch(
            "app.api.public.v1.auth.hash_password",
            return_value="hashed-password",
        ):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                response = await client.post(
                    "/auth/register",
                    json={
                        "email": "TEST@example.com",
                        "password": "TestPassword123!",
                        "first_name": "Test",
                        "last_name": "User",
                        "preferred_language": "en",
                    },
                )

        assert response.status_code == 201
        assert response.json()["email"] == "test@example.com"

        user = db.add.call_args.args[0]
        assert user.password_hash == "hashed-password"
        assert user.email == "test@example.com"
        db.commit.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_register_duplicate_email():
    db = AsyncMock()
    db.execute.return_value = mock_db_result(uuid.uuid4())

    async def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post(
                "/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "TestPassword123!",
                    "first_name": "Test",
                    "last_name": "User",
                },
            )

        assert response.status_code == 409
        db.add.assert_not_called()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_success():
    user = SimpleNamespace(
        id=uuid.uuid4(),
        is_active=True,
        password_hash="hashed-password",
    )

    db = AsyncMock()
    db.execute.return_value = mock_db_result(user)

    async def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db

    try:
        with (
            patch(
                "app.api.public.v1.auth.verify_password",
                return_value=True,
            ),
            patch(
                "app.api.public.v1.auth.create_access_token",
                return_value="test-jwt-token",
            ),
        ):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                response = await client.post(
                    "/auth/login",
                    json={
                        "email": "test@example.com",
                        "password": "TestPassword123!",
                    },
                )

        assert response.status_code == 200
        assert response.json() == {
            "access_token": "test-jwt-token",
            "token_type": "bearer",
        }
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_invalid_password():
    user = SimpleNamespace(
        id=uuid.uuid4(),
        is_active=True,
        password_hash="hashed-password",
    )

    db = AsyncMock()
    db.execute.return_value = mock_db_result(user)

    async def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db

    try:
        with patch(
            "app.api.public.v1.auth.verify_password",
            return_value=False,
        ):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                response = await client.post(
                    "/auth/login",
                    json={
                        "email": "test@example.com",
                        "password": "wrong-password",
                    },
                )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"
    finally:
        app.dependency_overrides.clear()

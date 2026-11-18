
import uuid
from unittest.mock import AsyncMock, MagicMock
from unittest.mock import patch
from types import SimpleNamespace
from fastapi import HTTPException
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from app.services.shift_application_service import withdraw_shift_application
from app.api.private.v1.shift_applications import router
from app.auth.dependencies import get_current_user
from app.db.session import get_db


app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_approve_forbidden():
    user = MagicMock(id=uuid.uuid4())
    application = MagicMock(id=uuid.uuid4())
    shift = MagicMock(business_id=uuid.uuid4())

    async def override_user():
        return user

    async def override_db():
        yield db

    db = AsyncMock()
    result = MagicMock()
    result.one_or_none.return_value = (application, shift)
    db.execute.return_value = result

    app.dependency_overrides[get_current_user] = override_user
    app.dependency_overrides[get_db] = override_db

    try:
        with patch(
            "app.api.private.v1.shift_applications.require_business_access",
            new_callable=AsyncMock,
            side_effect=HTTPException(status_code=403, detail="Forbidden"),
        ):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                response = await client.post(
                    f"/shift-applications/{application.id}/approve"
                )

        assert response.status_code == 403
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_approve_success():
    user = MagicMock(id=uuid.uuid4())
    application = MagicMock(id=uuid.uuid4())
    shift = MagicMock(business_id=uuid.uuid4())

    approved = MagicMock(
        id=application.id,
        status="accepted",
    )

    async def override_user():
        return user

    async def override_db():
        yield db

    db = AsyncMock()
    result = MagicMock()
    result.one_or_none.return_value = (application, shift)
    db.execute.return_value = result

    app.dependency_overrides[get_current_user] = override_user
    app.dependency_overrides[get_db] = override_db

    try:
        with (
            patch(
                "app.api.private.v1.shift_applications.require_business_access",
                new_callable=AsyncMock,
            ),
            patch(
                "app.api.private.v1.shift_applications.approve_shift_application",
                new_callable=AsyncMock,
                return_value=approved,
            ),
        ):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                response = await client.post(
                    f"/shift-applications/{application.id}/approve"
                )

        assert response.status_code == 200
        assert response.json()["status"] == "accepted"
        db.commit.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_approve_requires_authentication():
    db = AsyncMock()

    async def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post(
                f"/shift-applications/{uuid.uuid4()}/approve"
            )

        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_application_not_found():
    user = MagicMock(id=uuid.uuid4())

    async def override_user():
        return user

    db = AsyncMock()
    result = MagicMock()
    result.one_or_none.return_value = None
    db.execute.return_value = result

    async def override_db():
        yield db

    app.dependency_overrides[get_current_user] = override_user
    app.dependency_overrides[get_db] = override_db

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post(
                f"/shift-applications/{uuid.uuid4()}/approve"
            )

        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()



@pytest.mark.asyncio
async def test_reject_application():
    user = MagicMock(id=uuid.uuid4())
    application = MagicMock(
        id=uuid.uuid4(),
        status="pending",
    )
    shift = MagicMock(business_id=uuid.uuid4())

    db = AsyncMock()
    result = MagicMock()
    result.one_or_none.return_value = (application, shift)
    db.execute.return_value = result

    async def override_user():
        return user

    async def override_db():
        yield db

    app.dependency_overrides[get_current_user] = override_user
    app.dependency_overrides[get_db] = override_db

    try:
        with patch(
            "app.api.private.v1.shift_applications.require_business_access",
            new_callable=AsyncMock,
        ):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                response = await client.post(
                    f"/shift-applications/{application.id}/reject"
                )

        assert response.status_code == 200
        assert response.json()["status"] == "rejected"
        db.commit.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_withdraw_application_success():
    user = MagicMock(id=uuid.uuid4())
    application_id = uuid.uuid4()
    application = SimpleNamespace(
        id=application_id,
        status="withdrawn",
    )

    db = AsyncMock()

    async def override_user():
        return user

    async def override_db():
        yield db

    app.dependency_overrides[get_current_user] = override_user
    app.dependency_overrides[get_db] = override_db

    try:
        with patch(
            "app.api.private.v1.shift_applications.withdraw_shift_application",
            new_callable=AsyncMock,
            return_value=application,
        ) as service:
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                response = await client.post(
                    f"/shift-applications/{application_id}/withdraw"
                )

        assert response.status_code == 200
        assert response.json()["status"] == "withdrawn"
        db.commit.assert_awaited_once()
        service.assert_awaited_once_with(
            db=db,
            user_id=user.id,
            application_id=application_id,
        )
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_withdraw_application_not_found():
    user = MagicMock(id=uuid.uuid4())
    application_id = uuid.uuid4()
    db = AsyncMock()

    async def override_user():
        return user

    async def override_db():
        yield db

    app.dependency_overrides[get_current_user] = override_user
    app.dependency_overrides[get_db] = override_db

    try:
        with patch(
            "app.api.private.v1.shift_applications.withdraw_shift_application",
            new_callable=AsyncMock,
            side_effect=ValueError("Application not found"),
        ):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                response = await client.post(
                    f"/shift-applications/{application_id}/withdraw"
                )

        assert response.status_code == 404
        db.rollback.assert_awaited_once()
        db.commit.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()
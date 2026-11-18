
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock
from datetime import datetime, timedelta, timezone
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from app.api.private.v1.shifts import router
from app.auth.dependencies import get_current_user
from app.db.session import get_db


@pytest.fixture
def setup():
    app = FastAPI()
    app.include_router(router, prefix="/api/private/v1")

    db = AsyncMock()
    user = SimpleNamespace(id=uuid.uuid4())

    async def override_db():
        yield db

    async def override_user():
        return user

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = override_user

    return app, db, user


def test_apply_to_shift_success(setup, monkeypatch):
    app, db, user = setup
    shift_id = uuid.uuid4()

    application = SimpleNamespace(
        id=uuid.uuid4(),
        job_shift_id=shift_id,
        status="pending",
    )

    service = AsyncMock(return_value=application)
    monkeypatch.setattr(
        "app.api.private.v1.shifts.apply_for_shift",
        service,
    )

    with TestClient(app) as client:
        response = client.post(
            f"/api/private/v1/shifts/{shift_id}/apply"
        )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    db.commit.assert_awaited_once()
    service.assert_awaited_once_with(
        db=db,
        user_id=user.id,
        shift_id=shift_id,
    )


def test_apply_to_shift_invalid(setup, monkeypatch):
    app, db, _ = setup
    shift_id = uuid.uuid4()

    service = AsyncMock(
        side_effect=ValueError("Worker does not have the required skill")
    )
    monkeypatch.setattr(
        "app.api.private.v1.shifts.apply_for_shift",
        service,
    )

    with TestClient(app) as client:
        response = client.post(
            f"/api/private/v1/shifts/{shift_id}/apply"
        )

    assert response.status_code == 400
    assert "required skill" in response.json()["detail"]
    db.rollback.assert_awaited_once()
    db.commit.assert_not_awaited()


def test_apply_to_shift_duplicate(setup, monkeypatch):
    app, db, _ = setup
    shift_id = uuid.uuid4()

    service = AsyncMock(
        side_effect=IntegrityError(
            statement="INSERT INTO shift_applications",
            params={},
            orig=Exception("duplicate key"),
        )
    )
    monkeypatch.setattr(
        "app.api.private.v1.shifts.apply_for_shift",
        service,
    )

    with TestClient(app) as client:
        response = client.post(
            f"/api/private/v1/shifts/{shift_id}/apply"
        )

    assert response.status_code == 409
    db.rollback.assert_awaited_once()


def test_apply_to_shift_unauthorized():
    app = FastAPI()
    app.include_router(router, prefix="/api/private/v1")

    with TestClient(app) as client:
        response = client.post(
            f"/api/private/v1/shifts/{uuid.uuid4()}/apply"
        )

    assert response.status_code == 401



def test_list_available_shifts_success(setup, monkeypatch):
    app, db, _ = setup

    shift = SimpleNamespace(
        id=uuid.uuid4(),
        business_id=uuid.uuid4(),
        skill_id=uuid.uuid4(),
        starts_at=datetime.now(timezone.utc) + timedelta(days=1),
        ends_at=datetime.now(timezone.utc) + timedelta(days=2),
        hourly_rate=150,
        currency="PHP",
        workers_needed=2,
    )

    service = AsyncMock(return_value=[shift])

    monkeypatch.setattr(
        "app.api.private.v1.shifts.search_shifts",
        service,
    )

    with TestClient(app) as client:
        response = client.get(
            "/api/private/v1/shifts?country_code=PH&limit=20"
        )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["currency"] == "PHP"

    assert service.await_args.kwargs["country_code"] == "PH"
    assert service.await_args.kwargs["limit"] == 20


def test_list_available_shifts_invalid_timezone(setup):
    app, _, _ = setup

    with TestClient(app) as client:
        response = client.get(
            "/api/private/v1/shifts"
            "?starts_from=2026-12-01T10:00:00"
        )

    assert response.status_code == 422



def test_search_shifts_by_location(setup, monkeypatch):
    app, _, _ = setup

    service = AsyncMock(return_value=[])

    monkeypatch.setattr(
        "app.api.private.v1.shifts.search_shifts",
        service,
    )

    with TestClient(app) as client:
        response = client.get(
            "/api/private/v1/shifts"
            "?latitude=9.7845"
            "&longitude=126.1589"
            "&radius_km=20"
        )

    assert response.status_code == 200
    assert response.json() == []

    kwargs = service.await_args.kwargs

    assert kwargs["latitude"] == 9.7845
    assert kwargs["longitude"] == 126.1589
    assert kwargs["radius_km"] == 20


def test_search_shifts_missing_longitude(setup):
    app, _, _ = setup

    with TestClient(app) as client:
        response = client.get(
            "/api/private/v1/shifts?latitude=9.7845"
        )

    assert response.status_code == 422


import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.private.v1.skills import router
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


def mock_scalar_results(db, *values):
    db.scalar.side_effect = values


def test_list_skills_success(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()

    result = MagicMock()
    result.all.return_value = [
        (skill_id, "waiter", "en", "Waiter"),
        (skill_id, "waiter", "sv", "Servitör"),
    ]
    db.execute.return_value = result

    with TestClient(app) as client:
        response = client.get("/api/private/v1/skills")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(skill_id),
            "code": "waiter",
            "translations": {
                "en": "Waiter",
                "sv": "Servitör",
            },
        }
    ]
    db.execute.assert_awaited_once()


def test_create_worker_skill_success(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()
    profile_id = uuid.uuid4()

    profile = SimpleNamespace(id=profile_id)
    skill = SimpleNamespace(id=skill_id)

    mock_scalar_results(db, profile, None)
    db.get.return_value = skill

    with TestClient(app) as client:
        response = client.put(
            f"/api/private/v1/skills/{skill_id}/me",
            json={
                "years_experience": 3,
                "min_hourly_rate": 100,
                "max_hourly_rate": 200,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "skill_id": str(skill_id),
        "years_experience": 3,
        "min_hourly_rate": 100,
        "max_hourly_rate": 200,
    }
    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()


def test_update_worker_skill_success(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()

    profile = SimpleNamespace(id=uuid.uuid4())
    skill = SimpleNamespace(id=skill_id)

    worker_skill = SimpleNamespace(
        skill_id=skill_id,
        years_experience=1,
        min_hourly_rate=None,
        max_hourly_rate=None,
    )

    mock_scalar_results(db, profile, worker_skill)
    db.get.return_value = skill

    with TestClient(app) as client:
        response = client.put(
            f"/api/private/v1/skills/{skill_id}/me",
            json={"years_experience": 5},
        )

    assert response.status_code == 200
    assert response.json()["years_experience"] == 5
    assert worker_skill.years_experience == 5
    db.add.assert_not_called()
    db.commit.assert_awaited_once()


def test_create_worker_skill_invalid_experience(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()

    with TestClient(app) as client:
        response = client.put(
            f"/api/private/v1/skills/{skill_id}/me",
            json={"years_experience": -1},
        )

    assert response.status_code == 422
    db.commit.assert_not_awaited()


def test_create_worker_skill_invalid_rate_range(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()

    with TestClient(app) as client:
        response = client.put(
            f"/api/private/v1/skills/{skill_id}/me",
            json={
                "years_experience": 2,
                "min_hourly_rate": 200,
                "max_hourly_rate": 100,
            },
        )

    assert response.status_code == 422
    db.commit.assert_not_awaited()


def test_create_worker_skill_profile_not_found(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()
    db.scalar.return_value = None

    with TestClient(app) as client:
        response = client.put(
            f"/api/private/v1/skills/{skill_id}/me",
            json={"years_experience": 2},
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Worker profile not found"
    db.commit.assert_not_awaited()


def test_create_worker_skill_skill_not_found(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()

    db.scalar.return_value = SimpleNamespace(id=uuid.uuid4())
    db.get.return_value = None

    with TestClient(app) as client:
        response = client.put(
            f"/api/private/v1/skills/{skill_id}/me",
            json={"years_experience": 2},
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found"
    db.commit.assert_not_awaited()


def test_delete_worker_skill_success(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()

    profile = SimpleNamespace(id=uuid.uuid4())
    worker_skill = SimpleNamespace(skill_id=skill_id)

    mock_scalar_results(db, profile, worker_skill)

    with TestClient(app) as client:
        response = client.delete(
            f"/api/private/v1/skills/{skill_id}/me"
        )

    assert response.status_code == 204
    db.delete.assert_awaited_once_with(worker_skill)
    db.commit.assert_awaited_once()


def test_delete_worker_skill_not_found(setup):
    app, db, user = setup
    skill_id = uuid.uuid4()

    profile = SimpleNamespace(id=uuid.uuid4())
    mock_scalar_results(db, profile, None)

    with TestClient(app) as client:
        response = client.delete(
            f"/api/private/v1/skills/{skill_id}/me"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Worker skill not found"
    db.delete.assert_not_awaited()
    db.commit.assert_not_awaited()


import uuid
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.shift_application_service import withdraw_shift_application
from app.services.shift_application_service import apply_for_shift


def make_db(values):
    db = AsyncMock()
    results = []

    for value in values:
        result = MagicMock()
        result.scalar_one_or_none.return_value = value
        result.scalar_one.return_value = value
        results.append(result)

    db.execute.side_effect = results
    return db


def make_worker_and_shift():
    worker = MagicMock()
    worker.id = uuid.uuid4()

    shift = MagicMock()
    shift.id = uuid.uuid4()
    shift.skill_id = uuid.uuid4()
    shift.status = "open"
    shift.workers_needed = 2
    shift.starts_at = datetime.now(timezone.utc) + timedelta(days=2)
    shift.ends_at = shift.starts_at + timedelta(hours=4)

    return worker, shift


@pytest.mark.asyncio
async def test_apply_for_shift():
    worker, shift = make_worker_and_shift()

    db = make_db([
        worker,
        shift,
        shift.skill_id,
        None,
        0,
    ])

    with (
        patch(
            "app.services.shift_application_service.is_worker_available",
            new_callable=AsyncMock,
            return_value=True,
        ),
        patch(
            "app.services.shift_application_service.has_shift_conflict",
            new_callable=AsyncMock,
            return_value=False,
        ),
    ):
        application = await apply_for_shift(
            db, uuid.uuid4(), shift.id
        )

    assert application.status == "pending"
    assert application.worker_profile_id == worker.id
    db.add.assert_called_once()
    db.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_apply_without_required_skill():
    worker, shift = make_worker_and_shift()

    db = make_db([
        worker,
        shift,
        None,
    ])

    with pytest.raises(ValueError, match="required skill"):
        await apply_for_shift(db, uuid.uuid4(), shift.id)

    db.add.assert_not_called()

@pytest.mark.asyncio
async def test_withdraw_pending_application():
    user_id = uuid.uuid4()
    application = MagicMock()
    application.id = uuid.uuid4()
    application.status = "pending"
    application.deleted_at = None

    db = make_db([application])

    result = await withdraw_shift_application(
        db, user_id, application.id
    )

    assert result.status == "withdrawn"
    assert result.deleted_at is not None
    db.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_cannot_withdraw_accepted_application():
    application = MagicMock()
    application.id = uuid.uuid4()
    application.status = "accepted"

    db = make_db([application])

    with pytest.raises(ValueError, match="Only pending"):
        await withdraw_shift_application(
            db, uuid.uuid4(), application.id
        )

    db.flush.assert_not_awaited()


@pytest.mark.asyncio
async def test_cannot_withdraw_another_workers_application():
    db = make_db([None])

    with pytest.raises(ValueError, match="Application not found"):
        await withdraw_shift_application(
            db, uuid.uuid4(), uuid.uuid4()
        )

    db.flush.assert_not_awaited()
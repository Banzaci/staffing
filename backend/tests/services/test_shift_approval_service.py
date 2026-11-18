
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.shift_approval import approve_shift_application



def make_db(application, shift, accepted_count=0, country_code="PH"):
    db = AsyncMock()

    values = [
        application,
        application.worker_profile_id,
        shift,
        application,
        accepted_count,
        country_code,
    ]

    results = []

    for value in values:
        result = MagicMock()
        result.scalar_one_or_none.return_value = value
        result.scalar_one.return_value = value
        results.append(result)

    db.execute.side_effect = results

    return db

@pytest.mark.asyncio
async def test_reject_fully_staffed_shift():
    application, shift = make_application_and_shift()
    db = make_db(application, shift, accepted_count=2)

    with pytest.raises(ValueError, match="fully staffed"):
        await approve_shift_application(db, application.id)

    assert application.status == "pending"
    db.flush.assert_not_awaited()

def make_application_and_shift():
    shift_id = uuid.uuid4()
    start = datetime(2026, 12, 1, 9, tzinfo=timezone.utc)

    application = MagicMock(
        id=uuid.uuid4(),
        job_shift_id=shift_id,
        worker_profile_id=uuid.uuid4(),
        status="pending",
    )

    shift = MagicMock(
        id=shift_id,
        starts_at=start,
        ends_at=start + timedelta(hours=3),
        status="open",
        workers_needed=2,
    )

    return application, shift


@pytest.mark.asyncio
async def test_approve_shift_application():
    application, shift = make_application_and_shift()
    db = make_db(application, shift)

    with (
        patch(
            "app.services.shift_approval.is_worker_available",
            new_callable=AsyncMock,
            return_value=True,
        ),
        patch(
            "app.services.shift_approval.has_shift_conflict",
            new_callable=AsyncMock,
            return_value=False,
        ),
        patch(
            "app.services.shift_approval.has_work_authorization",
            new_callable=AsyncMock,
            return_value=True,
        ),
    ):
        result = await approve_shift_application(db, application.id)

    assert result.status == "accepted"
    db.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_reject_overlapping_shift():
    application, shift = make_application_and_shift()
    db = make_db(application, shift)

    with (
        patch(
            "app.services.shift_approval.is_worker_available",
            new_callable=AsyncMock,
            return_value=True,
        ),
        patch(
            "app.services.shift_approval.has_shift_conflict",
            new_callable=AsyncMock,
            return_value=True,
        ),
        patch(
            "app.services.shift_approval.has_work_authorization",
            new_callable=AsyncMock,
            return_value=True,
        ),
    ):
        with pytest.raises(ValueError, match="overlapping"):
            await approve_shift_application(db, application.id)

    assert application.status == "pending"
    db.flush.assert_not_awaited()


@pytest.mark.asyncio
async def test_reject_without_work_authorization():
    application, shift = make_application_and_shift()
    db = make_db(application, shift)

    with patch(
        "app.services.shift_approval.has_work_authorization",
        new_callable=AsyncMock,
        return_value=False,
    ):
        with pytest.raises(ValueError, match="work authorization"):
            await approve_shift_application(db, application.id)

    assert application.status == "pending"
    db.flush.assert_not_awaited()
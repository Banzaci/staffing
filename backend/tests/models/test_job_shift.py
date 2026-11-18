
import uuid
from datetime import datetime, timezone, timedelta

from app.models.job_shift import JobShift


def test_create_job_shift():
    starts_at = datetime(
        2026, 12, 1, 9, 0, tzinfo=timezone.utc
    )
    ends_at = starts_at + timedelta(hours=3)

    business_id = uuid.uuid4()
    skill_id = uuid.uuid4()

    shift = JobShift(
        business_id=business_id,
        skill_id=skill_id,
        starts_at=starts_at,
        ends_at=ends_at,
        hourly_rate=150.00,
        currency="PHP",
        workers_needed=2,
        status="open",
    )

    assert shift.business_id == business_id
    assert shift.skill_id == skill_id
    assert shift.starts_at == starts_at
    assert shift.ends_at == ends_at
    assert shift.hourly_rate == 150.00
    assert shift.currency == "PHP"
    assert shift.workers_needed == 2
    assert shift.status == "open"


def test_job_shift_defaults():
    shift = JobShift(
        business_id=uuid.uuid4(),
        skill_id=uuid.uuid4(),
        starts_at=datetime.now(timezone.utc),
        ends_at=datetime.now(timezone.utc) + timedelta(hours=3),
        hourly_rate=120.00,
        currency="PHP",
    )

    assert shift.workers_needed is None
    assert shift.status is None
    assert shift.created_at is None

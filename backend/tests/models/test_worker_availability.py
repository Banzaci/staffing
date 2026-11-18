
import uuid
from datetime import datetime, timedelta, timezone

from app.models.worker_availability import WorkerAvailability


def test_create_worker_availability():
    worker_id = uuid.uuid4()
    starts_at = datetime(2026, 12, 1, 8, 0, tzinfo=timezone.utc)
    ends_at = starts_at + timedelta(hours=4)

    availability = WorkerAvailability(
        worker_profile_id=worker_id,
        starts_at=starts_at,
        ends_at=ends_at,
    )

    assert availability.worker_profile_id == worker_id
    assert availability.starts_at == starts_at
    assert availability.ends_at == ends_at
    assert availability.deleted_at is None


def test_multiple_availability_periods():
    worker_id = uuid.uuid4()
    day = datetime(2026, 12, 1, tzinfo=timezone.utc)

    morning = WorkerAvailability(
        worker_profile_id=worker_id,
        starts_at=day + timedelta(hours=8),
        ends_at=day + timedelta(hours=12),
    )

    evening = WorkerAvailability(
        worker_profile_id=worker_id,
        starts_at=day + timedelta(hours=17),
        ends_at=day + timedelta(hours=22),
    )

    assert morning.ends_at < evening.starts_at
    assert morning.worker_profile_id == evening.worker_profile_id

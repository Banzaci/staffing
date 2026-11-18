
import uuid

from app.models.shift_application import ShiftApplication


def test_create_shift_application():
    shift_id = uuid.uuid4()
    worker_id = uuid.uuid4()

    application = ShiftApplication(
        job_shift_id=shift_id,
        worker_profile_id=worker_id,
        status="pending",
    )

    assert application.job_shift_id == shift_id
    assert application.worker_profile_id == worker_id
    assert application.status == "pending"
    assert application.id is None


def test_shift_application_defaults():
    application = ShiftApplication(
        job_shift_id=uuid.uuid4(),
        worker_profile_id=uuid.uuid4(),
    )

    assert application.status is None
    assert application.created_at is None


import uuid
from datetime import date

from app.models.worker_work_authorization import WorkerWorkAuthorization


def test_create_work_authorization():
    worker_id = uuid.uuid4()

    authorization = WorkerWorkAuthorization(
        worker_profile_id=worker_id,
        country_code="PH",
        authorization_type="work_permit",
        expires_at=date(2027, 12, 31),
        verification_status="verified",
    )

    assert authorization.worker_profile_id == worker_id
    assert authorization.country_code == "PH"
    assert authorization.authorization_type == "work_permit"
    assert authorization.expires_at == date(2027, 12, 31)
    assert authorization.verification_status == "verified"


def test_citizen_authorization():
    authorization = WorkerWorkAuthorization(
        worker_profile_id=uuid.uuid4(),
        country_code="SE",
        authorization_type="citizen",
    )

    assert authorization.country_code == "SE"
    assert authorization.authorization_type == "citizen"
    assert authorization.expires_at is None


def test_authorization_defaults():
    authorization = WorkerWorkAuthorization(
        worker_profile_id=uuid.uuid4(),
        country_code="GH",
        authorization_type="other",
    )

    assert authorization.verification_status is None
    assert authorization.verified_at is None

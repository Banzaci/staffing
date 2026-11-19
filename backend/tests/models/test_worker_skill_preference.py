import uuid

from app.models.worker_skill_preference import WorkerSkillPreference


def test_create_worker_skill_preference():
    worker_profile_id = uuid.uuid4()
    skill_id = uuid.uuid4()

    preference = WorkerSkillPreference(
        worker_profile_id=worker_profile_id,
        skill_id=skill_id,
    )

    assert preference.worker_profile_id == worker_profile_id
    assert preference.skill_id == skill_id


def test_worker_skill_preference_composite_primary_key():
    primary_keys = {
        column.name
        for column in WorkerSkillPreference.__table__.primary_key.columns
    }

    assert primary_keys == {"worker_profile_id", "skill_id"}
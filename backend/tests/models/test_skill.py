import uuid

from app.models.skill import Skill
from app.models.worker_skill import WorkerSkill
from app.models.skill_translation import SkillTranslation
from app.models.worker_skill_preference import WorkerSkillPreference


def test_skill_translation():
    skill_id = uuid.uuid4()

    translation = SkillTranslation(
        skill_id=skill_id,
        language_code="sv",
        name="Bartender",
    )

    assert translation.skill_id == skill_id
    assert translation.language_code == "sv"
    assert translation.name == "Bartender"


def test_create_skill():
    skill = Skill(code="bartender")

    assert skill.code == "bartender"
    assert skill.id is None


def test_create_worker_skill():
    worker_profile_id = uuid.uuid4()
    skill_id = uuid.uuid4()

    worker_skill = WorkerSkill(
        worker_profile_id=worker_profile_id,
        skill_id=skill_id,
        years_experience=5,
    )

    assert worker_skill.worker_profile_id == worker_profile_id
    assert worker_skill.skill_id == skill_id
    assert worker_skill.years_experience == 5


def test_worker_skill_default():
    worker_skill = WorkerSkill(
        worker_profile_id=uuid.uuid4(),
        skill_id=uuid.uuid4(),
    )

    assert worker_skill.years_experience is None


def test_create_worker_skill_preference():
    worker_profile_id = uuid.uuid4()
    skill_id = uuid.uuid4()

    preference = WorkerSkillPreference(
        worker_profile_id=worker_profile_id,
        skill_id=skill_id,
    )

    assert preference.worker_profile_id == worker_profile_id
    assert preference.skill_id == skill_id
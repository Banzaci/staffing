
import uuid

from app.models.language import Language
from app.models.worker_language import WorkerLanguage


def test_create_language():
    language = Language(
        code="ceb-PH",
        name="Cebuano",
    )

    assert language.code == "ceb-PH"
    assert language.name == "Cebuano"


def test_create_worker_language():
    worker_id = uuid.uuid4()

    worker_language = WorkerLanguage(
        worker_profile_id=worker_id,
        language_code="ceb-PH",
        proficiency="native",
    )

    assert worker_language.worker_profile_id == worker_id
    assert worker_language.language_code == "ceb-PH"
    assert worker_language.proficiency == "native"

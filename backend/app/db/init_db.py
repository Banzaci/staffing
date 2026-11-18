from app.db.base import Base
from app.db.session import engine
from app.models import (
    business,
    business_type,
    business_type_translation,
    employer,
    job_shift,
    language,
    shift_application,
    skill,
    skill_translation,
    user,
    worker_availability,
    worker_language,
    worker_profile,
    worker_skill,
    worker_work_authorization
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
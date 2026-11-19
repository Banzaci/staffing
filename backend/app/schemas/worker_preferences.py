import uuid
from pydantic import BaseModel

class WorkerPreferencesUpdate(BaseModel):
    skill_ids: list[uuid.UUID]
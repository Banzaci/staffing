from pydantic import BaseModel, Field

class WorkerSkillInput(BaseModel):
    years_experience: int = Field(ge=0)
    min_hourly_rate: float | None = Field(default=None, ge=0)
    max_hourly_rate: float | None = Field(default=None, ge=0)

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class JobShiftCreate(BaseModel):
    business_id: uuid.UUID
    skill_id: uuid.UUID
    starts_at: datetime
    ends_at: datetime
    hourly_rate: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    workers_needed: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def validate_shift(self):
        if self.starts_at.tzinfo is None or self.ends_at.tzinfo is None:
            raise ValueError("Shift dates must include a timezone")

        if self.starts_at >= self.ends_at:
            raise ValueError("Shift end must be after start")

        return self

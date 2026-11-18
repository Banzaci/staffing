
import uuid

from pydantic import BaseModel, Field


class BusinessCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    business_type_id: uuid.UUID
    country_code: str = Field(min_length=2, max_length=2)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

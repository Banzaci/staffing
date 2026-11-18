
from pydantic import BaseModel, Field, model_validator


class WorkerProfileCreate(BaseModel):
    bio: str | None = None
    avatar_url: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    willing_to_travel: bool = False

    @model_validator(mode="after")
    def validate_coordinates(self):
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError(
                "Latitude and longitude must be provided together"
            )
        return self

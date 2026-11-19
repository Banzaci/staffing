from app.models.user import UserRole
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class LoginRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "test1@test.com",
                "password": "Test1234"
            }
        }
    )

    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    role: UserRole
    preferred_language: str = Field(default="en", min_length=2, max_length=10)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
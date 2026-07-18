from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRegister(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized.count("@") != 1 or normalized.startswith("@"):
            raise ValueError("A valid email address is required")
        local_part, domain = normalized.split("@")
        if not local_part or "." not in domain or domain.startswith("."):
            raise ValueError("A valid email address is required")
        return normalized


class UserLogin(UserRegister):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)

import string

from uuid import UUID

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, SecretStr, field_validator, ConfigDict


def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid characters in username."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    username: str
    password: str
    last_login: str
    created_at: str
    is_active: bool
    role: str


class UserCreate(BaseModel):
    company_id: UUID
    username: str
    password: str
    role: str

    @field_validator("username")
    def validate_username(cls, username: str) -> str:
        return validate_username(username)


class UserOut(BaseModel):
    username: str

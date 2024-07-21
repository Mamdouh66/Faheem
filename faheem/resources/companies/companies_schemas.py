import string

from uuid import UUID

from pydantic import BaseModel, field_validator, ConfigDict


def validate_company_name(company_name: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(
        char in allowed for char in company_name
    ), "Invalid characters in company_name."
    assert len(company_name) >= 1, "company_name must be 1 characters or more."
    return company_name


class CompanyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str
    created_at: str
    competitor: list[str]


class CompanyCreate(BaseModel):
    name: str
    description: str
    competitor: list[str]

    @field_validator("name")
    def validate_company_name(cls, name: str) -> str:
        return validate_company_name(name)


class CompanyOut(BaseModel):
    name: str
    description: str
    competitor: list[str]

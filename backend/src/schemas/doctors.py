from datetime import datetime
from typing import Literal

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from database import DoctorEmploymentTypeEnum, users_validators


PHONE_NUMBER_DESCRIPTION = (
    "Phone number in international E.164 format. Spaces, parentheses, "
    "and hyphens are removed before validation."
)


class DoctorPhoneNumberRequestSchema(BaseModel):
    phone_number: str | None = Field(
        default=None,
        pattern=users_validators.PHONE_NUMBER_PATTERN,
        description=PHONE_NUMBER_DESCRIPTION,
        examples=["+380501112233"],
    )

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_phone_number(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        return users_validators.normalize_phone_number(value)


class DoctorProfileCreateRequestSchema(DoctorPhoneNumberRequestSchema):
    user_id: int = Field(..., ge=1)
    specialization: str = Field(..., min_length=1, max_length=100)
    years_experience: int | None = Field(default=None, ge=0, le=80)
    employment_type: DoctorEmploymentTypeEnum | None = None
    avatar: UploadFile | None = None


class DoctorProfileUpdateRequestSchema(DoctorPhoneNumberRequestSchema):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    specialization: str | None = Field(default=None, min_length=1, max_length=100)
    years_experience: int | None = Field(default=None, ge=0, le=80)
    employment_type: DoctorEmploymentTypeEnum | None = None
    avatar: UploadFile | None = None


class DoctorResponseSchema(BaseModel):
    id: int
    user_id: int
    doctor_code: str
    first_name: str
    last_name: str
    email: EmailStr | None = None
    phone_number: str | None = None
    specialization: str
    years_experience: int | None = None
    employment_type: DoctorEmploymentTypeEnum | None = None
    avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DoctorListResponseSchema(BaseModel):
    items: list[DoctorResponseSchema]
    total: int
    page: int
    page_size: int


DoctorSortBy = Literal["name", "specialization", "years_experience", "created_at"]
SortOrder = Literal["asc", "desc"]

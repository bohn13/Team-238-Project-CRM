from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from database import DoctorEmploymentTypeEnum


class DoctorProfileCreateRequestSchema(BaseModel):
    user_id: int = Field(..., ge=1)
    specialization: str = Field(..., min_length=1, max_length=100)
    years_experience: int | None = Field(default=None, ge=0, le=80)
    employment_type: DoctorEmploymentTypeEnum | None = None


class DoctorProfileUpdateRequestSchema(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    phone_number: str | None = Field(default=None, max_length=20)
    specialization: str | None = Field(default=None, min_length=1, max_length=100)
    years_experience: int | None = Field(default=None, ge=0, le=80)
    employment_type: DoctorEmploymentTypeEnum | None = None


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

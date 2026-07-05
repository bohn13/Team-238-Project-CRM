from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from database.models.patient import GenderEnum


class PatientCreateRequestSchema(BaseModel):
    gender: GenderEnum | None = Field(default=None)
    date_of_birth: date | None = Field(default=None)
    address: str | None = Field(default=None, max_length=255)


class PatientUpdateRequestSchema(BaseModel):
    gender: GenderEnum | None = Field(default=None)
    date_of_birth: date | None = Field(default=None)
    address: str | None = Field(default=None, max_length=255)


class PatientResponseSchema(BaseModel):
    patient_id: int
    gender: GenderEnum | None = None
    date_of_birth: date | None = None
    address: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

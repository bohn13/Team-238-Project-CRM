import enum
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator


class PatientGenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class PatientSourceEnum(str, enum.Enum):
    GOOGLE_SEARCH = "google_search"
    SOCIAL_MEDIA = "social_media"
    RECOMMENDATION = "recommendation"
    OUTDOOR_AD = "outdoor_ad"
    WEBSITE = "website"
    OTHER = "other"


class PatientBase(BaseModel):
    gender: PatientGenderEnum | None = None
    date_of_birth: date | None = None
    address: str | None = None
    source: PatientSourceEnum | None = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date | None) -> date | None:
        if value is not None and value > date.today():
            raise ValueError("Date of birth cannot be in the future.")

        return value


class PatientCreate(PatientBase):
    user_id: int


class PatientUpdate(PatientBase):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None


class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None


class PatientListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    first_name: str
    last_name: str
    phone_number: str | None
    date_of_birth: date | None
    source: PatientSourceEnum | None = None
    last_visit_date: datetime | None = None


class PaginatedPatientResponse(BaseModel):
    items: list[PatientListResponse]
    total: int
    page: int
    page_size: int
    pages: int

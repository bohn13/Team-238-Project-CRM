import enum
from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator


class PatientGenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class PatientBase(BaseModel):
    gender: PatientGenderEnum | None = None
    date_of_birth: date | None = None
    address: str | None = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date | None) -> date | None:
        if value is not None and value > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return value


class PatientCreate(PatientBase):
    user_id: int


class PatientUpdate(PatientBase):
    pass


class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class PatientListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    first_name: str
    last_name: str
    phone_number: str | None
    date_of_birth: date | None
    #last_visit_date: date | None = None

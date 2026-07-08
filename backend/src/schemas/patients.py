from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    gender: str | None = None
    date_of_birth: date | None = None
    address: str | None = None


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

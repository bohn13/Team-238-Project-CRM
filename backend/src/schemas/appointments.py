from datetime import datetime

from pydantic import BaseModel, ConfigDict

from database.models.appointments import AppointmentStatusEnum


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date_time: datetime
    duration: int
    reason_for_visit: str | None = None
    status: AppointmentStatusEnum = AppointmentStatusEnum.SCHEDULED


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: int | None = None
    doctor_id: int | None = None
    date_time: datetime | None = None
    duration: int | None = None
    reason_for_visit: str | None = None
    status: AppointmentStatusEnum | None = None


class AppointmentResponse(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

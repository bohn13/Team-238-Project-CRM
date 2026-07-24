from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from database.models.appointments import (
    AppointmentChannelEnum,
    AppointmentStatusEnum,
)


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date_time: datetime
    duration: int = Field(default=30, ge=1)
    reason_for_visit: str | None = None
    status: AppointmentStatusEnum = AppointmentStatusEnum.SCHEDULED
    channel: AppointmentChannelEnum | None = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: int | None = None
    doctor_id: int | None = None
    date_time: datetime | None = None
    duration: int | None = Field(default=None, ge=1)
    reason_for_visit: str | None = None
    status: AppointmentStatusEnum | None = None
    channel: AppointmentChannelEnum | None = None


class AppointmentResponse(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatusEnum

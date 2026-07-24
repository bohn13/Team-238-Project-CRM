from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class AppointmentStatusEnum(str, enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    WAITING = "waiting"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentChannelEnum(str, enum.Enum):
    WALK_IN = "walk_in"
    PHONE_CALL = "phone_call"
    MESSAGE = "message"


class AppointmentModel(Base):
    __tablename__ = "appointments"

    __table_args__ = (
        Index(
            "ix_appointments_doctor_date_time",
            "doctor_id",
            "date_time",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey(
            "patients.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey(
            "doctors.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    duration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
        server_default="30",
    )

    reason_for_visit: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[AppointmentStatusEnum] = mapped_column(
        String(30),
        nullable=False,
        default=AppointmentStatusEnum.SCHEDULED,
    )

    channel: Mapped[AppointmentChannelEnum | None] = mapped_column(
        String(30),
        nullable=True,
    )

    patient = relationship("PatientModel")
    doctor = relationship("DoctorModel")

import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GenderEnum(enum.Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"


class Patient(Base):
    __tablename__ = "patients"

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        primary_key=True,
    )

    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum, name="genders"),
        nullable=True,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )

    #user: Mapped["User"] = relationship(
        #"User",
        #back_populates="patients",
    #)

    #appointments: Mapped[list["Appointment"]] = relationship(
        #"Appointment",
       # back_populates="patients",
    #)

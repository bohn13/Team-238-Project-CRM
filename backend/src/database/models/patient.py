from __future__ import annotations

from datetime import date, datetime
import enum
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class PatientGenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class PatientModel(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    gender: Mapped[PatientGenderEnum | None] = mapped_column(String(20))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    address: Mapped[str | None] = mapped_column(String(255))

    user: Mapped["UserModel"] = relationship(back_populates="patient")

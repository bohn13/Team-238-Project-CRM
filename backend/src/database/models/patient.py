from __future__ import annotations

import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base

if TYPE_CHECKING:
    from database.models.users import UserModel


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
    source: Mapped[PatientSourceEnum | None] = mapped_column(
        String(30),
        nullable=True,
    )

    user: Mapped[UserModel] = relationship(back_populates="patient")

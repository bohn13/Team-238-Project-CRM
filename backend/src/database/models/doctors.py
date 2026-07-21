from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.users import UserModel


class DoctorEmploymentTypeEnum(str, enum.Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


class DoctorModel(Base):
    __tablename__ = "doctors"
    __table_args__ = (UniqueConstraint("user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    specialization: Mapped[str] = mapped_column(String(100), nullable=False)
    years_experience: Mapped[int | None] = mapped_column(Integer)
    employment_type: Mapped[DoctorEmploymentTypeEnum | None] = mapped_column(String(20))
    avatar_url: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[UserModel] = relationship(back_populates="doctor_profile")

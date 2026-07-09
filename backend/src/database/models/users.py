from __future__ import annotations

import enum
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from database.models.base import Base
from database.validators import users as validators
from security.passwords import hash_password, verify_password
from security.utils import generate_secure_token

if TYPE_CHECKING:
    from database.models.doctors import DoctorModel


class UserRoleEnum(str, enum.Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    DOCTOR = "doctor"
    MANAGER = "manager"
    PATIENT = "patient"
    USER = "user"


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[UserRoleEnum] = mapped_column(String(20), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True)
    email: Mapped[str | None] = mapped_column(String(50), unique=True)
    _password_hash: Mapped[str | None] = mapped_column("password_hash", String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    source: Mapped[str | None] = mapped_column(String(30))

    activation_token: Mapped[ActivationTokenModel | None] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    password_reset_token: Mapped[PasswordResetTokenModel | None] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    refresh_tokens: Mapped[list[RefreshTokenModel]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    doctor_profile: Mapped[DoctorModel | None] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @classmethod
    def create(
        cls,
        email: str,
        raw_password: str,
        first_name: str,
        last_name: str,
        role: UserRoleEnum = UserRoleEnum.USER,
        source: str = "website",
    ) -> UserModel:
        user = cls(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            source=source,
        )
        user.password = raw_password
        return user

    @property
    def password(self) -> None:
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, raw_password: str) -> None:
        validators.validate_password_strength(raw_password)
        self._password_hash = hash_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        if self._password_hash is None:
            return False
        return verify_password(raw_password, self._password_hash)

    @validates("email")
    def validate_email(self, key: str, value: str | None) -> str | None:
        if value is None:
            return value
        return validators.validate_email(value.lower())


class TokenBaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(
        String(64), unique=True, default=generate_secure_token
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


class ActivationTokenModel(TokenBaseModel):
    __tablename__ = "activation_tokens"
    __table_args__ = (UniqueConstraint("user_id"),)

    user: Mapped[UserModel] = relationship(back_populates="activation_token")


class PasswordResetTokenModel(TokenBaseModel):
    __tablename__ = "password_reset_tokens"
    __table_args__ = (UniqueConstraint("user_id"),)

    user: Mapped[UserModel] = relationship(back_populates="password_reset_token")


class RefreshTokenModel(TokenBaseModel):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(String(512), unique=True)
    user: Mapped[UserModel] = relationship(back_populates="refresh_tokens")

    @classmethod
    def create(cls, user_id: int, days_valid: int, token: str) -> RefreshTokenModel:
        expires_at = datetime.now(timezone.utc) + timedelta(days=days_valid)
        return cls(user_id=user_id, expires_at=expires_at, token=token)

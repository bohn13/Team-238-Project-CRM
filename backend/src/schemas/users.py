from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from database import users_validators
from database.models.users import UserRoleEnum

CREDENTIALS_EXAMPLE = {"email": "doctor@example.com", "password": "StrongPassword123!"}


class BaseEmailPasswordSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": CREDENTIALS_EXAMPLE},
    )

    email: EmailStr = Field(..., description="User email address.")
    password: str = Field(..., min_length=8, description="User password.")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return value.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return users_validators.validate_password_strength(value)


class UserRegistrationRequestSchema(BaseEmailPasswordSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **CREDENTIALS_EXAMPLE,
                "first_name": "Andrii",
                "last_name": "Yarotskyi",
            }
        },
    )

    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str | None = Field(
        default=None,
        pattern=users_validators.PHONE_NUMBER_PATTERN,
        description=(
            "Phone number in international E.164 format. Spaces, parentheses, "
            "and hyphens are removed before validation."
        ),
        examples=["+380501112233"],
    )
    source: str | None = Field(default="website", max_length=30)

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_phone_number(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        return users_validators.normalize_phone_number(value)


class UserRegistrationResponseSchema(BaseModel):
    id: int = Field(..., description="Created user ID.")
    email: EmailStr = Field(..., description="Registered email address.")

    model_config = ConfigDict(from_attributes=True)


class UserActivationRequestSchema(BaseModel):
    email: EmailStr = Field(..., description="Registered user email.")
    token: str = Field(..., description="Activation token from email.")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return value.lower()


class PasswordResetRequestSchema(BaseModel):
    email: EmailStr = Field(..., description="Email used for account registration.")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return value.lower()


class PasswordResetCompleteRequestSchema(BaseEmailPasswordSchema):
    token: str = Field(..., description="Password reset token from email.")


class UserLoginRequestSchema(BaseEmailPasswordSchema):
    pass


class UserLoginResponseSchema(BaseModel):
    access_token: str = Field(..., description="Short-lived JWT access token.")
    refresh_token: str = Field(..., description="Long-lived JWT refresh token.")
    token_type: str = Field(default="bearer", description="Authorization token type.")


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str = Field(..., description="Valid JWT refresh token.")


class TokenRefreshResponseSchema(BaseModel):
    access_token: str = Field(..., description="New JWT access token.")
    token_type: str = Field(default="bearer", description="Authorization token type.")


class UserRoleUpdateRequestSchema(BaseModel):
    role: UserRoleEnum = Field(..., description="Target user role.")


class CurrentUserResponseSchema(BaseModel):
    id: int
    role: UserRoleEnum
    first_name: str
    last_name: str
    phone_number: str | None = None
    email: EmailStr | None = None
    registration_date: datetime
    source: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserItemResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr | None = None

    model_config = ConfigDict(from_attributes=True)


class MessageResponseSchema(BaseModel):
    message: str = Field(..., description="Operation result message.")

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from database import users_validators
from database.models.users import UserGroupEnum


class BaseEmailPasswordSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "doctor@example.com",
                "password": "StrongPassword123!",
            }
        },
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
    pass


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
    group: UserGroupEnum = Field(..., description="Target user role.")


class MessageResponseSchema(BaseModel):
    message: str = Field(..., description="Operation result message.")

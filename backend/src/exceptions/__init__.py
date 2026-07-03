from exceptions.email import BaseEmailError
from exceptions.security import BaseSecurityError, InvalidTokenError, TokenExpiredError
from exceptions.storage import BaseS3StorageError, S3ConnectionError, S3FileUploadError
from exceptions.auth import (
    AuthServiceError,
    DatabaseWriteError,
    LastAdminDemotionError,
    UserAlreadyExistsError,
    ActiveActivationTokenError,
    DefaultUserGroupNotFoundError,
    InvalidActivationTokenError,
    UserAlreadyActiveError,
    InvalidPasswordResetTokenError,
    InvalidCredentialsError,
    InactiveUserError,
    RefreshTokenNotFoundError,
    UserNotFoundError,
    RoleNotFoundError,
    SettingSuperAdminRoleError
)

__all__ = [
    "BaseEmailError",
    "BaseS3StorageError",
    "BaseSecurityError",
    "InvalidTokenError",
    "S3ConnectionError",
    "S3FileUploadError",
    "TokenExpiredError",
    "AuthServiceError",
    "DatabaseWriteError",
    "LastAdminDemotionError",
    "UserAlreadyExistsError",
    "ActiveActivationTokenError",
    "DefaultUserGroupNotFoundError",
    "InvalidActivationTokenError",
    "UserAlreadyActiveError",
    "InvalidPasswordResetTokenError",
    "InvalidCredentialsError",
    "InactiveUserError",
    "RefreshTokenNotFoundError",
    "UserNotFoundError",
    "RoleNotFoundError",
    "SettingSuperAdminRoleError",
]

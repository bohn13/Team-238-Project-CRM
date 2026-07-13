from exceptions.email import BaseEmailError
from exceptions.security import BaseSecurityError, InvalidTokenError, TokenExpiredError
from exceptions.storage import BaseS3StorageError, S3ConnectionError, S3FileUploadError
from exceptions.auth import (
    AuthServiceError,
    DatabaseWriteError,
    LastAdminDemotionError,
    UserAlreadyExistsError,
    ActiveActivationTokenError,
    InvalidActivationTokenError,
    InvalidPasswordResetTokenError,
    InvalidCredentialsError,
    RefreshTokenNotFoundError,
    UserNotFoundError,
    SettingSuperAdminRoleError,
)
from exceptions.doctors import (
    DoctorProfileAlreadyExistsError,
    DoctorProfileNotFoundError,
    DoctorProfilePermissionError,
    DoctorServiceError,
    InvalidDoctorAvatarError,
    InvalidDoctorProfileUserError,
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
    "InvalidActivationTokenError",
    "InvalidPasswordResetTokenError",
    "InvalidCredentialsError",
    "RefreshTokenNotFoundError",
    "UserNotFoundError",
    "SettingSuperAdminRoleError",
    "DoctorProfileAlreadyExistsError",
    "DoctorProfileNotFoundError",
    "DoctorProfilePermissionError",
    "DoctorServiceError",
    "InvalidDoctorAvatarError",
    "InvalidDoctorProfileUserError",
]

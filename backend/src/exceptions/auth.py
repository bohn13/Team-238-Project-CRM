from datetime import datetime


class AuthServiceError(Exception):
    status_code = 400
    detail = "Authentication service error."


class UserAlreadyExistsError(AuthServiceError):
    status_code = 409

    def __init__(self, email: str):
        self.detail = f"A user with this email {email} already exists."


class ActiveActivationTokenError(AuthServiceError):
    status_code = 409

    def __init__(self, expires_at: datetime):
        self.detail = (
            "You already have an active activation link. You can request a new one "
            f"after {expires_at.strftime('%d %b %Y, %I:%M:%S %p')} UTC."
        )


class DefaultUserGroupNotFoundError(AuthServiceError):
    status_code = 500
    detail = "Default user group not found."


class InvalidActivationTokenError(AuthServiceError):
    status_code = 400
    detail = "Invalid or expired activation token."


class UserAlreadyActiveError(AuthServiceError):
    status_code = 400
    detail = "User account is already active."


class InvalidPasswordResetTokenError(AuthServiceError):
    status_code = 400
    detail = "Invalid email or token."


class InvalidCredentialsError(AuthServiceError):
    status_code = 401
    detail = "Invalid email or password."


class InactiveUserError(AuthServiceError):
    status_code = 403
    detail = "User account is not activated."


class RefreshTokenNotFoundError(AuthServiceError):
    status_code = 401
    detail = "Refresh token not found."


class UserNotFoundError(AuthServiceError):
    status_code = 404
    detail = "User not found."


class RoleNotFoundError(AuthServiceError):
    status_code = 400
    detail = "Requested role does not exist."


class LastAdminDemotionError(AuthServiceError):
    status_code = 400
    detail = "Cannot demote the last admin user."


class DatabaseWriteError(AuthServiceError):
    status_code = 500

    def __init__(self, detail: str):
        self.detail = detail


class SettingSuperAdminRoleError(AuthServiceError):
    status_code = 403
    detail = "You do not have permission to perform this action."

class BaseSecurityError(Exception):
    pass


class TokenExpiredError(BaseSecurityError):
    def __str__(self) -> str:
        return "Token has expired."


class InvalidTokenError(BaseSecurityError):
    def __str__(self) -> str:
        return "Invalid token."

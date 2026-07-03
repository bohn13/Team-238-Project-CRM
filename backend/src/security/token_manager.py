from datetime import datetime, timedelta, timezone

import jwt

from exceptions import InvalidTokenError, TokenExpiredError
from security.interfaces import JWTAuthManagerInterface


class JWTAuthManager(JWTAuthManagerInterface):
    def __init__(
        self,
        secret_key_access: str,
        secret_key_refresh: str,
        algorithm: str,
        access_token_expire_minutes: int,
        refresh_token_expire_days: int,
    ):
        self._secret_key_access = secret_key_access
        self._secret_key_refresh = secret_key_refresh
        self._algorithm = algorithm
        self._access_token_expire_minutes = access_token_expire_minutes
        self._refresh_token_expire_days = refresh_token_expire_days

    def _create_token(
        self, data: dict, secret_key: str, expires_delta: timedelta
    ) -> str:
        to_encode = data.copy()
        to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
        return jwt.encode(to_encode, secret_key, algorithm=self._algorithm)

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        return self._create_token(
            data,
            self._secret_key_access,
            expires_delta or timedelta(minutes=self._access_token_expire_minutes),
        )

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        return self._create_token(
            data,
            self._secret_key_refresh,
            expires_delta or timedelta(days=self._refresh_token_expire_days),
        )

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, self._secret_key_access, algorithms=[self._algorithm]
            )
        except jwt.ExpiredSignatureError as error:
            raise TokenExpiredError from error
        except jwt.InvalidTokenError as error:
            raise InvalidTokenError from error

    def decode_refresh_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, self._secret_key_refresh, algorithms=[self._algorithm]
            )
        except jwt.ExpiredSignatureError as error:
            raise TokenExpiredError from error
        except jwt.InvalidTokenError as error:
            raise InvalidTokenError from error

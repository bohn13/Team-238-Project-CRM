import pytest

from database.validators.users import validate_password_strength
from exceptions import InvalidTokenError
from security.passwords import hash_password, verify_password
from security.token_manager import JWTAuthManager


def test_password_hash_round_trip() -> None:
    password = "StrongPassword123!"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("WrongPassword123!", hashed_password)


@pytest.mark.parametrize(
    "password",
    [
        "short1!",
        "lowercase123!",
        "UPPERCASE123!",
        "NoDigits!",
        "NoSpecial123",
    ],
)
def test_password_strength_rejects_weak_passwords(password: str) -> None:
    with pytest.raises(ValueError):
        validate_password_strength(password)


def test_jwt_manager_rejects_refresh_token_as_access_token() -> None:
    manager = JWTAuthManager(
        secret_key_access="access-secret-with-at-least-32-bytes",
        secret_key_refresh="refresh-secret-with-at-least-32-bytes",
        algorithm="HS256",
        access_token_expire_minutes=60,
        refresh_token_expire_days=7,
    )
    refresh_token = manager.create_refresh_token({"user_id": 1})

    with pytest.raises(InvalidTokenError):
        manager.decode_access_token(refresh_token)

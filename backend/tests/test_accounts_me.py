from datetime import datetime, timezone

from fastapi.testclient import TestClient

from database import UserModel, UserRoleEnum
from main import app
from security.auth import get_current_user


def test_get_current_user_profile_returns_authenticated_user() -> None:
    user = UserModel(
        id=1,
        role=UserRoleEnum.DOCTOR,
        first_name="Ivan",
        last_name="Petrenko",
        phone_number="+380501112233",
        email="doctor@example.com",
        registration_date=datetime(2026, 7, 3, tzinfo=timezone.utc),
        source="website",
    )

    async def override_get_current_user() -> UserModel:
        return user

    app.dependency_overrides[get_current_user] = override_get_current_user
    try:
        response = TestClient(app).get("/accounts/users/me")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "role": "doctor",
        "first_name": "Ivan",
        "last_name": "Petrenko",
        "phone_number": "+380501112233",
        "email": "doctor@example.com",
        "registration_date": "2026-07-03T00:00:00Z",
        "source": "website",
    }


def test_get_current_user_profile_requires_authorization() -> None:
    response = TestClient(app).get("/accounts/users/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authorization header is missing."}

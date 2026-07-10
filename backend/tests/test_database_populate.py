from pathlib import Path

import pytest

from database.models.doctors import DoctorEmploymentTypeEnum
from database.models.users import UserRoleEnum
from database.populate import (
    DEFAULT_PASSWORD,
    _bool_or_default,
    _parse_user,
    _read_csv,
)


def test_parse_user_row_normalizes_email_and_uses_default_password() -> None:
    row = _parse_user(
        {
            "email": " Doctor@Example.COM ",
            "first_name": " Ivan ",
            "last_name": " Petrenko ",
            "role": "doctor",
            "phone_number": "",
            "is_active": "",
        },
        DEFAULT_PASSWORD,
        UserRoleEnum.USER,
        path=Path("users.csv"),
        line=2,
    )

    assert row.email == "doctor@example.com"
    assert row.first_name == "Ivan"
    assert row.last_name == "Petrenko"
    assert row.password == DEFAULT_PASSWORD
    assert row.role == UserRoleEnum.DOCTOR
    assert row.phone_number is None
    assert row.is_active is True


def test_parse_user_row_rejects_unknown_role() -> None:
    with pytest.raises(ValueError, match="invalid 'role' value"):
        _parse_user(
            {
                "email": "user@example.com",
                "first_name": "Ivan",
                "last_name": "Petrenko",
                "role": "owner",
            },
            DEFAULT_PASSWORD,
            UserRoleEnum.USER,
            path=Path("users.csv"),
            line=2,
        )


def test_optional_bool_parses_common_csv_values() -> None:
    assert _bool_or_default("yes", default=False) is True
    assert _bool_or_default("0", default=True) is False
    assert _bool_or_default("", default=True) is True


def test_read_csv_strips_utf8_bom_and_cell_values(tmp_path: Path) -> None:
    csv_path = tmp_path / "users.csv"
    csv_path.write_text(
        "\ufeffemail,first_name,last_name\n user@example.com , Ivan , Petrenko \n",
        encoding="utf-8",
    )

    rows = list(_read_csv(csv_path))

    assert rows == [
        (
            2,
            {
                "email": "user@example.com",
                "first_name": "Ivan",
                "last_name": "Petrenko",
            },
        )
    ]


def test_doctor_employment_enum_values_match_seed_contract() -> None:
    assert DoctorEmploymentTypeEnum("full_time") == DoctorEmploymentTypeEnum.FULL_TIME

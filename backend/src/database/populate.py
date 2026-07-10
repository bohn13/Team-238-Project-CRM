from __future__ import annotations

import argparse
import asyncio
import csv
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.doctors import DoctorEmploymentTypeEnum, DoctorModel
from database.models.users import UserModel, UserRoleEnum
from database.session_postgresql import AsyncPostgresqlSessionLocal
from security.passwords import hash_password

SEED_SOURCE = "seed"
DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "seed_data"
DEFAULT_PASSWORD = "SeedPassword123!"
DEFAULT_BATCH_SIZE = 1_000


@dataclass(frozen=True)
class SeedResult:
    saved: int = 0
    skipped: int = 0


@dataclass(frozen=True)
class UserSeedRow:
    email: str
    first_name: str
    last_name: str
    password: str
    role: UserRoleEnum
    phone_number: str | None
    is_active: bool

    def to_insert_values(self) -> dict:
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "password_hash": hash_password(self.password),
            "role": self.role,
            "source": SEED_SOURCE,
            "is_active": self.is_active,
        }


@dataclass(frozen=True)
class DoctorSeedRow:
    user: UserSeedRow
    specialization: str
    years_experience: int | None
    employment_type: DoctorEmploymentTypeEnum | None
    avatar_url: str | None

    def to_insert_values(self, user_id: int) -> dict:
        return {
            "user_id": user_id,
            "specialization": self.specialization,
            "years_experience": self.years_experience,
            "employment_type": self.employment_type,
            "avatar_url": self.avatar_url,
        }


class DatabasePopulator:
    """Seed fake data from CSV files without deleting real records."""

    def __init__(
        self,
        session: AsyncSession,
        data_dir: Path = DEFAULT_DATA_DIR,
        *,
        batch_size: int = DEFAULT_BATCH_SIZE,
        default_password: str = DEFAULT_PASSWORD,
        update_existing: bool = False,
    ) -> None:
        self.session = session
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.default_password = default_password
        self.update_existing = update_existing

    async def populate(self) -> None:
        users = await self.seed_users()
        doctors = await self.seed_doctors()
        await self.session.commit()
        print(
            "Seed completed: "
            f"users_saved={users.saved}, users_skipped={users.skipped}, "
            f"doctors_saved={doctors.saved}, doctors_skipped={doctors.skipped}"
        )

    async def seed_users(self) -> SeedResult:
        return await self._save_users(self._load_users())

    async def seed_doctors(self) -> SeedResult:
        doctor_rows = self._load_doctors()
        if not doctor_rows:
            return SeedResult()

        user_result = await self._save_users([row.user for row in doctor_rows])
        users_by_email = await self._get_seed_users_by_email(
            [row.user.email for row in doctor_rows]
        )

        values = []
        skipped = user_result.skipped
        for row in doctor_rows:
            user = users_by_email.get(row.user.email)
            if user is None:
                skipped += 1
                continue
            values.append(row.to_insert_values(user.id))

        saved = await self._save_doctor_values(values)
        return SeedResult(saved=saved, skipped=skipped)

    async def _save_users(self, rows: Sequence[UserSeedRow]) -> SeedResult:
        saved = 0
        skipped = 0

        for batch in _chunks(rows, self.batch_size):
            existing_users = await self._get_existing_users(batch)
            values = []

            for row in batch:
                if _should_skip_user(row, existing_users):
                    skipped += 1
                    continue
                values.append(row.to_insert_values())

            saved += await self._save_user_values(values)

        return SeedResult(saved=saved, skipped=skipped)

    async def _save_user_values(self, values: list[dict]) -> int:
        if not values:
            return 0

        stmt = insert(UserModel).values(values)
        if self.update_existing:
            stmt = stmt.on_conflict_do_update(
                index_elements=[UserModel.email],
                set_={
                    "first_name": stmt.excluded.first_name,
                    "last_name": stmt.excluded.last_name,
                    "phone_number": stmt.excluded.phone_number,
                    "password_hash": stmt.excluded.password_hash,
                    "role": stmt.excluded.role,
                    "is_active": stmt.excluded.is_active,
                },
                where=UserModel.source == SEED_SOURCE,
            )
        else:
            stmt = stmt.on_conflict_do_nothing(index_elements=[UserModel.email])

        result = await self.session.execute(stmt)
        return result.rowcount or 0

    async def _save_doctor_values(self, values: list[dict]) -> int:
        if not values:
            return 0

        stmt = insert(DoctorModel).values(values)
        if self.update_existing:
            stmt = stmt.on_conflict_do_update(
                index_elements=[DoctorModel.user_id],
                set_={
                    "specialization": stmt.excluded.specialization,
                    "years_experience": stmt.excluded.years_experience,
                    "employment_type": stmt.excluded.employment_type,
                    "avatar_url": stmt.excluded.avatar_url,
                },
            )
        else:
            stmt = stmt.on_conflict_do_nothing(index_elements=[DoctorModel.user_id])

        result = await self.session.execute(stmt)
        return result.rowcount or 0

    async def _get_existing_users(self, rows: Sequence[UserSeedRow]) -> list[UserModel]:
        emails = {row.email for row in rows}
        phone_numbers = {row.phone_number for row in rows if row.phone_number}

        result = await self.session.execute(
            select(UserModel).where(
                (UserModel.email.in_(emails))
                | (UserModel.phone_number.in_(phone_numbers))
            )
        )
        return list(result.scalars().all())

    async def _get_seed_users_by_email(
        self, emails: Sequence[str]
    ) -> dict[str, UserModel]:
        result = await self.session.execute(
            select(UserModel).where(
                UserModel.email.in_(set(emails)),
                UserModel.source == SEED_SOURCE,
            )
        )
        return {user.email: user for user in result.scalars().all() if user.email}

    def _load_users(self) -> list[UserSeedRow]:
        path = self.data_dir / "users.csv"
        return [
            _parse_user(row, self.default_password, UserRoleEnum.USER, path, line)
            for line, row in _read_csv(path)
        ]

    def _load_doctors(self) -> list[DoctorSeedRow]:
        path = self.data_dir / "doctors.csv"
        doctors = []

        for line, row in _read_csv(path):
            user = _parse_user(
                row, self.default_password, UserRoleEnum.DOCTOR, path, line
            )
            doctors.append(
                DoctorSeedRow(
                    user=user,
                    specialization=_required(row, "specialization", path, line),
                    years_experience=_int_or_none(row.get("years_experience")),
                    employment_type=_enum_or_none(
                        row.get("employment_type"),
                        DoctorEmploymentTypeEnum,
                        "employment_type",
                        path,
                        line,
                    ),
                    avatar_url=_blank_to_none(row.get("avatar_url")),
                )
            )

        return doctors


def _should_skip_user(row: UserSeedRow, existing_users: Sequence[UserModel]) -> bool:
    for user in existing_users:
        same_email = user.email == row.email
        same_phone = row.phone_number and user.phone_number == row.phone_number

        if same_email and user.source != SEED_SOURCE:
            return True
        if same_phone and user.email != row.email:
            return True

    return False


def _parse_user(
    row: dict[str, str],
    default_password: str,
    default_role: UserRoleEnum,
    path: Path,
    line: int,
) -> UserSeedRow:
    role = _enum_or_none(row.get("role"), UserRoleEnum, "role", path, line)
    return UserSeedRow(
        email=_required(row, "email", path, line).lower(),
        first_name=_required(row, "first_name", path, line),
        last_name=_required(row, "last_name", path, line),
        password=_blank_to_none(row.get("password")) or default_password,
        role=role or default_role,
        phone_number=_blank_to_none(row.get("phone_number")),
        is_active=_bool_or_default(row.get("is_active"), default=True),
    )


def _read_csv(path: Path) -> Iterator[tuple[int, dict[str, str]]]:
    if not path.exists():
        return

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        for line, row in enumerate(reader, start=2):
            yield line, {key: value.strip() for key, value in row.items() if key}


def _required(row: dict[str, str], field: str, path: Path, line: int) -> str:
    value = _blank_to_none(row.get(field))
    if value is None:
        raise ValueError(f"{path}:{line} missing required field '{field}'.")
    return value


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _int_or_none(value: str | None) -> int | None:
    value = _blank_to_none(value)
    return int(value) if value is not None else None


def _bool_or_default(value: str | None, *, default: bool) -> bool:
    value = _blank_to_none(value)
    if value is None:
        return default
    if value.lower() in {"1", "true", "yes", "y"}:
        return True
    if value.lower() in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}.")


def _enum_or_none(
    value: str | None,
    enum_class: type[UserRoleEnum] | type[DoctorEmploymentTypeEnum],
    field: str,
    path: Path,
    line: int,
) -> UserRoleEnum | DoctorEmploymentTypeEnum | None:
    value = _blank_to_none(value)
    if value is None:
        return None

    try:
        return enum_class(value.lower())
    except ValueError as error:
        allowed = ", ".join(item.value for item in enum_class)
        raise ValueError(
            f"{path}:{line} invalid '{field}' value {value!r}. Allowed: {allowed}."
        ) from error


def _chunks[T](items: Sequence[T], size: int) -> Iterator[Sequence[T]]:
    if size < 1:
        raise ValueError("batch_size must be greater than zero.")

    for index in range(0, len(items), size):
        yield items[index : index + size]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed fake database data from CSV.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--default-password", default=DEFAULT_PASSWORD)
    parser.add_argument(
        "--update-existing",
        action="store_true",
        help="Update rows previously created by this seed command.",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    async with AsyncPostgresqlSessionLocal() as session:
        populator = DatabasePopulator(
            session=session,
            data_dir=args.data_dir,
            batch_size=args.batch_size,
            default_password=args.default_password,
            update_existing=args.update_existing,
        )
        await populator.populate()


if __name__ == "__main__":
    asyncio.run(main())

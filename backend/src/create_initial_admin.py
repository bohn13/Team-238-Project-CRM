import argparse
import asyncio
import socket
from getpass import getpass

from sqlalchemy.exc import SQLAlchemyError

from database import UserModel, UserRoleEnum
from database.session_postgresql import AsyncPostgresqlSessionLocal
from repositories.users import UserRepository


async def create_initial_admin(email: str) -> None:
    normalized_email = email.strip().lower()
    if not normalized_email:
        raise ValueError("Email is required.")

    password = getpass("Superadmin password: ")
    password_confirm = getpass("Confirm superadmin password: ")
    if not password:
        raise ValueError("Password cannot be empty.")
    if password != password_confirm:
        raise ValueError("Passwords do not match.")

    async with AsyncPostgresqlSessionLocal() as session:
        users = UserRepository(session)
        existing_superadmins = await users.count_users_with_role(UserRoleEnum.SUPERADMIN)
        if existing_superadmins:
            raise RuntimeError(
                "Superadmin already exists. Use superadmin role-change endpoint instead."
            )

        existing_user = await users.get_by_email(normalized_email)
        if existing_user:
            existing_user.role = UserRoleEnum.SUPERADMIN
            existing_user.password = password
        else:
            superadmin = UserModel.create(
                email=normalized_email,
                raw_password=password,
                first_name="Initial",
                last_name="Superadmin",
                role=UserRoleEnum.SUPERADMIN,
                source="admin_created",
            )
            users.add_user(superadmin)

        await session.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create first superadmin user.")
    parser.add_argument("--email", required=True, help="Superadmin email")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        asyncio.run(create_initial_admin(email=args.email))
    except (SQLAlchemyError, socket.gaierror) as error:
        raise RuntimeError(
            "Database connection failed. Check POSTGRES_HOST/POSTGRES_DB_PORT/"
            "POSTGRES_USER/POSTGRES_PASSWORD in your .env file and make sure "
            "the database container/service is running."
        ) from error
    print("Initial superadmin user is ready.")


if __name__ == "__main__":
    main()

from datetime import datetime, timezone

from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import (
    ActivationTokenModel,
    PasswordResetTokenModel,
    RefreshTokenModel,
    UserModel,
    UserRoleEnum,
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def as_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> UserModel | None:
        return await self.session.scalar(
            select(UserModel).where(UserModel.email == email)
        )

    async def get_by_email_with_activation_token(self, email: str) -> UserModel | None:
        return await self.session.scalar(
            select(UserModel)
            .options(joinedload(UserModel.activation_token))
            .where(UserModel.email == email)
        )

    async def get_by_id(self, user_id: int) -> UserModel | None:
        return await self.session.scalar(
            select(UserModel).where(UserModel.id == user_id)
        )

    async def get_current_by_id(self, user_id: int) -> UserModel | None:
        return await self.session.scalar(
            select(UserModel).where(UserModel.id == user_id)
        )

    async def count_users_with_role(self, role: UserRoleEnum) -> int:
        result = await self.session.scalar(
            select(func.count(UserModel.id)).where(UserModel.role == role)
        )
        return int(result or 0)

    def add_user(self, user: UserModel) -> None:
        self.session.add(user)

    def add_activation_token(self, token: ActivationTokenModel) -> None:
        self.session.add(token)

    def add_password_reset_token(self, token: PasswordResetTokenModel) -> None:
        self.session.add(token)

    def add_refresh_token(self, token: RefreshTokenModel) -> None:
        self.session.add(token)

    async def flush(self) -> None:
        await self.session.flush()

    async def delete_activation_token(self, token: ActivationTokenModel) -> None:
        await self.session.delete(token)

    async def delete_password_reset_token(self, token: PasswordResetTokenModel) -> None:
        await self.session.delete(token)

    async def delete_password_reset_tokens_for_user(self, user_id: int) -> None:
        await self.session.execute(
            delete(PasswordResetTokenModel).where(
                PasswordResetTokenModel.user_id == user_id
            )
        )

    async def get_activation_token(
        self, email: str, token: str
    ) -> ActivationTokenModel | None:
        return await self.session.scalar(
            select(ActivationTokenModel)
            .options(joinedload(ActivationTokenModel.user))
            .join(UserModel)
            .where(UserModel.email == email, ActivationTokenModel.token == token)
        )

    async def get_password_reset_token_for_user(
        self, user_id: int
    ) -> PasswordResetTokenModel | None:
        return await self.session.scalar(
            select(PasswordResetTokenModel).where(
                PasswordResetTokenModel.user_id == user_id
            )
        )

    async def get_refresh_token(self, token: str) -> RefreshTokenModel | None:
        return await self.session.scalar(
            select(RefreshTokenModel).where(RefreshTokenModel.token == token)
        )

    async def delete_refresh_token(
        self, refresh_token_record: RefreshTokenModel
    ) -> None:
        await self.session.delete(refresh_token_record)

    async def list(self, search: str | None) -> list[UserModel]:
        stmt = select(UserModel).where(
            (UserModel.is_active.is_(True)) & (UserModel.role == UserRoleEnum.USER)
        )

        search_term = search.strip() if search else None
        if search_term:
            pattern = f"%{search_term}%"

            stmt = stmt.where(
                or_(
                    UserModel.email.ilike(pattern),
                    UserModel.first_name.ilike(pattern),
                    UserModel.last_name.ilike(pattern),
                )
            )
        stmt = stmt.order_by(
            UserModel.registration_date.desc(),
            UserModel.id.desc(),
        ).limit(10)

        result = await self.session.scalars(stmt)
        return list(result)

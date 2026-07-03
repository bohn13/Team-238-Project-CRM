from datetime import datetime, timezone

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import (
    ActivationTokenModel,
    PasswordResetTokenModel,
    RefreshTokenModel,
    UserGroupEnum,
    UserGroupModel,
    UserModel,
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

    async def get_active_with_group(self, user_id: int) -> UserModel | None:
        return await self.session.scalar(
            select(UserModel)
            .options(joinedload(UserModel.group))
            .where(UserModel.id == user_id, UserModel.is_active.is_(True))
        )

    async def get_group_by_name(
        self, group_name: UserGroupEnum
    ) -> UserGroupModel | None:
        return await self.session.scalar(
            select(UserGroupModel).where(UserGroupModel.name == group_name)
        )

    async def get_group_by_id(self, group_id: int) -> UserGroupModel | None:
        return await self.session.scalar(
            select(UserGroupModel).where(UserGroupModel.id == group_id)
        )

    async def count_users_in_group(self, group_id: int) -> int:
        result = await self.session.scalar(
            select(func.count(UserModel.id)).where(UserModel.group_id == group_id)
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

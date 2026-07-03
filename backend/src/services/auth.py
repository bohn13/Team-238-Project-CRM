from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from database import (
    ActivationTokenModel,
    PasswordResetTokenModel,
    RefreshTokenModel,
    UserGroupEnum,
    UserModel,
)
from exceptions import (
    UserAlreadyExistsError,
    DefaultUserGroupNotFoundError,
    ActiveActivationTokenError,
    DatabaseWriteError,
    InvalidActivationTokenError,
    UserAlreadyActiveError,
    InvalidPasswordResetTokenError,
    InvalidCredentialsError,
    InactiveUserError,
    RefreshTokenNotFoundError,
    UserNotFoundError,
    RoleNotFoundError,
    LastAdminDemotionError,
    SettingSuperAdminRoleError,
)
from notifications import EmailSenderInterface
from repositories.users import UserRepository, as_aware_utc, utc_now
from security.interfaces import JWTAuthManagerInterface


@dataclass(frozen=True)
class LoginResult:
    access_token: str
    refresh_token: str


class AuthService:
    password_reset_message = (
        "If you are registered, you will receive an email with instructions."
    )

    def __init__(
        self,
        session: AsyncSession,
        settings: Settings,
        jwt_manager: JWTAuthManagerInterface,
        email_sender: EmailSenderInterface,
    ):
        self.session = session
        self.settings = settings
        self.jwt_manager = jwt_manager
        self.email_sender = email_sender
        self.users = UserRepository(session)

    async def register_user(self, email: str, password: str) -> UserModel:
        user = await self.users.get_by_email_with_activation_token(email)
        if user and user.is_active:
            raise UserAlreadyExistsError(email)

        user_group = await self.users.get_group_by_name(UserGroupEnum.DOCTOR)
        if not user_group:
            raise DefaultUserGroupNotFoundError

        try:
            if user is None:
                user = UserModel.create(
                    email=email,
                    raw_password=password,
                    group_id=user_group.id,
                )
                self.users.add_user(user)
                await self.users.flush()
            elif user.activation_token:
                expires_at = as_aware_utc(user.activation_token.expires_at)
                if utc_now() < expires_at:
                    raise ActiveActivationTokenError(expires_at)
                await self.users.delete_activation_token(user.activation_token)
                await self.users.flush()

            activation_token = ActivationTokenModel(user_id=user.id)
            self.users.add_activation_token(activation_token)
            await self.session.commit()
            await self.session.refresh(user)
        except ActiveActivationTokenError:
            raise
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred during user creation."
            ) from error

        activation_link = (
            f"{self.settings.FRONTEND_BASE_URL}/accounts/activate/"
            f"?token={activation_token.token}"
        )
        await self.email_sender.send_activation_email(user.email, activation_link)
        return user

    async def activate_account(self, email: str, token: str) -> str:
        token_record = await self.users.get_activation_token(email, token)
        if not token_record or as_aware_utc(token_record.expires_at) < utc_now():
            if token_record:
                await self.users.delete_activation_token(token_record)
                await self.session.commit()
            raise InvalidActivationTokenError

        user = token_record.user
        if user.is_active:
            raise UserAlreadyActiveError

        user.is_active = True
        await self.users.delete_activation_token(token_record)
        await self.session.commit()

        login_link = f"{self.settings.FRONTEND_BASE_URL}/accounts/login/"
        await self.email_sender.send_activation_complete_email(email, login_link)
        return "User account activated successfully."

    async def request_password_reset_token(self, email: str) -> str:
        user = await self.users.get_by_email(email)
        if not user or not user.is_active:
            return self.password_reset_message

        await self.users.delete_password_reset_tokens_for_user(user.id)
        reset_token = PasswordResetTokenModel(user_id=user.id)
        self.users.add_password_reset_token(reset_token)
        await self.session.commit()

        reset_link = (
            f"{self.settings.FRONTEND_BASE_URL}/accounts/reset-password/complete/"
            f"?token={reset_token.token}"
        )
        await self.email_sender.send_password_reset_email(email, reset_link)
        return self.password_reset_message

    async def reset_password(self, email: str, token: str, password: str) -> str:
        user = await self.users.get_by_email(email)
        if not user or not user.is_active:
            raise InvalidPasswordResetTokenError

        token_record = await self.users.get_password_reset_token_for_user(user.id)
        if not token_record or token_record.token != token:
            if token_record:
                await self.users.delete_password_reset_token(token_record)
                await self.session.commit()
            raise InvalidPasswordResetTokenError

        if as_aware_utc(token_record.expires_at) < utc_now():
            await self.users.delete_password_reset_token(token_record)
            await self.session.commit()
            raise InvalidPasswordResetTokenError

        try:
            user.password = password
            await self.users.delete_password_reset_token(token_record)
            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while resetting the password."
            ) from error

        login_link = f"{self.settings.FRONTEND_BASE_URL}/accounts/login/"
        await self.email_sender.send_password_reset_complete_email(email, login_link)
        return "Password reset successfully."

    async def login_user(self, email: str, password: str) -> LoginResult:
        user = await self.users.get_by_email(email)
        if not user or not user.verify_password(password):
            raise InvalidCredentialsError
        if not user.is_active:
            raise InactiveUserError

        refresh_token_value = self.jwt_manager.create_refresh_token(
            {"user_id": user.id}
        )
        refresh_token = RefreshTokenModel.create(
            user_id=user.id,
            days_valid=self.settings.LOGIN_TIME_DAYS,
            token=refresh_token_value,
        )
        try:
            self.users.add_refresh_token(refresh_token)
            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while processing the request."
            ) from error

        access_token = self.jwt_manager.create_access_token({"user_id": user.id})
        return LoginResult(access_token=access_token, refresh_token=refresh_token_value)

    async def refresh_access_token(self, refresh_token: str) -> str:
        refresh_token_record = await self.users.get_refresh_token(refresh_token)
        if not refresh_token_record:
            raise RefreshTokenNotFoundError

        user = await self.users.get_by_id(refresh_token_record.user_id)
        if not user:
            raise UserNotFoundError

        return self.jwt_manager.create_access_token({"user_id": user.id})

    async def update_user_role(self, user_id: int, group: UserGroupEnum) -> str:
        target_user = await self.users.get_by_id(user_id)
        if not target_user:
            raise UserNotFoundError

        target_group = await self.users.get_group_by_name(group)
        if not target_group:
            raise RoleNotFoundError

        if target_group.name == UserGroupEnum.SUPERADMIN:
            raise SettingSuperAdminRoleError

        if target_user.group_id == target_group.id:
            return "User already has this role."

        current_group = await self.users.get_group_by_id(target_user.group_id)
        if (
            current_group
            and current_group.name == UserGroupEnum.SUPERADMIN
            and group != UserGroupEnum.SUPERADMIN
        ):
            admins_count = await self.users.count_users_in_group(target_user.group_id)
            if admins_count == 1:
                raise LastAdminDemotionError

        target_user.group_id = target_group.id
        await self.session.commit()
        return "User role updated successfully."

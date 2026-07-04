from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from database import (
    ActivationTokenModel,
    PasswordResetTokenModel,
    RefreshTokenModel,
    UserModel,
    UserRoleEnum,
)
from exceptions import (
    DatabaseWriteError,
    InvalidActivationTokenError,
    InvalidCredentialsError,
    InvalidPasswordResetTokenError,
    LastAdminDemotionError,
    RefreshTokenNotFoundError,
    SettingSuperAdminRoleError,
    UserAlreadyExistsError,
    UserNotFoundError,
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

    async def register_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        phone_number: str | None = None,
        source: str | None = "website",
    ) -> UserModel:
        user = await self.users.get_by_email_with_activation_token(email)
        if user:
            raise UserAlreadyExistsError(email)

        try:
            user = UserModel.create(
                email=email,
                raw_password=password,
                first_name=first_name,
                last_name=last_name,
                source=source or "website",
            )
            user.phone_number = phone_number
            self.users.add_user(user)
            await self.users.flush()

            activation_token = ActivationTokenModel(user_id=user.id)
            self.users.add_activation_token(activation_token)
            await self.session.commit()
            await self.session.refresh(user)
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

        await self.users.delete_activation_token(token_record)
        await self.session.commit()

        login_link = f"{self.settings.FRONTEND_BASE_URL}/accounts/login/"
        await self.email_sender.send_activation_complete_email(email, login_link)
        return "User account activated successfully."

    async def request_password_reset_token(self, email: str) -> str:
        user = await self.users.get_by_email(email)
        if not user:
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
        if not user:
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

    async def logout_user(self, user: UserModel, refresh_token: str) -> str:
        refresh_token_record = await self.users.get_refresh_token(refresh_token)
        if not refresh_token_record or user.id != refresh_token_record.user_id:
            raise RefreshTokenNotFoundError

        try:
            await self.users.delete_refresh_token(
                refresh_token_record=refresh_token_record
            )
            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while processing the request."
            ) from error

        return "User logged out successfully."

    async def refresh_access_token(self, refresh_token: str) -> str:
        refresh_token_record = await self.users.get_refresh_token(refresh_token)
        if not refresh_token_record:
            raise RefreshTokenNotFoundError

        user = await self.users.get_by_id(refresh_token_record.user_id)
        if not user:
            raise UserNotFoundError

        return self.jwt_manager.create_access_token({"user_id": user.id})

    async def update_user_role(self, user_id: int, role: UserRoleEnum) -> str:
        target_user = await self.users.get_by_id(user_id)
        if not target_user:
            raise UserNotFoundError

        if role == UserRoleEnum.SUPERADMIN:
            raise SettingSuperAdminRoleError

        if target_user.role == role:
            return "User already has this role."

        if (
            target_user.role == UserRoleEnum.SUPERADMIN
            and role != UserRoleEnum.SUPERADMIN
        ):
            admins_count = await self.users.count_users_with_role(
                UserRoleEnum.SUPERADMIN
            )
            if admins_count == 1:
                raise LastAdminDemotionError

        target_user.role = role
        await self.session.commit()
        return "User role updated successfully."

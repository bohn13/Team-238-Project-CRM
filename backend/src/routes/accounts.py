from fastapi import APIRouter, Depends, HTTPException, Query, status

from config import (
    Settings,
    get_accounts_email_notificator,
    get_jwt_auth_manager,
    get_settings,
)
from database import AsyncSessionDep
from exceptions import AuthServiceError, BaseSecurityError
from notifications import EmailSenderInterface
from schemas import (
    CurrentUserResponseSchema,
    MessageResponseSchema,
    PasswordResetCompleteRequestSchema,
    PasswordResetRequestSchema,
    TokenRefreshRequestSchema,
    TokenRefreshResponseSchema,
    UserActivationRequestSchema,
    UserItemResponseSchema,
    UserLoginRequestSchema,
    UserLoginResponseSchema,
    UserRegistrationRequestSchema,
    UserRegistrationResponseSchema,
    UserRoleUpdateRequestSchema,
)
from security.auth import CurrentUserDep
from security.interfaces import JWTAuthManagerInterface
from security.permissions import AdminDep
from services.auth import AuthService

router = APIRouter()


def map_auth_error(error: AuthServiceError) -> HTTPException:
    return HTTPException(status_code=error.status_code, detail=error.detail)


def get_auth_service(
    db: AsyncSessionDep,
    settings: Settings = Depends(get_settings),
    jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager),
    email_sender: EmailSenderInterface = Depends(get_accounts_email_notificator),
) -> AuthService:
    return AuthService(
        session=db,
        settings=settings,
        jwt_manager=jwt_manager,
        email_sender=email_sender,
    )


AuthServiceDep = Depends(get_auth_service)


@router.post(
    "/register/",
    response_model=UserRegistrationResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Register a new user with an email and password.",
)
async def register_user(
    user_data: UserRegistrationRequestSchema,
    _: AdminDep,
    auth_service: AuthService = AuthServiceDep,
) -> UserRegistrationResponseSchema:
    try:
        user = await auth_service.register_user(
            email=str(user_data.email),
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=user_data.phone_number,
            source=user_data.source,
        )
    except AuthServiceError as error:
        raise map_auth_error(error) from error
    return UserRegistrationResponseSchema.model_validate(user)


@router.post(
    "/activate/",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Activate user account",
)
async def activate_account(
    activation_data: UserActivationRequestSchema,
    auth_service: AuthService = AuthServiceDep,
) -> MessageResponseSchema:
    try:
        message = await auth_service.activate_account(
            email=str(activation_data.email), token=activation_data.token
        )
    except AuthServiceError as error:
        raise map_auth_error(error) from error
    return MessageResponseSchema(message=message)


@router.post(
    "/password-reset/request/",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Request password reset token",
)
async def request_password_reset_token(
    data: PasswordResetRequestSchema,
    auth_service: AuthService = AuthServiceDep,
) -> MessageResponseSchema:
    message = await auth_service.request_password_reset_token(email=str(data.email))
    return MessageResponseSchema(message=message)


@router.post(
    "/reset-password/complete/",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Reset user password",
)
async def reset_password(
    data: PasswordResetCompleteRequestSchema,
    auth_service: AuthService = AuthServiceDep,
) -> MessageResponseSchema:
    try:
        message = await auth_service.reset_password(
            email=str(data.email),
            token=data.token,
            password=data.password,
        )
    except AuthServiceError as error:
        raise map_auth_error(error) from error
    return MessageResponseSchema(message=message)


@router.post(
    "/login/",
    response_model=UserLoginResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="User login",
)
async def login_user(
    login_data: UserLoginRequestSchema,
    auth_service: AuthService = AuthServiceDep,
) -> UserLoginResponseSchema:
    try:
        tokens = await auth_service.login_user(
            email=str(login_data.email), password=login_data.password
        )
    except AuthServiceError as error:
        raise map_auth_error(error) from error
    return UserLoginResponseSchema(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


@router.post(
    "/logout",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Log out user",
)
async def logout_user(
    token_data: TokenRefreshRequestSchema,
    user: CurrentUserDep,
    auth_service: AuthService = AuthServiceDep,
    jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager),
) -> MessageResponseSchema:
    try:
        jwt_manager.decode_refresh_token(token_data.refresh_token)
        await auth_service.logout_user(
            user=user, refresh_token=token_data.refresh_token
        )
    except BaseSecurityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error
    except AuthServiceError as error:
        raise map_auth_error(error) from error
    return MessageResponseSchema(message="Logout Successfully")


@router.post(
    "/refresh/",
    response_model=TokenRefreshResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
)
async def refresh_access_token(
    token_data: TokenRefreshRequestSchema,
    auth_service: AuthService = AuthServiceDep,
    jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager),
) -> TokenRefreshResponseSchema:
    try:
        jwt_manager.decode_refresh_token(token_data.refresh_token)
        access_token = await auth_service.refresh_access_token(
            refresh_token=token_data.refresh_token
        )
    except BaseSecurityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error
    except AuthServiceError as error:
        raise map_auth_error(error) from error
    return TokenRefreshResponseSchema(access_token=access_token)


@router.patch(
    "/users/{user_id}/role/",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Change user role",
)
async def update_user_role(
    user_id: int,
    data: UserRoleUpdateRequestSchema,
    _: AdminDep,
    auth_service: AuthService = AuthServiceDep,
) -> MessageResponseSchema:
    try:
        message = await auth_service.update_user_role(user_id=user_id, role=data.role)
    except AuthServiceError as error:
        raise map_auth_error(error) from error
    return MessageResponseSchema(message=message)


@router.get(
    "/users/me/",
    response_model=CurrentUserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
)
async def get_current_user_profile(user: CurrentUserDep) -> CurrentUserResponseSchema:
    return CurrentUserResponseSchema.model_validate(user)


@router.get(
    "/users/",
    response_model=list[UserItemResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Get active users",
)
async def list_users(
    _: AdminDep,
    auth_service: AuthService = AuthServiceDep,
    search: str | None = Query(default=None, max_length=100),
) -> list[UserItemResponseSchema]:
    result = await auth_service.list_users(search=search)
    return [UserItemResponseSchema.model_validate(item) for item in result]

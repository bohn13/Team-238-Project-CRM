from typing import Annotated

from fastapi import Depends, HTTPException, status

from config import get_jwt_auth_manager
from database import AsyncSessionDep, UserModel
from exceptions import BaseSecurityError
from repositories.users import UserRepository
from security.http import get_token
from security.interfaces import JWTAuthManagerInterface

TokenDep = Annotated[str, Depends(get_token)]


async def get_current_user(
    token: TokenDep,
    db: AsyncSessionDep,
    jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager),
) -> UserModel:
    try:
        payload = jwt_manager.decode_access_token(token)
        user_id = payload.get("user_id")
    except BaseSecurityError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error)
        ) from error

    if not isinstance(user_id, int):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload."
        )

    user = await UserRepository(db).get_current_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    return user


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]

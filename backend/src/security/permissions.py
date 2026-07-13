from typing import Annotated

from fastapi import Depends, HTTPException, status

from database import UserModel, UserRoleEnum
from security.auth import get_current_user


async def get_admin_user(user: UserModel = Depends(get_current_user)) -> UserModel:
    if user.role not in (UserRoleEnum.SUPERADMIN, UserRoleEnum.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this action.",
        )
    return user


AdminDep = Annotated[UserModel, Depends(get_admin_user)]


async def get_superadmin_user(user: UserModel = Depends(get_current_user)) -> UserModel:
    if user.role != UserRoleEnum.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmin can perform this action.",
        )
    return user


async def get_doctor_admin_or_superadmin_user(
    user: UserModel = Depends(get_current_user),
) -> UserModel:
    if user.role not in (
        UserRoleEnum.SUPERADMIN,
        UserRoleEnum.ADMIN,
        UserRoleEnum.DOCTOR,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this action.",
        )
    return user


DoctorAdminOrSuperAdminDep = Annotated[
    UserModel,
    Depends(get_doctor_admin_or_superadmin_user),
]

SuperAdminDep = Annotated[UserModel, Depends(get_superadmin_user)]

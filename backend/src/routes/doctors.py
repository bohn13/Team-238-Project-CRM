from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)

from config import get_s3_storage_client
from database import AsyncSessionDep, DoctorEmploymentTypeEnum
from exceptions import BaseS3StorageError, DoctorServiceError, UserNotFoundError
from routes.accounts import map_auth_error
from schemas import (
    DoctorListResponseSchema,
    DoctorResponseSchema,
    MessageResponseSchema,
)
from schemas.doctors import (
    DoctorProfileCreateRequestSchema,
    DoctorProfileUpdateRequestSchema,
    DoctorSortBy,
    SortOrder,
)
from security.auth import CurrentUserDep
from security.permissions import AdminDep, DoctorAdminOrSuperAdminDep
from services.doctors import DoctorService
from storages import S3StorageInterface

router = APIRouter()


def map_doctor_error(error: DoctorServiceError) -> HTTPException:
    return HTTPException(status_code=error.status_code, detail=error.detail)


def get_doctor_service(db: AsyncSessionDep) -> DoctorService:
    return DoctorService(session=db)


DoctorServiceDep = Depends(get_doctor_service)


@router.get(
    "/",
    response_model=DoctorListResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="List doctors",
)
async def list_doctors(
    _: DoctorAdminOrSuperAdminDep,
    doctor_service: DoctorService = DoctorServiceDep,
    storage: S3StorageInterface = Depends(get_s3_storage_client),
    search: str | None = Query(default=None, max_length=100),
    specialization: str | None = Query(default=None, max_length=100),
    employment_type: DoctorEmploymentTypeEnum | None = None,
    sort_by: DoctorSortBy = "name",
    sort_order: SortOrder = "asc",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> DoctorListResponseSchema:
    try:
        result = await doctor_service.list_profiles(
            search=search,
            specialization=specialization,
            employment_type=employment_type,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size,
            storage=storage,
        )
    except BaseS3StorageError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
    return DoctorListResponseSchema.model_validate(result)


@router.post(
    "/profile/",
    response_model=DoctorResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create doctor profile",
)
async def create_doctor_profile(
    _: AdminDep,
    data: Annotated[
        DoctorProfileCreateRequestSchema,
        Form(media_type="multipart/form-data"),
    ],
    doctor_service: DoctorService = DoctorServiceDep,
    storage: S3StorageInterface = Depends(get_s3_storage_client),
) -> DoctorResponseSchema:
    try:
        doctor = await doctor_service.create_profile(
            user_id=data.user_id,
            specialization=data.specialization,
            years_experience=data.years_experience,
            employment_type=data.employment_type,
            phone_number=data.phone_number,
            avatar_file_data=await data.avatar.read() if data.avatar else None,
            avatar_content_type=data.avatar.content_type if data.avatar else None,
            storage=storage,
        )
    except UserNotFoundError as error:
        raise map_auth_error(error) from error
    except DoctorServiceError as error:
        raise map_doctor_error(error) from error
    except BaseS3StorageError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
    return DoctorResponseSchema.model_validate(doctor)


@router.get(
    "/{id}/profile/",
    response_model=DoctorResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get doctor profile",
)
async def get_doctor_profile(
    id: int,
    current_user: CurrentUserDep,
    doctor_service: DoctorService = DoctorServiceDep,
    storage: S3StorageInterface = Depends(get_s3_storage_client),
) -> DoctorResponseSchema:
    try:
        doctor = await doctor_service.get_profile(
            current_user=current_user,
            doctor_id=id,
            storage=storage,
        )
    except DoctorServiceError as error:
        raise map_doctor_error(error) from error
    except BaseS3StorageError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
    return DoctorResponseSchema.model_validate(doctor)


@router.patch(
    "/{id}/profile/",
    response_model=DoctorResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update doctor profile",
)
async def update_doctor_profile(
    id: int,
    current_user: CurrentUserDep,
    data: Annotated[
        DoctorProfileUpdateRequestSchema,
        Form(media_type="multipart/form-data"),
    ],
    doctor_service: DoctorService = DoctorServiceDep,
    storage: S3StorageInterface = Depends(get_s3_storage_client),
) -> DoctorResponseSchema:
    update_data = data.model_dump(exclude={"avatar"}, exclude_none=True)
    try:
        doctor = await doctor_service.update_profile(
            current_user=current_user,
            doctor_id=id,
            data=update_data,
            storage=storage,
            avatar_file_data=await data.avatar.read() if data.avatar else None,
            avatar_content_type=data.avatar.content_type if data.avatar else None,
        )
    except DoctorServiceError as error:
        raise map_doctor_error(error) from error
    except BaseS3StorageError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
    return DoctorResponseSchema.model_validate(doctor)


@router.post(
    "/{id}/avatar/",
    response_model=DoctorResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Upload doctor avatar",
)
async def upload_doctor_avatar(
    id: int,
    current_user: CurrentUserDep,
    avatar: UploadFile = File(...),
    doctor_service: DoctorService = DoctorServiceDep,
    storage: S3StorageInterface = Depends(get_s3_storage_client),
) -> DoctorResponseSchema:
    try:
        doctor = await doctor_service.upload_avatar(
            current_user=current_user,
            doctor_id=id,
            file_data=await avatar.read(),
            content_type=avatar.content_type,
            storage=storage,
        )
    except DoctorServiceError as error:
        raise map_doctor_error(error) from error
    except BaseS3StorageError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
    return DoctorResponseSchema.model_validate(doctor)


@router.delete(
    "/{id}/",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Delete doctor profile",
)
async def delete_doctor_profile(
    id: int,
    _: AdminDep,
    doctor_service: DoctorService = DoctorServiceDep,
    storage: S3StorageInterface = Depends(get_s3_storage_client),
) -> MessageResponseSchema:
    try:
        message = await doctor_service.delete_profile(doctor_id=id, storage=storage)
    except BaseS3StorageError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
    except DoctorServiceError as error:
        raise map_doctor_error(error) from error
    return MessageResponseSchema(message=message)

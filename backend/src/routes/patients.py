from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.session_postgresql import get_postgresql_db
from exceptions import DatabaseWriteError
from schemas.patients import (
    PatientCreate,
    PatientListResponse,
    PatientResponse,
    PatientUpdate,
)
from security.permissions import DoctorAdminOrSuperAdminDep
from services.patients import PatientService


router = APIRouter()


@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_patient(
    patient_data: PatientCreate,
    current_user: DoctorAdminOrSuperAdminDep,
    db: AsyncSession = Depends(get_postgresql_db),
) -> PatientResponse:
    service = PatientService(db)

    try:
        return await service.create_profile(patient_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except DatabaseWriteError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error


@router.get(
    "/",
    response_model=list[PatientListResponse],
)
async def get_patients(
    current_user: DoctorAdminOrSuperAdminDep,
    db: AsyncSession = Depends(get_postgresql_db),
) -> list[PatientListResponse]:
    service = PatientService(db)

    return await service.get_all()


@router.get(
    "/{patient_id}/",
    response_model=PatientResponse,
)
async def get_patient(
    patient_id: int,
    current_user: DoctorAdminOrSuperAdminDep,
    db: AsyncSession = Depends(get_postgresql_db),
) -> PatientResponse:
    service = PatientService(db)

    try:
        return await service.get_by_id(patient_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.patch(
    "/{patient_id}/",
    response_model=PatientResponse,
)
async def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    current_user: DoctorAdminOrSuperAdminDep,
    db: AsyncSession = Depends(get_postgresql_db),
) -> PatientResponse:
    service = PatientService(db)

    try:
        return await service.update_profile(
            patient_id=patient_id,
            patient_data=patient_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except DatabaseWriteError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error


@router.delete(
    "/{patient_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient(
    patient_id: int,
    current_user: DoctorAdminOrSuperAdminDep,
    db: AsyncSession = Depends(get_postgresql_db),
) -> None:
    service = PatientService(db)

    try:
        await service.delete_profile(patient_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except DatabaseWriteError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error

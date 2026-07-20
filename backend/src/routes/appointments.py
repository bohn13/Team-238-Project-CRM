from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.appointments import AppointmentStatusEnum
from database.session_postgresql import get_postgresql_db
from repositories.appointments import AppointmentRepository
from schemas.appointments import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
)


router = APIRouter(
    tags=["appointments"],
)


@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    appointment_data: AppointmentCreate,
    db: AsyncSession = Depends(get_postgresql_db),
):
    repository = AppointmentRepository(db)

    try:
        return await repository.create(appointment_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "/",
    response_model=list[AppointmentResponse],
)
async def get_appointments(
    doctor_id: int | None = None,
    patient_id: int | None = None,
    appointment_date: date | None = None,
    appointment_status: AppointmentStatusEnum | None = None,
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_postgresql_db),
):
    repository = AppointmentRepository(db)

    return await repository.get_all(
        doctor_id=doctor_id,
        patient_id=patient_id,
        appointment_date=appointment_date,
        appointment_status=appointment_status,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{appointment_id}/",
    response_model=AppointmentResponse,
)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
):
    repository = AppointmentRepository(db)

    appointment = await repository.get_by_id(appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    return appointment


@router.patch(
    "/{appointment_id}/",
    response_model=AppointmentResponse,
)
async def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: AsyncSession = Depends(get_postgresql_db),
):
    repository = AppointmentRepository(db)

    appointment = await repository.get_by_id(appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    try:
        return await repository.update(
            appointment=appointment,
            appointment_data=appointment_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.delete(
    "/{appointment_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
) -> None:
    repository = AppointmentRepository(db)

    appointment = await repository.get_by_id(appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    await repository.delete(appointment)


@router.patch(
    "/{appointment_id}/confirm/",
    response_model=AppointmentResponse,
)
async def confirm_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
):
    repository = AppointmentRepository(db)

    appointment = await repository.get_by_id(appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    try:
        return await repository.confirm(appointment)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.patch(
    "/{appointment_id}/cancel/",
    response_model=AppointmentResponse,
)
async def cancel_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
):
    repository = AppointmentRepository(db)

    appointment = await repository.get_by_id(appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    try:
        return await repository.cancel(appointment)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.patch(
    "/{appointment_id}/restore/",
    response_model=AppointmentResponse,
)
async def restore_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
):
    repository = AppointmentRepository(db)

    appointment = await repository.get_by_id(appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    try:
        return await repository.restore(appointment)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

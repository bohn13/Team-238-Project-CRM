from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.session_postgresql import get_postgresql_db
from repositories.appointments import (
    create_appointment,
    delete_appointment,
    get_appointment_by_id,
    get_appointments,
    update_appointment,
)
from schemas.appointments import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
)

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment_route(
    appointment_data: AppointmentCreate,
    db: AsyncSession = Depends(get_postgresql_db),
):
    try:
        return await create_appointment(db, appointment_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get("/", response_model=list[AppointmentResponse])
async def get_appointments_route(
    db: AsyncSession = Depends(get_postgresql_db),
):
    return await get_appointments(db)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment_route(
    appointment_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
):
    appointment = await get_appointment_by_id(db, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    return appointment


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment_route(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: AsyncSession = Depends(get_postgresql_db),
):
    appointment = await get_appointment_by_id(db, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    try:
        return await update_appointment(db, appointment, appointment_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment_route(
    appointment_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
):
    appointment = await get_appointment_by_id(db, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    await delete_appointment(db, appointment)

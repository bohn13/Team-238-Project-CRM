from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.appointments import AppointmentModel, AppointmentStatusEnum
from schemas.appointments import AppointmentCreate, AppointmentUpdate


async def is_doctor_busy(
    db: AsyncSession,
    doctor_id: int,
    date_time: datetime,
    exclude_appointment_id: int | None = None,
) -> bool:
    query = select(AppointmentModel).where(
        AppointmentModel.doctor_id == doctor_id,
        AppointmentModel.date_time == date_time,
        AppointmentModel.status != AppointmentStatusEnum.CANCELLED,
    )

    if exclude_appointment_id is not None:
        query = query.where(AppointmentModel.id != exclude_appointment_id)

    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


async def create_appointment(
    db: AsyncSession,
    appointment_data: AppointmentCreate,
) -> AppointmentModel:
    doctor_busy = await is_doctor_busy(
        db=db,
        doctor_id=appointment_data.doctor_id,
        date_time=appointment_data.date_time,
    )

    if doctor_busy:
        raise ValueError("Doctor already has an appointment at this time.")

    appointment = AppointmentModel(
        **appointment_data.model_dump(),
        status=AppointmentStatusEnum.SCHEDULED,
    )

    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


async def get_appointments(db: AsyncSession) -> list[AppointmentModel]:
    result = await db.execute(select(AppointmentModel))
    return list(result.scalars().all())


async def get_appointment_by_id(
    db: AsyncSession,
    appointment_id: int,
) -> AppointmentModel | None:
    result = await db.execute(
        select(AppointmentModel).where(AppointmentModel.id == appointment_id)
    )
    return result.scalar_one_or_none()


async def update_appointment(
    db: AsyncSession,
    appointment: AppointmentModel,
    appointment_data: AppointmentUpdate,
) -> AppointmentModel:
    update_data = appointment_data.model_dump(exclude_unset=True)

    new_doctor_id = update_data.get("doctor_id", appointment.doctor_id)
    new_date_time = update_data.get("date_time", appointment.date_time)

    doctor_busy = await is_doctor_busy(
        db=db,
        doctor_id=new_doctor_id,
        date_time=new_date_time,
        exclude_appointment_id=appointment.id,
    )

    if doctor_busy:
        raise ValueError("Doctor already has an appointment at this time.")

    for field, value in update_data.items():
        setattr(appointment, field, value)

    await db.commit()
    await db.refresh(appointment)
    return appointment


async def cancel_appointment(
    db: AsyncSession,
    appointment: AppointmentModel,
) -> AppointmentModel:
    appointment.status = AppointmentStatusEnum.CANCELLED

    await db.commit()
    await db.refresh(appointment)
    return appointment


async def delete_appointment(
    db: AsyncSession,
    appointment: AppointmentModel,
) -> None:
    await db.delete(appointment)
    await db.commit()

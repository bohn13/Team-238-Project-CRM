from datetime import date, datetime, time, timedelta

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.appointments import (
    AppointmentModel,
    AppointmentStatusEnum,
)
from schemas.appointments import AppointmentCreate, AppointmentUpdate


ACTIVE_APPOINTMENT_STATUSES = (
    AppointmentStatusEnum.SCHEDULED,
    AppointmentStatusEnum.CONFIRMED,
    AppointmentStatusEnum.WAITING,
    AppointmentStatusEnum.ONGOING,
)


class AppointmentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def is_doctor_busy(
        self,
        doctor_id: int,
        date_time: datetime,
        duration: int = 30,
        exclude_appointment_id: int | None = None,
    ) -> bool:
        new_appointment_end = date_time + timedelta(minutes=duration)

        existing_appointment_end = (
            AppointmentModel.date_time
            + AppointmentModel.duration * text("INTERVAL '1 minute'")
        )

        query = select(AppointmentModel.id).where(
            AppointmentModel.doctor_id == doctor_id,
            AppointmentModel.status.in_(ACTIVE_APPOINTMENT_STATUSES),
            AppointmentModel.date_time < new_appointment_end,
            existing_appointment_end > date_time,
        )

        if exclude_appointment_id is not None:
            query = query.where(AppointmentModel.id != exclude_appointment_id)

        result = await self.db.execute(query)

        return result.scalar_one_or_none() is not None

    async def create(
        self,
        appointment_data: AppointmentCreate,
    ) -> AppointmentModel:
        appointment_values = appointment_data.model_dump()

        duration = appointment_values.get("duration") or 30

        doctor_busy = await self.is_doctor_busy(
            doctor_id=appointment_data.doctor_id,
            date_time=appointment_data.date_time,
            duration=duration,
        )

        if doctor_busy:
            raise ValueError("Doctor already has an appointment during this time.")

        appointment_values["duration"] = duration
        appointment_values["status"] = AppointmentStatusEnum.SCHEDULED

        appointment = AppointmentModel(**appointment_values)

        self.db.add(appointment)
        await self.db.commit()
        await self.db.refresh(appointment)

        return appointment

    async def get_all(
        self,
        doctor_id: int | None = None,
        patient_id: int | None = None,
        appointment_date: date | None = None,
        appointment_status: AppointmentStatusEnum | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AppointmentModel]:
        query = select(AppointmentModel)

        if doctor_id is not None:
            query = query.where(AppointmentModel.doctor_id == doctor_id)

        if patient_id is not None:
            query = query.where(AppointmentModel.patient_id == patient_id)

        if appointment_date is not None:
            day_start = datetime.combine(
                appointment_date,
                time.min,
            )
            day_end = day_start + timedelta(days=1)

            query = query.where(
                AppointmentModel.date_time >= day_start,
                AppointmentModel.date_time < day_end,
            )

        if appointment_status is not None:
            query = query.where(AppointmentModel.status == appointment_status)

        query = query.order_by(AppointmentModel.date_time).offset(offset).limit(limit)

        result = await self.db.execute(query)

        return list(result.scalars().all())

    async def get_by_id(
        self,
        appointment_id: int,
    ) -> AppointmentModel | None:
        result = await self.db.execute(
            select(AppointmentModel).where(AppointmentModel.id == appointment_id)
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        appointment: AppointmentModel,
        appointment_data: AppointmentUpdate,
    ) -> AppointmentModel:
        update_data = appointment_data.model_dump(exclude_unset=True)

        new_doctor_id = update_data.get(
            "doctor_id",
            appointment.doctor_id,
        )
        new_date_time = update_data.get(
            "date_time",
            appointment.date_time,
        )
        new_duration = update_data.get(
            "duration",
            appointment.duration,
        )

        doctor_busy = await self.is_doctor_busy(
            doctor_id=new_doctor_id,
            date_time=new_date_time,
            duration=new_duration,
            exclude_appointment_id=appointment.id,
        )

        if doctor_busy:
            raise ValueError("Doctor already has an appointment during this time.")

        for field, value in update_data.items():
            setattr(appointment, field, value)

        await self.db.commit()
        await self.db.refresh(appointment)

        return appointment

    async def confirm(
        self,
        appointment: AppointmentModel,
    ) -> AppointmentModel:

        if appointment.status == AppointmentStatusEnum.CANCELLED:
            raise ValueError("Cancelled appointment cannot be confirmed.")

        if appointment.status == AppointmentStatusEnum.CONFIRMED:
            raise ValueError("Appointment is already confirmed.")

        appointment.status = AppointmentStatusEnum.CONFIRMED

        await self.db.commit()
        await self.db.refresh(appointment)

        return appointment

    async def cancel(
        self,
        appointment: AppointmentModel,
    ) -> AppointmentModel:
        if appointment.status == AppointmentStatusEnum.CANCELLED:
            raise ValueError("Appointment is already cancelled.")

        if appointment.status == AppointmentStatusEnum.COMPLETED:
            raise ValueError("Completed appointment cannot be cancelled.")

        appointment.status = AppointmentStatusEnum.CANCELLED

        await self.db.commit()
        await self.db.refresh(appointment)

        return appointment

    async def delete(
        self,
        appointment: AppointmentModel,
    ) -> None:
        await self.db.delete(appointment)
        await self.db.commit()

    async def restore(
        self,
        appointment: AppointmentModel,
    ) -> AppointmentModel:
        if appointment.status != AppointmentStatusEnum.CANCELLED:
            raise ValueError("Only cancelled appointment can be restored.")

        is_busy = await self.is_doctor_busy(
            doctor_id=appointment.doctor_id,
            date_time=appointment.date_time,
            duration=appointment.duration,
            exclude_appointment_id=appointment.id,
        )

        if is_busy:
            raise ValueError("Doctor already has an appointment during this time.")

        appointment.status = AppointmentStatusEnum.SCHEDULED

        await self.db.commit()
        await self.db.refresh(appointment)

        return appointment

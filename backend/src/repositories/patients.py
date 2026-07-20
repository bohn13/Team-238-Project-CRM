from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.appointments import (
    AppointmentModel,
    AppointmentStatusEnum,
)
from database.models.patient import PatientModel
from database.models.users import UserModel
from schemas.patients import PatientUpdate


class PatientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, patient: PatientModel) -> None:
        self.session.add(patient)

    async def get_by_id(
        self,
        patient_id: int,
    ) -> PatientModel | None:
        return await self.session.scalar(
            select(PatientModel).where(PatientModel.id == patient_id)
        )

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> PatientModel | None:
        return await self.session.scalar(
            select(PatientModel).where(PatientModel.user_id == user_id)
        )

    async def get_all(self) -> list[dict]:
        last_visit_subquery = (
            select(
                AppointmentModel.patient_id,
                func.max(AppointmentModel.date_time).label("last_visit_date"),
            )
            .where(AppointmentModel.status == AppointmentStatusEnum.COMPLETED)
            .group_by(AppointmentModel.patient_id)
            .subquery()
        )

        statement = (
            select(
                PatientModel.id,
                PatientModel.user_id,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.phone_number,
                PatientModel.date_of_birth,
                PatientModel.source,
                last_visit_subquery.c.last_visit_date,
            )
            .join(
                UserModel,
                PatientModel.user_id == UserModel.id,
            )
            .outerjoin(
                last_visit_subquery,
                last_visit_subquery.c.patient_id == PatientModel.id,
            )
            .order_by(
                UserModel.last_name,
                UserModel.first_name,
            )
        )

        result = await self.session.execute(statement)

        return [dict(row._mapping) for row in result.all()]

    def update(
        self,
        patient: PatientModel,
        patient_data: PatientUpdate,
    ) -> PatientModel:
        update_data = patient_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(patient, field, value)

        return patient

    async def delete(
        self,
        patient: PatientModel,
    ) -> None:
        await self.session.delete(patient)

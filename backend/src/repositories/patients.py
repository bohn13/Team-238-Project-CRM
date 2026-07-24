from sqlalchemy import exists, func, or_, select, text
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
            select(PatientModel).where(
                PatientModel.id == patient_id,
            )
        )

    async def get_details_by_id(
            self,
            patient_id: int,
    ) -> dict | None:
        statement = (
            select(
                PatientModel.id,
                PatientModel.user_id,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.email,
                UserModel.phone_number,
                PatientModel.gender,
                PatientModel.date_of_birth,
                PatientModel.address,
                PatientModel.source,
            )
            .join(
                UserModel,
                PatientModel.user_id == UserModel.id,
            )
            .where(
                PatientModel.id == patient_id,
            )
        )

        result = await self.session.execute(statement)
        row = result.first()

        if row is None:
            return None

        return dict(row._mapping)

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> PatientModel | None:
        return await self.session.scalar(
            select(PatientModel).where(
                PatientModel.user_id == user_id,
            )
        )

    @staticmethod
    def _get_last_visit_subquery():

        return (
            select(
                AppointmentModel.patient_id,
                func.max(
                    AppointmentModel.date_time,
                ).label("last_visit_date"),
            )
            .where(
                AppointmentModel.status
                == AppointmentStatusEnum.COMPLETED,
            )
            .group_by(
                AppointmentModel.patient_id,
            )
            .subquery()
        )

    @staticmethod
    def _apply_filters(
        statement,
        last_visit_subquery,
        category: str,
        search: str | None,
    ):

        if category == "new":
            statement = statement.where(
                UserModel.registration_date
                >= func.now() - text("INTERVAL '3 days'")
            )

        elif category == "today":
            today_appointment_exists = exists(
                select(AppointmentModel.id).where(
                    AppointmentModel.patient_id == PatientModel.id,
                    func.date(AppointmentModel.date_time)
                    == func.current_date(),
                    AppointmentModel.status
                    != AppointmentStatusEnum.CANCELLED,
                )
            )

            statement = statement.where(
                today_appointment_exists,
            )

        elif category == "inactive":
            statement = statement.where(
                last_visit_subquery.c.last_visit_date.is_not(None),
                last_visit_subquery.c.last_visit_date
                < func.now() - text("INTERVAL '6 months'"),
            )

        if search:
            search_value = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    UserModel.first_name.ilike(search_value),
                    UserModel.last_name.ilike(search_value),
                    UserModel.phone_number.ilike(search_value),
                )
            )

        return statement

    async def count(
        self,
        category: str = "all",
        search: str | None = None,
    ) -> int:

        last_visit_subquery = self._get_last_visit_subquery()

        statement = (
            select(
                func.count(PatientModel.id),
            )
            .join(
                UserModel,
                PatientModel.user_id == UserModel.id,
            )
            .outerjoin(
                last_visit_subquery,
                last_visit_subquery.c.patient_id == PatientModel.id,
            )
        )

        statement = self._apply_filters(
            statement=statement,
            last_visit_subquery=last_visit_subquery,
            category=category,
            search=search,
        )

        total = await self.session.scalar(statement)

        return total or 0

    async def get_all(
        self,
        category: str = "all",
        search: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[dict]:

        last_visit_subquery = self._get_last_visit_subquery()

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
        )

        statement = self._apply_filters(
            statement=statement,
            last_visit_subquery=last_visit_subquery,
            category=category,
            search=search,
        )

        statement = (
            statement.order_by(
                UserModel.last_name,
                UserModel.first_name,
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(statement)

        return [
            dict(row._mapping)
            for row in result.all()
        ]

    def update(
        self,
        patient: PatientModel,
        patient_data: PatientUpdate,
    ) -> PatientModel:
        update_data = patient_data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(patient, field, value)

        return patient

    async def delete(
        self,
        patient: PatientModel,
    ) -> None:
        await self.session.delete(patient)

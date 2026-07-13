from sqlalchemy import Select, asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import DoctorEmploymentTypeEnum, DoctorModel, UserModel


class DoctorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, doctor_id: int) -> DoctorModel | None:
        return await self.session.scalar(
            select(DoctorModel)
            .options(joinedload(DoctorModel.user))
            .where(DoctorModel.id == doctor_id)
        )

    async def get_by_user_id(self, user_id: int) -> DoctorModel | None:
        return await self.session.scalar(
            select(DoctorModel)
            .options(joinedload(DoctorModel.user))
            .where(DoctorModel.user_id == user_id)
        )

    def add(self, doctor: DoctorModel) -> None:
        self.session.add(doctor)

    async def delete(self, doctor: DoctorModel) -> None:
        await self.session.delete(doctor)

    async def count(
        self,
        search: str | None = None,
        specialization: str | None = None,
        employment_type: DoctorEmploymentTypeEnum | None = None,
    ) -> int:
        statement = select(func.count(DoctorModel.id)).join(DoctorModel.user)
        statement = self._apply_filters(
            statement=statement,
            search=search,
            specialization=specialization,
            employment_type=employment_type,
        )
        result = await self.session.scalar(statement)
        return int(result or 0)

    async def list(
        self,
        search: str | None = None,
        specialization: str | None = None,
        employment_type: DoctorEmploymentTypeEnum | None = None,
        sort_by: str = "name",
        sort_order: str = "asc",
        offset: int = 0,
        limit: int = 20,
    ) -> list[DoctorModel]:
        statement = (
            select(DoctorModel)
            .options(joinedload(DoctorModel.user))
            .join(DoctorModel.user)
        )
        statement = self._apply_filters(
            statement=statement,
            search=search,
            specialization=specialization,
            employment_type=employment_type,
        )
        statement = self._apply_sorting(statement, sort_by, sort_order)
        statement = statement.offset(offset).limit(limit)
        result = await self.session.scalars(statement)
        return list(result)

    def _apply_filters(
        self,
        statement: Select,
        search: str | None,
        specialization: str | None,
        employment_type: DoctorEmploymentTypeEnum | None,
    ) -> Select:
        statement = statement.where(UserModel.is_active.is_(True))

        if search:
            pattern = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    UserModel.first_name.ilike(pattern),
                    UserModel.last_name.ilike(pattern),
                    UserModel.email.ilike(pattern),
                    UserModel.phone_number.ilike(pattern),
                )
            )

        if specialization:
            pattern = f"%{specialization.strip()}%"
            statement = statement.where(DoctorModel.specialization.ilike(pattern))

        if employment_type:
            statement = statement.where(DoctorModel.employment_type == employment_type)

        return statement

    def _apply_sorting(
        self, statement: Select, sort_by: str, sort_order: str
    ) -> Select:
        sort_map = {
            "name": UserModel.last_name,
            "specialization": DoctorModel.specialization,
            "years_experience": DoctorModel.years_experience,
            "created_at": DoctorModel.created_at,
        }
        column = sort_map.get(sort_by, UserModel.last_name)
        direction = desc if sort_order == "desc" else asc
        return statement.order_by(direction(column), asc(UserModel.first_name))

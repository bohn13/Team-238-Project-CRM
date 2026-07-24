from math import ceil

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.patient import PatientModel
from database.models.users import UserRoleEnum
from exceptions import DatabaseWriteError
from repositories.patients import PatientRepository
from repositories.users import UserRepository
from schemas.patients import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.patients = PatientRepository(session)
        self.users = UserRepository(session)

    async def create_profile(
        self,
        patient_data: PatientCreate,
    ) -> PatientModel:
        user = await self.users.get_by_id(patient_data.user_id)

        if user is None:
            raise ValueError("User not found.")

        if not user.is_active:
            raise ValueError("Patient profile can be created only for an active user.")

        existing_patient = await self.patients.get_by_user_id(patient_data.user_id)

        if existing_patient is not None:
            raise ValueError("Patient profile already exists for this user.")

        if user.role != UserRoleEnum.USER:
            raise ValueError("Patient profile can be created only for a regular user.")

        patient = PatientModel(**patient_data.model_dump())

        try:
            user.role = UserRoleEnum.PATIENT
            self.patients.add(patient)
            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while creating patient profile."
            ) from error

        created_patient = await self.patients.get_by_user_id(patient_data.user_id)

        if created_patient is None:
            raise ValueError("Patient profile was not created.")

        return created_patient

    async def get_all(
        self,
        category: str = "all",
        search: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        offset = (page - 1) * page_size

        total = await self.patients.count(
            category=category,
            search=search,
        )

        items = await self.patients.get_all(
            category=category,
            search=search,
            offset=offset,
            limit=page_size,
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": ceil(total / page_size) if total else 0,
        }

    async def get_by_id(
            self,
            patient_id: int,
    ) -> dict:
        patient = await self.patients.get_details_by_id(
            patient_id,
        )

        if patient is None:
            raise ValueError("Patient profile not found.")

        return patient

    async def update_profile(
        self,
        patient_id: int,
        patient_data: PatientUpdate,
    ) -> PatientModel:
        patient = await self.patients.get_by_id(patient_id)

        if patient is None:
            raise ValueError("Patient profile not found.")

        self.patients.update(
            patient,
            patient_data,
        )

        try:
            await self.session.commit()
            await self.session.refresh(patient)
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while updating patient profile."
            ) from error

        return patient

from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database import DoctorEmploymentTypeEnum, DoctorModel, UserModel, UserRoleEnum
from exceptions import (
    DatabaseWriteError,
    DoctorProfileAlreadyExistsError,
    DoctorProfileNotFoundError,
    DoctorProfilePermissionError,
    InvalidDoctorAvatarError,
    InvalidDoctorProfileUserError,
    UserNotFoundError,
)
from repositories.doctors import DoctorRepository
from repositories.users import UserRepository
from storages import S3StorageInterface


class DoctorService:
    allowed_avatar_content_types = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
    }
    max_avatar_size_bytes = 5 * 1024 * 1024

    def __init__(self, session: AsyncSession):
        self.session = session
        self.doctors = DoctorRepository(session)
        self.users = UserRepository(session)

    async def create_profile(
        self,
        current_user: UserModel,
        user_id: int,
        specialization: str,
        years_experience: int | None = None,
        employment_type: DoctorEmploymentTypeEnum | None = None,
    ) -> dict:
        self._ensure_can_manage_profile(current_user=current_user, user_id=user_id)

        user = await self.users.get_by_id(user_id)
        if not user:
            raise UserNotFoundError
        if not user.is_active or user.role != UserRoleEnum.USER:
            raise InvalidDoctorProfileUserError

        existing_profile = await self.doctors.get_by_user_id(user_id)
        if existing_profile:
            raise DoctorProfileAlreadyExistsError

        doctor = DoctorModel(
            user_id=user.id,
            specialization=specialization,
            years_experience=years_experience,
            employment_type=employment_type,
        )

        try:
            user.role = UserRoleEnum.DOCTOR
            self.doctors.add(doctor)
            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while creating doctor profile."
            ) from error

        created_doctor = await self.doctors.get_by_user_id(user_id)
        if not created_doctor:
            raise DoctorProfileNotFoundError
        return self._serialize_doctor(created_doctor)

    async def get_profile(self, current_user: UserModel, doctor_id: int) -> dict:
        doctor = await self.doctors.get_by_id(doctor_id)
        if not doctor or not doctor.user.is_active:
            raise DoctorProfileNotFoundError
        self._ensure_can_manage_profile(
            current_user=current_user, user_id=doctor.user_id
        )
        return self._serialize_doctor(doctor)

    async def update_profile(
        self,
        current_user: UserModel,
        doctor_id: int,
        data: dict,
    ) -> dict:
        doctor = await self.doctors.get_by_id(doctor_id)
        if not doctor or not doctor.user.is_active:
            raise DoctorProfileNotFoundError
        self._ensure_can_manage_profile(
            current_user=current_user, user_id=doctor.user_id
        )

        user_fields = {"first_name", "last_name", "phone_number"}
        doctor_fields = {"specialization", "years_experience", "employment_type"}

        try:
            for field, value in data.items():
                if field in user_fields:
                    setattr(doctor.user, field, value)
                if field in doctor_fields:
                    setattr(doctor, field, value)

            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while updating doctor profile."
            ) from error

        updated_doctor = await self.doctors.get_by_id(doctor_id)
        if not updated_doctor:
            raise DoctorProfileNotFoundError
        return self._serialize_doctor(updated_doctor)

    async def upload_avatar(
        self,
        current_user: UserModel,
        doctor_id: int,
        file_data: bytes,
        content_type: str | None,
        storage: S3StorageInterface,
    ) -> dict:
        doctor = await self.doctors.get_by_id(doctor_id)
        if not doctor or not doctor.user.is_active:
            raise DoctorProfileNotFoundError
        self._ensure_can_manage_profile(
            current_user=current_user, user_id=doctor.user_id
        )

        extension = self.allowed_avatar_content_types.get(content_type or "")
        if (
            not extension
            or not file_data
            or len(file_data) > self.max_avatar_size_bytes
        ):
            raise InvalidDoctorAvatarError

        file_name = f"doctors/{doctor.id}/avatar-{uuid4().hex}.{extension}"
        await storage.upload_file(file_name=file_name, file_data=file_data)
        avatar_url = await storage.get_file_url(file_name)

        try:
            doctor.avatar_url = avatar_url
            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while updating doctor avatar."
            ) from error

        updated_doctor = await self.doctors.get_by_id(doctor_id)
        if not updated_doctor:
            raise DoctorProfileNotFoundError
        return self._serialize_doctor(updated_doctor)

    async def delete_profile(self, doctor_id: int) -> str:
        doctor = await self.doctors.get_by_id(doctor_id)
        if not doctor or not doctor.user.is_active:
            raise DoctorProfileNotFoundError

        try:
            doctor.user.role = UserRoleEnum.USER
            await self.doctors.delete(doctor)
            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while deleting doctor profile."
            ) from error

        return "Doctor profile deleted successfully."

    async def list_profiles(
        self,
        search: str | None = None,
        specialization: str | None = None,
        employment_type: DoctorEmploymentTypeEnum | None = None,
        sort_by: str = "name",
        sort_order: str = "asc",
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        offset = (page - 1) * page_size
        total = await self.doctors.count(
            search=search,
            specialization=specialization,
            employment_type=employment_type,
        )
        doctors = await self.doctors.list(
            search=search,
            specialization=specialization,
            employment_type=employment_type,
            sort_by=sort_by,
            sort_order=sort_order,
            offset=offset,
            limit=page_size,
        )
        return {
            "items": [self._serialize_doctor(doctor) for doctor in doctors],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def _ensure_can_manage_profile(self, current_user: UserModel, user_id: int) -> None:
        if current_user.role in (UserRoleEnum.SUPERADMIN, UserRoleEnum.ADMIN):
            return
        if current_user.id == user_id and current_user.role in (
            UserRoleEnum.USER,
            UserRoleEnum.DOCTOR,
        ):
            return
        raise DoctorProfilePermissionError

    def _serialize_doctor(self, doctor: DoctorModel) -> dict:
        return {
            "id": doctor.id,
            "user_id": doctor.user_id,
            "doctor_code": f"DR{doctor.id:03d}",
            "first_name": doctor.user.first_name,
            "last_name": doctor.user.last_name,
            "email": doctor.user.email,
            "phone_number": doctor.user.phone_number,
            "specialization": doctor.specialization,
            "years_experience": doctor.years_experience,
            "employment_type": doctor.employment_type,
            "avatar_url": doctor.avatar_url,
            "created_at": doctor.created_at,
            "updated_at": doctor.updated_at,
        }

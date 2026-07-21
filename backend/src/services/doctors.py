from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database import DoctorEmploymentTypeEnum, DoctorModel, UserModel, UserRoleEnum
from exceptions import (
    BaseS3StorageError,
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
        user_id: int,
        specialization: str,
        years_experience: int | None = None,
        employment_type: DoctorEmploymentTypeEnum | None = None,
        avatar_file_data: bytes | None = None,
        avatar_content_type: str | None = None,
        storage: S3StorageInterface | None = None,
    ) -> dict:
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
            await self.session.flush()
            if avatar_file_data is not None:
                if storage is None:
                    raise InvalidDoctorAvatarError
                doctor.avatar_url = await self._upload_avatar_file(
                    doctor=doctor,
                    file_data=avatar_file_data,
                    content_type=avatar_content_type,
                    storage=storage,
                )
            await self.session.commit()
        except BaseS3StorageError:
            await self.session.rollback()
            raise
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while creating doctor profile."
            ) from error

        created_doctor = await self.doctors.get_by_user_id(user_id)
        if not created_doctor:
            raise DoctorProfileNotFoundError
        return await self._serialize_doctor(created_doctor, storage=storage)

    async def get_profile(
        self,
        current_user: UserModel,
        doctor_id: int,
        storage: S3StorageInterface | None = None,
    ) -> dict:
        doctor = await self.doctors.get_by_id(doctor_id)
        if not doctor or not doctor.user.is_active:
            raise DoctorProfileNotFoundError
        self._ensure_can_manage_profile(
            current_user=current_user, user_id=doctor.user_id
        )
        return await self._serialize_doctor(
            doctor,
            storage=storage,
        )

    async def update_profile(
        self,
        current_user: UserModel,
        doctor_id: int,
        data: dict,
        storage: S3StorageInterface | None = None,
        avatar_file_data: bytes | None = None,
        avatar_content_type: str | None = None,
    ) -> dict:
        doctor = await self.doctors.get_by_id(doctor_id)
        if not doctor or not doctor.user.is_active:
            raise DoctorProfileNotFoundError
        self._ensure_can_manage_profile(
            current_user=current_user,
            user_id=doctor.user_id,
        )

        user_fields = {"first_name", "last_name", "phone_number"}
        doctor_fields = {"specialization", "years_experience", "employment_type"}
        old_avatar_key = doctor.avatar_url

        try:
            for field, value in data.items():
                if field in user_fields:
                    setattr(doctor.user, field, value)
                if field in doctor_fields:
                    setattr(doctor, field, value)

            if avatar_file_data is not None:
                if storage is None:
                    raise InvalidDoctorAvatarError
                doctor.avatar_url = await self._upload_avatar_file(
                    doctor=doctor,
                    file_data=avatar_file_data,
                    content_type=avatar_content_type,
                    storage=storage,
                )
            await self.session.commit()
        except BaseS3StorageError:
            await self.session.rollback()
            raise
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while updating doctor profile."
            ) from error

        await self._delete_old_avatar_file(
            old_avatar_key=old_avatar_key,
            current_avatar_key=doctor.avatar_url,
            storage=storage,
        )

        updated_doctor = await self.doctors.get_by_id(doctor_id)
        if not updated_doctor:
            raise DoctorProfileNotFoundError
        return await self._serialize_doctor(
            updated_doctor,
            storage=storage,
        )

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
            current_user=current_user,
            user_id=doctor.user_id,
        )
        old_avatar_key = doctor.avatar_url

        try:
            doctor.avatar_url = await self._upload_avatar_file(
                doctor=doctor,
                file_data=file_data,
                content_type=content_type,
                storage=storage,
            )
            await self.session.commit()
        except BaseS3StorageError:
            await self.session.rollback()
            raise
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while updating doctor avatar."
            ) from error

        await self._delete_old_avatar_file(
            old_avatar_key=old_avatar_key,
            current_avatar_key=doctor.avatar_url,
            storage=storage,
        )

        updated_doctor = await self.doctors.get_by_id(doctor_id)
        if not updated_doctor:
            raise DoctorProfileNotFoundError
        return await self._serialize_doctor(
            updated_doctor,
            storage=storage,
        )

    async def delete_profile(
        self,
        doctor_id: int,
        storage: S3StorageInterface | None = None,
    ) -> str:
        doctor = await self.doctors.get_by_id(doctor_id)
        if not doctor or not doctor.user.is_active:
            raise DoctorProfileNotFoundError
        old_avatar_key = doctor.avatar_url

        try:
            doctor.user.role = UserRoleEnum.USER
            await self.doctors.delete(doctor)
            await self.session.commit()
        except SQLAlchemyError as error:
            await self.session.rollback()
            raise DatabaseWriteError(
                "An error occurred while deleting doctor profile."
            ) from error

        await self._delete_old_avatar_file(
            old_avatar_key=old_avatar_key,
            current_avatar_key=None,
            storage=storage,
        )

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
        storage: S3StorageInterface | None = None,
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
            "items": [
                await self._serialize_doctor(
                    doctor,
                    storage=storage,
                )
                for doctor in doctors
            ],
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

    async def _upload_avatar_file(
        self,
        doctor: DoctorModel,
        file_data: bytes,
        content_type: str | None,
        storage: S3StorageInterface,
    ) -> str:
        extension = self.allowed_avatar_content_types.get(content_type or "")
        if (
            not extension
            or not file_data
            or len(file_data) > self.max_avatar_size_bytes
        ):
            raise InvalidDoctorAvatarError

        file_name = f"doctors/{doctor.id}/avatar-{uuid4().hex}.{extension}"
        await storage.upload_file(file_name=file_name, file_data=file_data)
        return file_name

    async def _delete_old_avatar_file(
        self,
        old_avatar_key: str | None,
        current_avatar_key: str | None,
        storage: S3StorageInterface | None,
    ) -> None:
        if (
            not old_avatar_key
            or old_avatar_key == current_avatar_key
            or storage is None
        ):
            return
        try:
            await storage.delete_file(old_avatar_key)
        except BaseS3StorageError:
            return

    async def _serialize_doctor(
        self,
        doctor: DoctorModel,
        storage: S3StorageInterface | None = None,
    ) -> dict:
        avatar_url = doctor.avatar_url
        if avatar_url and storage:
            avatar_url = await storage.generate_presigned_url(avatar_url)

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
            "avatar_url": avatar_url,
            "created_at": doctor.created_at,
            "updated_at": doctor.updated_at,
        }

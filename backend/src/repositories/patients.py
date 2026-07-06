from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user import UserModel
from database.models.patients import PatientModel
from schemas.patients import PatientCreate, PatientUpdate


async def create_patient(
    db: AsyncSession,
    patient_data: PatientCreate,
) -> PatientModel:
    patient = PatientModel(**patient_data.model_dump())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient


async def get_patients(db: AsyncSession) -> list[dict]:
    result = await db.execute(
        select(
            PatientModel.id,
            PatientModel.user_id,
            UserModel.first_name,
            UserModel.last_name,
            UserModel.phone_number,
            PatientModel.date_of_birth,
        ).join(UserModel, PatientModel.user_id == UserModel.id)
    )

    return [dict(row._mapping) for row in result.all()]


async def get_patient_by_id(
    db: AsyncSession,
    patient_id: int,
) -> PatientModel | None:
    result = await db.execute(
        select(PatientModel).where(PatientModel.id == patient_id)
    )
    return result.scalar_one_or_none()


async def update_patient(
    db: AsyncSession,
    patient: PatientModel,
    patient_data: PatientUpdate,
) -> PatientModel:
    update_data = patient_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(patient, field, value)

    await db.commit()
    await db.refresh(patient)
    return patient


async def delete_patient(
    db: AsyncSession,
    patient: PatientModel,
) -> None:
    await db.delete(patient)
    await db.commit()

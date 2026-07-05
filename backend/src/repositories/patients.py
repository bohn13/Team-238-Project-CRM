from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import PatientModel


class PatientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, patient_id: int) -> PatientModel | None:
        return await self.session.scalar(
            select(PatientModel).where(PatientModel.patient_id == patient_id)
        )

    async def get_all(self) -> list[PatientModel]:
        result = await self.session.scalars(select(PatientModel))
        return list(result.all())

    def add_patient(self, patient: PatientModel) -> None:
        self.session.add(patient)

    async def delete_patient(self, patient: PatientModel) -> None:
        await self.session.delete(patient)

    async def flush(self) -> None:
        await self.session.flush()
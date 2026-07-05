from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Patient


class PatientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, patient_id: int) -> Patient | None:
        return await self.session.scalar(
            select(Patient).where(Patient.patient_id == patient_id)
        )

    async def get_all(self) -> list[Patient]:
        result = await self.session.scalars(select(Patient))
        return list(result.all())

    def add_patient(self, patient: Patient) -> None:
        self.session.add(patient)

    async def delete_patient(self, patient: Patient) -> None:
        await self.session.delete(patient)

    async def flush(self) -> None:
        await self.session.flush()

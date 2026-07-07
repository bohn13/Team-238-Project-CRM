from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.session_postgresql import get_postgresql_db
from repositories.patients import (
    create_patient,
    delete_patient,
    get_patient_by_id,
    get_patients,
    update_patient,
)
from schemas.patients import PatientCreate, PatientResponse, PatientUpdate, PatientListResponse

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_route(
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_postgresql_db),
):
    return await create_patient(db, patient_data)


@router.get("/", response_model=list[PatientListResponse])
async def get_patients_route(
    db: AsyncSession = Depends(get_postgresql_db),
):
    return await get_patients(db)


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient_route(
    patient_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
):
    patient = await get_patient_by_id(db, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return patient


@router.patch("/{patient_id}", response_model=PatientResponse)
async def update_patient_route(
    patient_id: int,
    patient_data: PatientUpdate,
    db: AsyncSession = Depends(get_postgresql_db),
):
    patient = await get_patient_by_id(db, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return await update_patient(db, patient, patient_data)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient_route(
    patient_id: int,
    db: AsyncSession = Depends(get_postgresql_db),
):
    patient = await get_patient_by_id(db, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    await delete_patient(db, patient)

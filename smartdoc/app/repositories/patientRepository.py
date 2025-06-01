from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from ..models.Patient import Patient

class PatientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, patient_data: dict) -> Patient:
        try:
            patient = Patient(**patient_data)
            self.db.add(patient)
            await self.db.commit()
            await self.db.refresh(patient)
            return patient
        except Exception as e:
            await self.db.rollback()
            raise e
    
    async def get_by_id(self, patient_id: str) -> Optional[Patient]:
        result = await self.db.execute(select(Patient).where(Patient.id == patient_id))
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: str) -> Optional[Patient]:
        result = await self.db.execute(select(Patient).where(Patient.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        result = await self.db.execute(select(Patient).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update(self, patient: Patient, update_data: dict) -> Patient:
        for field, value in update_data.items():
            if hasattr(patient, field) and value is not None:
                setattr(patient, field, value)
        await self.db.commit()
        await self.db.refresh(patient)
        return patient
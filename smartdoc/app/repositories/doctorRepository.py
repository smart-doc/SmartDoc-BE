from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from ..models.Doctor import Doctor

class DoctorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, doctor_data: dict) -> Doctor:
        try:
            doctor = Doctor(**doctor_data)
            self.db.add(doctor)
            await self.db.commit()
            await self.db.refresh(doctor)
            return doctor
        except Exception as e:
            await self.db.rollback()
            raise e
    
    async def get_by_id(self, user_id: str) -> Optional[Doctor]:
        result = await self.db.execute(select(Doctor).where(Doctor.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: str) -> Optional[Doctor]:
        result = await self.db.execute(select(Doctor).where(Doctor.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_hospital_id(self, hospital_id: str, skip: int = 0, limit: int = 100) -> List[Doctor]:
        result = await self.db.execute(
            select(Doctor).where(Doctor.hospital_id == hospital_id).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_all(self, hospital_id: Optional[str] = None,
 skip: int = 0, limit: int = 100) -> List[Doctor]:
        query = select(Doctor)
        if hospital_id:
            query = query.filter_by(hospital_id == hospital_id)
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update(self, doctor: Doctor, update_data: dict) -> Doctor:
        for field, value in update_data.items():
            if hasattr(doctor, field) and value is not None:
                setattr(doctor, field, value)
        
        await self.db.commit()
        await self.db.refresh(doctor)
        return doctor
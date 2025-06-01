from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Optional, List
from ..models.hospital import Hospital

class HospitalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, hospital_data: dict) -> Hospital:
        try:
            hospital = Hospital(**hospital_data)
            self.db.add(hospital)
            await self.db.commit()
            await self.db.refresh(hospital)
            return hospital
        except Exception as e:
            await self.db.rollback()
            raise e
    
    async def get_by_id(self, hospital_id: str) -> Optional[Hospital]:
        result = await self.db.execute(select(Hospital).where(Hospital.id == hospital_id))
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: str) -> Optional[Hospital]:
        result = await self.db.execute(select(Hospital).where(Hospital.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Hospital]:
        result = await self.db.execute(
            select(Hospital).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def update(self, hospital: Hospital, update_data: dict) -> Hospital:
        for field, value in update_data.items():
            if hasattr(hospital, field) and value is not None:
                setattr(hospital, field, value)
        
        await self.db.commit()
        await self.db.refresh(hospital)
        return hospital
    
    async def get_hospitals_for_registration(self) -> List[Dict]:
        hospitals = await self.get_all()
        return [
            {"id": str(hospital.id), "name": str(hospital.name)}
            for hospital in hospitals if hospital.status == "active" and hospital.subscription_status == "active"
        ]
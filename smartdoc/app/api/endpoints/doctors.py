from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.db import get_database
from app.repositories.doctorRepository import DoctorRepository
from app.repositories.hospitalRepository import HospitalRepository
from app.schemas.doctorSchema import DoctorResponse, DoctorUpdate
from app.dependencies.auth import get_current_user, get_current_hospital_admin
from app.models.user import User
from app.models import UserRole

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=List[DoctorResponse])
async def get_doctors(
    hospital_id: str = None,
    specialization: str = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_database)
):
    """Get doctors with optional filters"""
    doctors = await DoctorRepository(db).get_all(hospital_id, skip, limit)
    return doctors

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(
    doctor_id: str,
    db: AsyncSession = Depends(get_database)
):
    """Get doctor by ID"""
    doctor = await DoctorRepository(db).get_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(
    doctor_id: str,
    update_data: DoctorUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    """Update doctor details (Admin or self)"""
    doctor = await DoctorRepository(db).get_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    if current_user.role != UserRole.ADMIN and str(current_user.id) != str(doctor.user_id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_dict = update_data.dict(exclude_none=True)
    updated_doctor = await DoctorRepository(db).update(doctor, update_dict)
    return updated_doctor
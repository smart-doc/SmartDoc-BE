from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ...db import get_database
from ...repositories.hospitalRepository import HospitalRepository
from ...schemas.hospitalSchema import HospitalResponse, HospitalUpdate
from ...dependencies.auth import get_current_user, get_current_hospital_admin
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=List[HospitalResponse])
async def get_hospitals(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_database)
):
    """Get all hospitals"""
    hospital_repo = HospitalRepository(db)
    hospitals = await hospital_repo.get_all(skip, limit)
    return hospitals

@router.get("/{hospital_id}", response_model=HospitalResponse)
async def get_hospital(
    hospital_id: str,
    db: AsyncSession = Depends(get_database)
):
    """Get hospital by ID"""
    hospital_repo = HospitalRepository(db)
    hospital = await hospital_repo.get_by_id(hospital_id)
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )
    return hospital

@router.put("/{hospital_id}", response_model=HospitalResponse)
async def update_hospital(
    hospital_id: str,
    update_data: HospitalUpdate,
    current_user: User = Depends(get_current_hospital_admin),
    db: AsyncSession = Depends(get_database)
):
    """Update hospital details"""
    hospital_repo = HospitalRepository(db)
    hospital = await hospital_repo.get_by_id(hospital_id)
    
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )
    
    # Check if user owns this hospital (if not admin)
    if current_user.role != "admin" and str(hospital.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this hospital"
        )
    
    update_dict = update_data.dict(exclude_none=True)
    updated_hospital = await hospital_repo.update(hospital, update_dict)
    return updated_hospital
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List
# from ...db import get_database
# from ...schemas.patient import PatientCreate, PatientResponse, PatientUpdate
# from ...dependencies.auth import get_current_user
# from ...models.user import User

# router = APIRouter()

# @router.post("/register", response_model=dict)
# async def register_patient(
#     patient_data: PatientCreate,
#     db: AsyncSession = Depends(get_database)
# ):
#     """Patient self-registration"""
#     # Implementation would go here
#     pass

# @router.get("/me", response_model=PatientResponse)
# async def get_my_profile(
#     current_user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_database)
# ):
#     """Get current patient's profile"""
#     # Implementation would go here
#     pass

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_database
from app.repositories.patientRepository import PatientRepository
from app.schemas.patientSchema import PatientResponse, PatientUpdate
from app.dependencies.auth import get_current_user, get_current_patient
from app.models.user import User

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/me", response_model=PatientResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_patient),
    db: AsyncSession = Depends(get_database)
):
    """Get current patient's profile"""
    patient = await PatientRepository(db).get_by_user_id(str(current_user.id))
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient

@router.put("/me", response_model=PatientResponse)
async def update_my_profile(
    update_data: PatientUpdate,
    current_user: User = Depends(get_current_patient),
    db: AsyncSession = Depends(get_database)
):
    """Update current patient's profile"""
    patient = await PatientRepository(db).get_by_user_id(str(current_user.id))
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    update_dict = update_data.dict(exclude_none=True)
    updated_patient = await PatientRepository(db).update(patient, update_dict)
    return updated_patient
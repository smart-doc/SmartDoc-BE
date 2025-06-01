from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.db import get_database
from app.services.authService import AuthService
from app.services.profileService import ProfileService
from app.schemas.userSchema import UserLogin, Token, ForgotPasswordRequest, ResetPasswordRequest, UserResponse
from app.schemas.patientSchema import PatientCreate
from app.schemas.hospitalSchema import HospitalCreate
from app.schemas.doctorSchema import DoctorCreate
from app.schemas.userSchema import AdminCreate
from app.dependencies.auth import get_current_user, get_current_admin
from app.models.user import User
from typing import List, Dict
from app.repositories.hospitalRepository import HospitalRepository
from ...models import UserRole

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/admin/register", response_model=Dict)
async def create_admin(
    admin_data: AdminCreate,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_database)
):
    """Create admin account (Admin only)"""
    auth_service = AuthService(db)
    return await auth_service.create_admin(admin_data)

@router.post("/hospital/register", response_model=Dict)
async def create_hospital_account(
    hospital_data: HospitalCreate,
    db: AsyncSession = Depends(get_database)
):
    """Hospital registration (Public)"""
    auth_service = AuthService(db)
    return await auth_service.create_hospital_account(hospital_data)

@router.get("/hospitals", response_model=List[Dict])
async def get_hospitals_for_registration(
    db: AsyncSession = Depends(get_database)
):
    """Get list of active hospitals for doctor registration"""
    hospital_repo = HospitalRepository(db)
    return await hospital_repo.get_hospitals_for_registration()

@router.post("/doctor/register", response_model=Dict)
async def create_doctor_account(
    doctor_data: DoctorCreate,
    db: AsyncSession = Depends(get_database)
):
    """Doctor registration (Public, requires hospital_id)"""
    auth_service = AuthService(db)
    return await auth_service.create_doctor_account(doctor_data)

@router.post("/patient/register", response_model=Dict)
async def create_patient_account(
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_database)
):
    """Patient self-registration (Public)"""
    auth_service = AuthService(db)
    return await auth_service.create_patient_account(patient_data)

@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_database)
):
    """User login"""
    auth_service = AuthService(db)
    return await auth_service.login(login_data)

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """User logout"""
    return {"message": "Successfully logged out"}

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_database)
):
    """Request password reset"""
    auth_service = AuthService(db)
    return await auth_service.forgot_password(request.email)

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_database)
):
    """Reset password"""
    auth_service = AuthService(db)
    return await auth_service.reset_password(request.token, request.new_password)

@router.get("/profiles", response_model=List[Dict])
async def get_all_profiles(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_database)
):
    """Get all user profiles (Admin only)"""
    profile_service = ProfileService(db)
    return await profile_service.get_all_profiles(skip, limit)

@router.get("/profile/{user_id}", response_model=Dict)
async def get_user_profile(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    """Get specific user profile"""
    if current_user.role != UserRole.ADMIN and str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    profile_service = ProfileService(db)
    return await profile_service.get_user_profile(user_id)

@router.get("/profile/me", response_model=Dict)
async def get_signed_in_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    """Get current user's profile"""
    profile_service = ProfileService(db)
    return await profile_service.get_signed_in_user_profile(current_user)

@router.put("/profile/{user_id}", response_model=Dict)
async def update_user_profile(
    user_id: str,
    update_data: Dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    """Update user profile"""
    profile_service = ProfileService(db)
    return await profile_service.update_user_profile(user_id, update_data, current_user)

@router.post("/otp")
async def send_otp(phone: str, db: AsyncSession = Depends(get_database)):
    auth_service = AuthService(db)
    return await auth_service.send_otp(phone)
    # return hospital_schema.HospitalResponse.from_orm(hospital).dict(exclude_unset=True)

@router.post("/sync")
async def sync_data(data: Dict, current_user: User = Depends(get_current_user)):
    # Process offline data
    return {"message": "Data synced"}

# data_consent: bool = Field(..., description="Consent for data processing per NDPR")



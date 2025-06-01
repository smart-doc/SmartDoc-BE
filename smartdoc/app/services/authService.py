from ..schemas import doctorSchema, hospitalSchema, patientSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import Optional, Dict
import secrets
import redis
from ..schemas.doctorSchema import DoctorCreate, DoctorResponse
from ..schemas.patientSchema import PatientCreate, PatientResponse
from ..schemas.hospitalSchema import HospitalCreate, HospitalResponse
from app.repositories.userRepository import UserRepository
from app.repositories.hospitalRepository import HospitalRepository
from app.repositories.doctorRepository import DoctorRepository
from app.repositories.patientRepository import PatientRepository
from ....smartdoc.app.security import create_access_token, create_refresh_token
from ..schemas.userSchema import UserLogin, UserResponse, Token, AdminCreate, UserRole, UserStatus
from app.models import UserRole
import uuid
from ..models.__init__ import SubscriptionStatus
import redis.asyncio as aioredis
from datetime import datetime
# Redis client for storing reset tokens
redis_client = redis.Redis.from_url("redis://localhost:6379", decode_responses=True)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.hospital_repo = HospitalRepository(db)
        self.doctor_repo = DoctorRepository(db)
        self.patient_repo = PatientRepository(db)
    
    async def create_admin(self, admin_data: AdminCreate) -> Dict:
        existing_user = await self.user_repo.get_by_id(admin_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user = await self.user_repo.create_user(
            email=admin_data.email,
            password=admin_data.password,
            role=UserRole.ADMIN
        )
        
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return {
            "user": UserResponse.from_orm(user),
            "tokens": Token(
                access_token=access_token,
                refresh_token=refresh_token
            )
        }
    
    async def create_hospital_account(self, hospital_data: HospitalCreate) -> Dict:
        existing_user = await self.user_repo.get_by_id(hospital_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user account
        user = await self.user_repo.create_user(
            email=hospital_data.email,
            password=hospital_data.password,
            role=UserRole.HOSPITAL
        )
        
        # Create hospital profile
        hospital_dict = hospital_data.dict(exclude={"email", "password"})
        hospital_dict["user_id"] = str(user.id)
        
        hospital = await self.hospital_repo.create(hospital_dict)
        
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return {
            "user": UserResponse.from_orm(user),
            "hospital": HospitalResponse.from_orm(hospital),
            "tokens": Token(
                access_token=access_token,
                refresh_token=refresh_token
            )
        }
    
    async def create_doctor_account(self, doctor_data: DoctorCreate) -> Dict:
        # Validate hospital
        hospital = await self.hospital_repo.get_by_id(doctor_data.hospital_id)
        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")
        if hospital.subscription_status != SubscriptionStatus.ACTIVE:
            raise HTTPException(status_code=403, detail="Hospital subscription is not active")
        
        existing_user = await self.user_repo.get_by_id(doctor_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user account
        user = await self.user_repo.create_user(
            email=doctor_data.email,
            password=doctor_data.password,
            role=UserRole.DOCTOR
        )
        
        # Create doctor profile
        doctor_dict = doctor_data.dict(exclude={"email", "password"})
        doctor_dict["user_id"] = str(user.id)
        
        doctor = await self.doctor_repo.create(doctor_dict)
        
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return {
            "user": UserResponse.from_orm(user),
            "doctor": DoctorResponse.from_orm(doctor),
            "tokens": Token(
                access_token=access_token,
                refresh_token=refresh_token
            )
        }
    
    async def create_patient_account(self, patient_data: PatientCreate) -> Dict:
        existing_user = await self.user_repo.get_by_id(patient_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user account
        user = await self.user_repo.create_user(
            email=patient_data.email,
            password=patient_data.password,
            role=UserRole.PATIENT
        )
        
        # Create patient profile
        patient_dict = patient_data.dict(exclude={"email", "password"})
        patient_dict["user_id"] = str(user.id)
        
        patient = await self.patient_repo.create(patient_dict)
        
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return {
            "user": UserResponse.from_orm(user),
            "patient": PatientResponse.from_orm(patient),
            "tokens": Token(
                access_token=access_token,
                refresh_token=refresh_token
            )
        }
    
    async def login(self, login_data: UserLogin) -> Token:
        user = await self.user_repo.authenticate(login_data.email, login_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Check hospital subscription for doctors
        if user.role == UserRole.DOCTOR:
            doctor = await self.doctor_repo.get_by_user_id(str(user.id))
            if doctor:
                hospital = await self.hospital_repo.get_by_id(doctor.hospital_id)
                if hospital and hospital.subscription_status != SubscriptionStatus.ACTIVE:
                    raise HTTPException(status_code=403, detail="Hospital subscription is not active")
        
        if user.status != UserStatus.ACTIVE:
            raise HTTPException(status_code=403, detail="User account is not active")
        
        # Update last_login
        user.last_login = datetime.utcnow()
        await self.db.commit()
        
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    async def forgot_password(self, email: str) -> Dict:
        user = await self.user_repo.get_by_id(email)
        if not user:
            return {"message": "If email exists, a reset link has been sent"}
        
        reset_token = secrets.token_urlsafe(32)
        redis_client.setex(f"reset_token:{reset_token}", 3600, str(user.id))
        
        # TODO: Send email or WhatsApp OTP
        return {"message": "success"}
    
    async def reset_password(self, token: str, new_password: str) -> Dict:
        user_id = redis_client.get(f"reset_token:{token}")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        await self.user_repo.update(user, new_password)
        redis_client.delete(f"reset_token:{token}")
        
        return {"message": "Password reset successful"}

# async def send_otp(self, phone: str) -> Dict:
#     from twilio.rest import Client
#     patient = await self.patient_repo.get_by_phone(phone)
#     if not patient:
#         raise HTTPException(status_code=404, detail="Patient not found")
#     otp = secrets.token_digits(6)
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         body=f"Your SmartDoc OTP is {otp}",
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone
#     )
#     redis_client.setex(f"otp:{phone}", 300, otp)
#     return {"message": "OTP sent"}
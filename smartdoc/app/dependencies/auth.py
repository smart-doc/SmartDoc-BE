from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_database
from app.security import verify_token
from app.repositories.userRepository import UserRepository
from app.repositories.doctorRepository import DoctorRepository
from app.repositories.hospitalRepository import HospitalRepository
from app.models.user import User
from app.models import UserRole
from app.models.__init__ import SubscriptionStatus

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_database)
) -> User:
    token = credentials.credentials
    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    
    if user is None or user.status != "active":
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    # Check hospital subscription for doctors
    if user.role == UserRole.DOCTOR:
        doctor = await DoctorRepository(db).get_by_user_id(user_id)
        if doctor:
            hospital = await HospitalRepository(db).get_by_id(doctor.hospital_id)
            if hospital and hospital.subscription_status != SubscriptionStatus.ACTIVE:
                raise HTTPException(status_code=403, detail="Hospital subscription is not active")
    
    return user

async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def get_current_hospital(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.HOSPITAL:
        raise HTTPException(status_code=403, detail="Hospital access required")
    return current_user

async def get_current_doctor(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Doctor access required")
    return current_user

async def get_current_patient(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Patient access required")
    return current_user

# async def send_otp(self, phone: str) -> Dict:
#     patient = await self.patient_repo.get_by_phone(phone)
#     if not patient:
#         raise HTTPException(status_code=404, detail="Patient not found")
#     otp = secrets.token_digits(6)
#     from twilio.rest import Client
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         body=f"Your SmartDoc OTP is {otp}",
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone
#     )
#     redis_client.setex(f"otp:{phone}", 300, otp)
#     return {"message": "OTP sent"}
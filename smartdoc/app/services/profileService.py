from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List, Dict
from app.repositories.userRepository import UserRepository
from app.repositories.doctorRepository import DoctorRepository
from app.repositories.patientRepository import PatientRepository
from app.repositories.hospitalRepository import HospitalRepository
from app.models.user import User
from app.models import UserRole
from app.schemas.userSchema import UserResponse
from app.schemas import hospitalSchema, doctorSchema, patientSchema

class ProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.hospital_repo = HospitalRepository(db)
        self.doctor_repo = DoctorRepository(db)
        self.patient_repo = PatientRepository(db)
    
    async def get_all_profiles(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        users = await self.user_repo.get_all_users(skip, limit)
        profiles = []
        
        for user in users:
            profile_data = UserResponse.from_orm(user).dict()
            if user.role == UserRole.HOSPITAL:
                hospital = await self.hospital_repo.get_by_id(str(user.id))
                if hospital:
                    profile_data["hospital"] = hospitalSchema.HospitalResponse.from_orm(hospitalSchema).dict()
            elif user.role == UserRole.DOCTOR:
                doctor = await self.doctor_repo.get_by_id(str(user.id))
                if doctor:
                    profile_data["doctor"] = doctorSchema.DoctorResponse.from_orm(doctorSchema).dict()
            elif user.role == UserRole.PATIENT:
                patient = await self.patient_repo.get_by_id(str(user.id))
                if patient:
                    profile_data["patient"] = patientSchema.PatientResponse.from_orm(patientSchema).dict()
            
            profiles.append(profile_data)
        
        return profiles
    
    async def get_user_profile(self, user_id: str) -> Dict:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        profile_data = UserResponse.from_orm(user).dict()
        
        if user.role == UserRole.HOSPITAL:
            hospital = await self.hospital_repo.get_by_user_id(user_id)
            if hospital:
                profile_data["hospital"] = hospitalSchema.HospitalResponse.from_orm(hospitalSchema).dict()
        elif user.role == UserRole.DOCTOR:
            doctor = await self.doctor_repo.get_by_user_id(user_id)
            if doctor:
                profile_data["doctor"] = doctorSchema.DoctorResponse.from_orm(doctorSchema).dict()
        elif user.role == UserRole.PATIENT:
            patient = await self.patient_repo.get_by_user_id(user_id)
            if patient:
                profile_data["patient"] = patientSchema.PatientResponse.from_orm(patientSchema).dict()
        
        return profile_data
    
    async def get_signed_in_user_profile(self, current_user: User) -> Dict:
        return await self.get_user_profile(str(current_user.id))
    
    async def update_user_profile(self, user_id: str, update_data: Dict, current_user: User) -> Dict:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if current_user.role != UserRole.ADMIN and str(current_user.id) != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this profile")
        
        if "email" in update_data:
            existing_user = await self.user_repo.get_by_id(update_data["email"])
            if existing_user and str(existing_user.id) != user_id:
                raise HTTPException(status_code=400, detail="Email already registered")
            user.email = update_data["email"]
            await self.db.commit()
            await self.db.refresh(user)
        
        if user.role == UserRole.HOSPITAL and "hospital" in update_data:
            hospital = await self.hospital_repo.get_by_user_id(user_id)
            if hospital:
                await self.hospital_repo.update(hospital, update_data["hospital"])
        elif user.role == UserRole.DOCTOR and "doctor" in update_data:
            doctor = await self.doctor_repo.get_by_user_id(user_id)
            if doctor:
                await self.doctor_repo.update(doctor, update_data["doctor"])
        elif user.role == UserRole.PATIENT and "patient" in update_data:
            patient = await self.patient_repo.get_by_user_id(user_id)
            if patient:
                await self.patient_repo.update(patient, update_data["patient"])
        
        return await self.get_user_profile(user_id)
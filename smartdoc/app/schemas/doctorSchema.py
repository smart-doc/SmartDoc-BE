from pydantic import BaseModel
from typing import Optional, List
# from datetime import date, time, datetime
# from decimal import Decimal
from ..models import Gender, UserStatus

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    specialization: str
    sub_specialization: Optional[str] = None
    # years_of_experience: Optional[int] = None
    # education: Optional[str] = None
    # certifications: Optional[List[str]] = None
    # languages_spoken: Optional[List[str]] = None
    # consultation_fee: Optional[Decimal] = None
    # available_days: Optional[List[str]] = None
    # available_hours_start: Optional[time] = None
    # available_hours_end: Optional[time] = None
    bio: Optional[str] = None
    # is_accepting_patients: bool = True

class DoctorCreate(DoctorBase):
    email: str
    password: str
    hospital_id: str
    # employee_id: Optional[str] = None
    # date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None

class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    sub_specialization: Optional[str] = None
    # years_of_experience: Optional[int] = None
    # education: Optional[str] = None
    # certifications: Optional[List[str]] = None
    # languages_spoken: Optional[List[str]] = None
    # consultation_fee: Optional[Decimal] = None
    # available_days: Optional[List[str]] = None
    # available_hours_start: Optional[time] = None
    # available_hours_end: Optional[time] = None
    bio: Optional[str] = None
    # is_accepting_patients: Optional[bool] = None

class DoctorResponse(DoctorBase):
    id: str
    user_id: str
    hospital_id: str
    gender: Optional[Gender] = None
    status: UserStatus

# class ConsultationBase(BaseModel):
#     patient_id: str
#     doctor_id: str
#     hospital_id: str
#     consultation_type: str
#     symptoms: Optional[str]
#     ai_recommendation_reason: Optional[str]
#     status: str = "scheduled"

# class ConsultationCreate(ConsultationBase):
#     pass

# class ConsultationResponse(ConsultationBase):
#     id: str
#     scheduled_at: Optional[datetime]
#     created_at: datetime

    class Config:
        from_attributes = True
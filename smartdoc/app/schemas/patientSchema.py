from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal
from ..models import Gender, BloodGroup

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    date_of_birth: date
    gender: Gender
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    blood_group: Optional[BloodGroup] = None
    height_cm: Optional[Decimal] = None
    weight_kg: Optional[Decimal] = None
    preferred_language: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    data_consent: bool = True  # NDPR compliance

class PatientCreate(PatientBase):
    email: str
    password: str

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    blood_group: Optional[BloodGroup] = None
    height_cm: Optional[Decimal] = None
    weight_kg: Optional[Decimal] = None
    preferred_language: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    data_consent: bool = True  # NDPR compliance

class PatientResponse(PatientBase):
    id: str
    user_id: str
    
    class Config:
        from_attributes = True
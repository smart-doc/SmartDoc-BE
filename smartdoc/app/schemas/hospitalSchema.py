from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from ..models.__init__ import SubscriptionStatus

class HospitalBase(BaseModel):
    name: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    registration_number: str
    website: Optional[str] = None
    description: Optional[str] = None
    specialties: Optional[List[str]] = None
    emergency_services: bool = False
    bed_capacity: Optional[int] = None
    founded_year: Optional[int] = None
    accreditation: Optional[str] = None
    # subscription_status: Optional[SubscriptionStatus] = None  # New

class HospitalCreate(HospitalBase):
    name: str
    phone: str
    address: str
    email: str
    password: str

class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    specialties: Optional[List[str]] = None
    emergency_services: Optional[bool] = None
    bed_capacity: Optional[int] = None
    founded_year: Optional[int] = None
    accreditation: Optional[str] = None
    # subscription_status: Optional[SubscriptionStatus] = None  # New

class HospitalResponse(HospitalBase):
    id: str
    user_id: str
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    status: str
    
    class Config:
        from_attributes = True
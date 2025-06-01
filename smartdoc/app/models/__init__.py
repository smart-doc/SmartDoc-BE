from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, DECIMAL, Date, Time, Enum as SQLEnum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
import uuid

Base = declarative_base()

class UserRole(str, Enum):
    ADMIN = "admin"
    HOSPITAL = "hospital"  # Changed from HOSPITAL_ADMIN
    DOCTOR = "doctor"
    PATIENT = "patient"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class SubscriptionStatus(str, Enum):  # New
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"

class ConsultationStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ConsultationType(str, Enum):
    AI_RECOMMENDED = "ai_recommended"
    DIRECT_BOOKING = "direct_booking"
    EMERGENCY = "emergency"
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, DECIMAL, Date, Time, Enum as SQLEnum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
import uuid
from .__init__ import Gender, UserStatus
from ..db.db import Base


class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    hospital_id = Column(UUID(as_uuid=True), ForeignKey("hospitals.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(SQLEnum(Gender))
    # medical_license_number = Column(String(100), unique=True, nullable=False)
    specialization = Column(String(100), nullable=False)
    sub_specialization = Column(String(100))
    # years_of_experience = Column(Integer)
    # education = Column(Text)
    # certifications = Column(ARRAY(String))
    # languages_spoken = Column(ARRAY(String))
    # consultation_fee = Column(DECIMAL(10, 2))
    # available_days = Column(ARRAY(String))
    # available_hours_start = Column(Time)
    # available_hours_end = Column(Time)
    bio = Column(Text)
    # profile_image_url = Column(String(500))
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE)  # Renamed is_accepting_patients to status
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="doctor")
    hospital = relationship("Hospital", back_populates="doctors")
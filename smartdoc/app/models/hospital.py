from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, DECIMAL, Date, Time, Enum as SQLEnum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
import uuid
from .__init__ import UserStatus
from ..db.db import Base

class Hospital(Base):
    __tablename__ = "hospitals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    registration_number = Column(String(100), unique=True, nullable=False)
    website = Column(String(255))
    description = Column(Text)
    specialties = Column(ARRAY(String))
    emergency_services = Column(Boolean, default=False)
    bed_capacity = Column(Integer)
    founded_year = Column(Integer)
    accreditation = Column(String(255))
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE)
    # subscription_status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)  # New
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital")

from sqlalchemy import CheckConstraint, Column, String, Integer, DateTime, Boolean, Text, DECIMAL, Date, Time, Enum as SQLEnum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
import uuid
from .__init__ import ConsultationType, ConsultationStatus
from ..db.db import Base

class Consultation(Base):
    __tablename__ = "consultations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False)
    hospital_id = Column(UUID(as_uuid=True), ForeignKey("hospitals.id"), nullable=False)
    consultation_type = Column(SQLEnum(ConsultationType), nullable=False)
    symptoms = Column(Text)
    ai_recommendation_reason = Column(Text)
    status = Column(SQLEnum(ConsultationStatus), default=ConsultationStatus.SCHEDULED)
    scheduled_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    consultation_notes = Column(Text)
    diagnosis = Column(Text)
    prescribed_medications = Column(JSONB)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(Date)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    patient_feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    
    # Relationships
    patient = relationship("Patient")
    doctor = relationship("Doctor")
    hospital = relationship("Hospital")
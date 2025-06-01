from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, DECIMAL, Date, Time, Enum as SQLEnum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
import uuid
from ..db.db import Base


class MedicalHistory(Base):
    __tablename__ = "medical_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    chronic_conditions = Column(ARRAY(String))
    allergies = Column(ARRAY(String))
    allergy_severity = Column(SQLEnum('mild', 'moderate', 'severe', name='severity_enum'))
    current_medications = Column(JSONB)
    past_surgeries = Column(JSONB)
    family_history_diabetes = Column(Boolean)
    family_history_heart_disease = Column(Boolean)
    family_history_cancer = Column(Boolean)
    family_history_hypertension = Column(Boolean)
    family_history_mental_health = Column(Boolean)
    family_history_other = Column(Text)
    smoking_status = Column(SQLEnum('never', 'former', 'current', name='smoking_enum'))
    alcohol_consumption = Column(SQLEnum('never', 'occasional', 'moderate', 'heavy', name='alcohol_enum'))
    exercise_frequency = Column(SQLEnum('none', 'rare', 'weekly', 'daily', name='exercise_enum'))
    pregnancy_history = Column(JSONB)
    menstrual_history = Column(Text)
    vaccination_records = Column(JSONB)
    other_medical_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="medical_history")
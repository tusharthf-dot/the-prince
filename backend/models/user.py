from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    input_type = Column(String)  # text, speech, image
    raw_input = Column(Text)
    clarity_score = Column(Float)
    confidence_score = Column(Float)
    persuasiveness_score = Column(Float)
    structure_score = Column(Float)
    overall_score = Column(Float)
    feedback = Column(Text)
    principle_applied = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    total_sessions = Column(Integer, default=0)
    avg_clarity = Column(Float, default=0.0)
    avg_confidence = Column(Float, default=0.0)
    avg_persuasiveness = Column(Float, default=0.0)
    weak_areas = Column(Text)
    improvement_rate = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
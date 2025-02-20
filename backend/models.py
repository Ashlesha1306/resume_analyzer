from sqlalchemy import Column, Integer, String, Text, ARRAY
from .database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    core_skills = Column(ARRAY(String))
    soft_skills = Column(ARRAY(String))
    work_experience = Column(Text)
    education = Column(Text)
    resume_rating = Column(Integer)
    improvement_areas = Column(Text)
    upskill_suggestions = Column(Text)
    file_name = Column(String)

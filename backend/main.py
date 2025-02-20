from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .database import get_db, engine
from .models import Resume, Base
from .extract import extract_text_from_pdf, extract_info
from .llm import analyze_resume

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ResumeResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    core_skills: list
    soft_skills: list
    work_experience: str
    education: str
    resume_rating: int
    improvement_areas: str
    upskill_suggestions: str
    file_name: str

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads a resume, extracts structured information, 
    and stores it in the PostgreSQL database.
    """
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from resume
    text = extract_text_from_pdf(file_path)
    extracted_info = extract_info(text)

    # Analyze resume using LLM
    analysis = analyze_resume(text)

    # Save to database
    resume = Resume(
        file_name=file.filename,
        name=extracted_info["name"],
        email=extracted_info["email"],
        phone=extracted_info["phone"],
        core_skills=extracted_info["core_skills"],
        soft_skills=analysis.get("soft_skills", []),
        work_experience=analysis.get("work_experience", ""),
        education=analysis.get("education", ""),
        resume_rating=analysis.get("resume_rating", 7),  # Default rating if missing
        improvement_areas=analysis.get("improvement_areas", ""),
        upskill_suggestions=analysis.get("upskill_suggestions", ""),
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume

@app.get("/resumes/")
def get_all_resumes(db: Session = Depends(get_db)):
    """
    Retrieves all past uploaded resumes from the database.
    """
    resumes = db.query(Resume).all()
    return resumes

@app.get("/resume/{resume_id}")
def get_resume_by_id(resume_id: int, db: Session = Depends(get_db)):
    """
    Fetches a specific resume's extracted data by ID.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        return {"error": "Resume not found"}
    return resume

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime, Text, Boolean, case, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
import smtplib
from email.mime.text import MIMEText
import random
import os
from dotenv import load_dotenv
import enum
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
from fastapi import UploadFile, File
import shutil
from sqlalchemy import Text
from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, String, DateTime, Date, Text
from datetime import datetime
import random
import smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel
from datetime import date
from sqlalchemy import ForeignKey
from fastapi import File, UploadFile
import os
from sqlalchemy import Float
import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, validator
import re
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from fastapi.staticfiles import StaticFiles


# Load your trained model
import os

model_path = os.path.join(os.path.dirname(__file__), "model.h5")
model = tf.keras.models.load_model(model_path)

print("✅ Model Loaded Successfully")
# Class labels (VERY IMPORTANT ORDER)
class_names = ["NORMAL", "PNEUMONIA"]

UPLOAD_DIR = "uploads"
FEEDBACK_UPLOAD_DIR = "feedback_uploads"
os.makedirs(FEEDBACK_UPLOAD_DIR, exist_ok=True)
os.makedirs("profile_photos", exist_ok=True)
os.makedirs("uploads", exist_ok=True)





# ==============================
# EMAIL CONFIGURATION
# ==============================

# =====================================================
# LOAD ENV
# =====================================================
load_dotenv()

# =====================================================
# DATABASE CONFIG
# =====================================================
# read URL from env so it can be changed without editing source
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/chestxraydb")

# helper to create engine with fallback if the primary DB is unreachable
from sqlalchemy.exc import OperationalError

def create_db_engine(url: str):
    try:
        eng = create_engine(url, pool_pre_ping=True)
        # test connection immediately so early failures are detected
        with eng.connect() as conn:
            pass
        print(f"[db] connected to {url}")
        return eng
    except Exception as err:  # catch network/connection errors
        print(f"[db] could not connect to {url}: {err}")
        # fallback to sqlite file so the app can still start
        fallback_url = "sqlite:///./fallback.db"
        print(f"[db] falling back to {fallback_url}")
        eng = create_engine(fallback_url, pool_pre_ping=True)
        return eng

engine = create_db_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

app = FastAPI(title="Hospital Doctor + Triage Full System")

# allow requests coming from any host/IP (enables accessing from mobile devices on the
# same LAN).  Without this some ASGI servers will reject requests when the Host
# header contains the machine's local IP, resulting in an “IP address is invalid”
# or “Invalid HTTP_HOST header” message.
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

# allow any host/IP in Host header (see comment above)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# open CORS so a mobile webview or external frontend can hit the API without
# being blocked by the browser.  allow_origins=['*'] is permissive but okay for
# local development on the LAN.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/profile_photos", StaticFiles(directory="profile_photos"), name="profile_photos")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# =====================================================
# ENUMS
# =====================================================
class PriorityEnum(str, enum.Enum):
    CRITICAL = "CRITICAL"
    URGENT = "URGENT"
    ROUTINE = "ROUTINE"

class StatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class DecisionEnum(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

# =====================================================
# MODELS
# =====================================================
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    hospital_email = Column(String(150), unique=True)
    phone_number = Column(String(20), unique=True)

    role_requested = Column(String(100))
    password = Column(String(255))
    theme = Column(String(20), default="Light")
    notifications_enabled = Column(Boolean, default=True)
    profile_photo = Column(String(255), nullable=True)
    preferred_language = Column(String(50), default="English (US)")
    specialization = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())


class DoctorPrivacySettings(Base):
    __tablename__ = "doctor_privacy_settings"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, nullable=False)
    data_sharing = Column(Boolean, default=False)
    history_retention = Column(Boolean, default=True)
    diagnostics = Column(Boolean, default=True)



class Technician(Base):
    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(150), unique=True)
    phone_number = Column(String(20))
    role_requested = Column(String(50))
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    profile_photo = Column(String(255), nullable=True)

class TechnicianPasswordResetOTP(Base):
    __tablename__ = "technician_password_reset_otp"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150))
    otp_code = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)




class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer)  # ADD THIS LINE

    scan_id = Column(String(50))
    patient = Column(String(100))
    scan_type = Column(String(100))
    status = Column(String(50))
    scan_status = Column(String(50)) 
    scan_code = Column(String(50), unique=True, index=True)
    review_status = Column(String(50), nullable=True)
    quality_validated_at = Column(DateTime, nullable=True)
    image_path = Column(String(255), nullable=True)
    uploaded_at = Column(DateTime, nullable=True)
    exposure_level = Column(String(50), nullable=True)
    sharpness_level = Column(String(50), nullable=True)
    technician_id = Column(Integer)  
    created_at = Column(DateTime, default=datetime.utcnow)


class ScanPreparation(Base):
    __tablename__ = "scan_preparations"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))

    position_patient = Column(Boolean, default=False)
    proper_distance = Column(Boolean, default=False)
    radiation_safety = Column(Boolean, default=False)
    remove_metal = Column(Boolean, default=False)
    calibration_verified = Column(Boolean, default=False)
    exposure_settings = Column(Boolean, default=False)
    patient_id = Column(Integer)  
    created_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from datetime import datetime

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patient.id"))
    patient_name = Column(String(100))
    patient_age = Column(Integer)

    diagnosis = Column(String(255))
    priority = Column(String(50))

    image_url = Column(String(255))

    ai_findings = Column(Text)
    ai_confidence = Column(Integer)

    final_diagnosis = Column(String(255))

    doctor_notes = Column(Text)

    decision = Column(String(50), default="PENDING")
    status = Column(String(50), default="PENDING")

    report_id = Column(String(50))

    finalized = Column(Boolean, default=False)

    signed_by = Column(String(150))

    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)

    case_code = Column(String(20))

    ai_result = Column(String(100))
    scan_id = Column(Integer)
    doctor_id = Column(Integer)


class Study(Base):
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    session_id = Column(String(100), unique=True)
    dicom_path = Column(String(255))
    file_size_mb = Column(Float)
    upload_progress = Column(Integer, default=0)
    study_status = Column(String(50), default="Processing")
    assigned_doctor = Column(String(100))
    encrypted = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PACSArchive(Base):
    __tablename__ = "pacs_archives"

    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("studies.id"))
    archive_location = Column(String(255))
    archive_status = Column(String(50), default="Archived")
    archived_at = Column(DateTime, default=datetime.utcnow)

class RISWorklist(Base):
    __tablename__ = "ris_worklist"

    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("studies.id"))
    patient_id = Column(Integer)
    worklist_status = Column(String(50), default="Pending Review")
    assigned_doctor = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("studies.id"))
    ai_status = Column(String(50), default="Processing")
    confidence_score = Column(Float)
    ai_result = Column(Text)
    processed_at = Column(DateTime, default=datetime.utcnow)


class RadiologistReview(Base):
    __tablename__ = "radiologist_reviews"

    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("studies.id"))
    doctor_name = Column(String(100))
    review_status = Column(String(50), default="Pending")
    review_notes = Column(Text)
    reviewed_at = Column(DateTime)

# =====================================================
# PATIENT MODEL
# =====================================================
from datetime import date

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255))
    date_of_birth = Column(Date)
    gender = Column(String(10))

    mrn = Column(String(50), unique=True)
    patient_code = Column(String(50), unique=True)   # ADD THIS

    reason_for_xray = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

class TriageCase(Base):
    __tablename__ = "triage_cases"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    patient_name = Column(String(100))
    patient_age = Column(Integer)
    diagnosis = Column(String(255))
    priority = Column(Enum(PriorityEnum))
    image_url = Column(String(255))
    ai_findings = Column(Text)
    ai_confidence = Column(Integer)
    final_diagnosis = Column(String(255))
    doctor_id = Column(Integer)
    doctor_notes = Column(Text)
    decision = Column(Enum(DecisionEnum), default=DecisionEnum.PENDING)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    report_id = Column(String(50))
    finalized = Column(Boolean, default=False)
    signed_by = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)
    case_code = Column(String(20))
    ai_result = Column(String(100))


Base.metadata.create_all(bind=engine)

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255))
    answer = Column(Text)


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, nullable=False)
    message = Column(Text)
    status = Column(String(20), default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)

class DoctorSession(Base):
    __tablename__ = "doctor_sessions"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, nullable=False)
    token = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    technician_id = Column(Integer)
    feedback_type = Column(String(50))
    subject = Column(String(255))
    description = Column(Text)
    screenshot_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

# =====================================================
# DB Dependency
# =====================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/case/{case_id}")
def get_case_by_id(case_id: int, db: Session = Depends(get_db)):
    """Fetch a single triage case by its ID, with patient details and robust fallback."""
    
    # Try picking from TriageCase with outerjoin to Patient for extra data
    result = db.query(TriageCase, Patient).outerjoin(
        Patient, TriageCase.patient_id == Patient.id
    ).filter(TriageCase.id == case_id).first()
    
    if result:
        case, patient = result
        
        # Parse findings JSON if it exists
        findings_list = []
        if case.ai_findings:
            try:
                import json
                findings_list = json.loads(case.ai_findings)
            except:
                findings_list = []

        return {
            "id": case.id,
            "case_code": case.case_code,
            "patient_id": case.patient_id,
            "patient_name": case.patient_name,
            "patient_age": case.patient_age,
            "patient_gender": patient.gender if patient else (case.patient_gender if hasattr(case, 'patient_gender') else "N/A"),
            "diagnosis": case.diagnosis,
            "priority": case.priority.value if hasattr(case.priority, 'value') else str(case.priority),
            "ai_result": case.final_diagnosis or "No specific findings detected.",
            "ai_confidence": (case.ai_confidence / 100) if case.ai_confidence is not None else 0,
            "ai_findings": case.ai_findings,
            "findings": findings_list,
            "status": case.status.value if hasattr(case.status, 'value') else str(case.status),
            "decision": case.decision.value if hasattr(case.decision, 'value') else str(case.decision),
            "image_url": case.image_url,
            "created_at": case.created_at,
            "clinical_notes": case.doctor_notes or "Clinical correlation recommended.",
            "final_diagnosis": case.final_diagnosis,
            "doctor_id": case.doctor_id
        }
    
    # Fallback to legacy Case table
    legacy_case = db.query(Case).filter(Case.id == case_id).first()
    if legacy_case:
         return {
            "id": legacy_case.id,
            "case_code": getattr(legacy_case, "case_code", f"CASE-{legacy_case.id}"),
            "patient_name": legacy_case.patient_name,
            "patient_age": legacy_case.patient_age,
            "patient_gender": "N/A",
            "diagnosis": legacy_case.diagnosis,
            "priority": "Routine",
            "ai_result": legacy_case.ai_result,
            "ai_confidence": legacy_case.ai_confidence,
            "clinical_notes": getattr(legacy_case, "doctor_notes", ""),
            "status": "COMPLETED",
            "image_url": legacy_case.image_url,
            "created_at": legacy_case.created_at
        }
        
    raise HTTPException(status_code=404, detail="Case not found")

# =====================================================
# OTP MEMORY
# =====================================================
verification_codes = {}

# =====================================================
# EMAIL FUNCTION
# =====================================================
def send_otp_email(receiver_email: str, otp: str):
    # load credentials from environment; having defaults helps during development
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("APP_PASSWORD")
    if not sender_email or not sender_password:
        # log the misconfiguration
        print(f"[send_otp_email] missing EMAIL or APP_PASSWORD env vars: {sender_email}, {bool(sender_password)}")
        return False

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        msg = MIMEText(f"Your OTP is {otp}. Valid for 5 minutes.")
        msg["Subject"] = "Password Reset OTP"
        msg["From"] = sender_email
        msg["To"] = receiver_email
        server.send_message(msg)
        server.quit()
        return True
    except Exception as exc:
        # print the error to stdout so it's visible in the server logs
        print(f"[send_otp_email] exception: {exc}")
        return False

# =====================================================
# SCHEMAS
# =====================================================

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    hospital_email: EmailStr
    phone_number: str
    role_requested: str
    password: str
    confirm_password: str

    @validator("first_name", "last_name")
    def name_validation(cls, v):
        if not v.isalpha():
            raise ValueError("Name must contain only letters")
        if len(v) < 2:
            raise ValueError("Name too short")
        return v.strip()

    @validator("hospital_email")   # ✅ INSIDE CLASS (4 spaces)
    def email_validation(cls, v):  # ✅ ALSO 4 spaces
        import re

        v = v.strip().lower()

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|in|org|edu)$"

        if not re.match(pattern, v):
            raise ValueError("Enter valid email (example@gmail.com)")

        return v

    @validator("phone_number")
    def phone_validation(cls, v):
        if not re.fullmatch(r"[6-9]\d{9}", v):
            raise ValueError("Phone must be 10 digits and start with 6-9")
        return v

    @validator("role_requested")
    def role_validation(cls, v):
        if v.lower() != "doctor":
            raise ValueError("Role must be doctor")
        return v.lower()

    @validator("password")
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError("Min 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain uppercase")
        if not re.search(r"[a-z]", v):
            raise ValueError("Must contain lowercase")
        if not re.search(r"\d", v):
            raise ValueError("Must contain number")
        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError("Must contain special char")
        return v

    @validator("confirm_password")
    def confirm_password(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

class DoctorLogin(BaseModel):
    hospital_email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    confirm_password: str

class AddCaseRequest(BaseModel):
    doctor_id: int 
    patient_name: str
    patient_age: int
    diagnosis: str
    priority: PriorityEnum
    image_url: str
    ai_findings: Optional[str] = None
    ai_confidence: Optional[int] = None

class SignRequest(BaseModel):
    doctor_name: str

class EditNotesRequest(BaseModel):
    doctor_notes: str

class ConfirmDiagnosisRequest(BaseModel):
    doctor_name: str
    notes: Optional[str] = None

class OtherConditionRequest(BaseModel):
    doctor_name: str
    other_condition: str
    notes: Optional[str] = None

class NotesRequest(BaseModel):
    notes: str

class FinalizeRequest(BaseModel):
    doctor_name: str
    impression: Optional[str] = None
    recommendation: Optional[str] = None


class EditProfileRequest(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

class NotificationSettingsRequest(BaseModel):
    new_cases: bool
    critical_findings: bool
    report_delivery: bool

class DiagnosisUpdateRequest(BaseModel):
    status: str
    confirmed_findings: list[str]
    clinical_notes: str
    icd_code: str

class PrivacySettingsRequest(BaseModel):
    data_sharing: bool
    history_retention: bool
    diagnostics: bool

class LanguageUpdateRequest(BaseModel):
    preferred_language: str

class SupportRequest(BaseModel):
    message: str

class ChatRequest(BaseModel):
    case_id: int
    disease: str
    confidence: float
    triage: str
    question: str

def generate_ai_response(disease, confidence, triage, question):

    q = question.lower()

    # 1. Explain the diagnosis
    if "explain" in q and "diagnosis" in q:
        return f"The system predicts {disease} based on abnormal lung opacities visible in the chest X-ray."

    # 2. Why is this case critical?
    elif "critical" in q and "why" in q:
        return f"The case is marked as {triage} due to severe abnormalities detected in lung regions requiring immediate attention."

    # 3. What is confidence score?
    elif "confidence" in q and "score" in q:
        return f"Confidence score indicates how certain the AI model is about its prediction. Here, it's {confidence*100:.1f}%."

    # 4. What features were detected?
    elif "feature" in q or "detected" in q:
        return "The model detected lung opacity and abnormal patterns in lung regions."

    # 5. Is this Pneumonia or TB?
    elif "tb" in q or "tuberculosis" in q:
        return f"The model predicts {disease}, but further clinical tests are needed to confirm TB."

    # 6. What is the triage level?
    elif "triage" in q and "level" in q:
        return f"Triage level indicates urgency: {triage}."

    # 7. What are the next steps?
    elif "next" in q and "step" in q:
        return "Clinical evaluation and confirmatory tests are recommended."

    # 8. Is this life-threatening?
    elif "life" in q and "threatening" in q:
        return "It may be serious depending on severity and requires prompt attention."

    # 9. Can this prediction be wrong?
    elif "wrong" in q or "false" in q:
        return "Yes, AI predictions may have errors. Doctor verification is required."

    # 10. What symptoms are associated?
    elif "symptom" in q:
        return "Common symptoms include cough, fever, chest pain, and breathing difficulty."

    # 11. Which lung area is affected?
    elif "lung" in q and "area" in q:
        return "Abnormalities are observed in specific lung regions."

    # 12. How severe is this case?
    elif "severe" in q:
        return "Severity is determined based on abnormal patterns detected."

    # 13. What does normal mean?
    elif "normal" in q:
        return "No significant abnormalities detected."

    # 14. Why urgent and not critical?
    elif "urgent" in q and "not" in q and "critical" in q:
        return "Urgent cases need quick attention but are not immediately life-threatening."

    # 15. Can I trust this AI?
    elif "trust" in q and "ai" in q:
        return "AI assists decision-making, but final decisions must be made by the doctor."

    # 16. What tests are needed?
    elif "test" in q and "needed" in q:
        return "CT scan, blood tests, or sputum analysis may be required."

    # 17. Is hospitalization required?
    elif "hospital" in q and "required" in q:
        return "It depends on severity and clinical evaluation."

    # 18. What is lung opacity?
    elif "lung" in q and "opacity" in q:
        return "Lung opacity indicates infection, fluid, or inflammation."

    # 19. What if confidence is low?
    elif "low" in q and "confidence" in q:
        return "Low confidence suggests uncertainty; further testing is needed."

    # 20. Give case summary
    elif "summary" in q:
        return f"The system predicts a disease with given confidence and triage level, requiring clinical review. Predicted: {disease}, Confidence: {confidence*100:.1f}%, Triage: {triage}."

    # Default
    else:
        return f"The case is predicted as {disease} with {confidence*100:.1f}% confidence and triage level {triage}. Doctor verification is required."


class TechnicianRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role_requested: str
    password: str
    confirm_password: str

    @validator("first_name", "last_name")
    def name_validation(cls, v):
        if not v.isalpha():
            raise ValueError("Name must contain only letters")
        if len(v) < 2:
            raise ValueError("Name too short")
        return v.strip()

    @validator("email")   # ✅ inside class
    def email_validation(cls, v):
        import re

        v = v.strip().lower()

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|in|org|edu)$"

        if not re.match(pattern, v):
            raise ValueError("Enter valid email (example@gmail.com)")

        return v

    @validator("phone_number")
    def phone_validation(cls, v):
        if not re.fullmatch(r"[6-9]\d{9}", v):
            raise ValueError("Phone must be 10 digits and start with 6-9")
        return v

    @validator("role_requested")
    def role_validation(cls, v):
        if v.lower() != "technician":
            raise ValueError("Role must be technician")
        return v.lower()

    @validator("password")
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError("Min 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain uppercase")
        if not re.search(r"[a-z]", v):
            raise ValueError("Must contain lowercase")
        if not re.search(r"\d", v):
            raise ValueError("Must contain number")
        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError("Must contain special char")
        return v

    @validator("confirm_password")
    def confirm_password(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

class TechnicianLogin(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str



class PatientRegisterRequest(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    mrn: str
    reason_for_xray: str

class ScanPreparationRequest(BaseModel):
    position_patient: bool
    proper_distance: bool
    radiation_safety: bool
    remove_metal: bool
    calibration_verified: bool
    exposure_settings: bool

class UpdateTechnicianProfile(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str




# =====================================================
# AUTH APIs
# =====================================================

@app.post("/register")
def register_doctor(data: DoctorCreate, db: Session = Depends(get_db)):

    # ✅ Extra safety (even though validator already checks)
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # ✅ Normalize data
    email = data.hospital_email.lower().strip()
    phone = data.phone_number.strip()

    # ✅ Check duplicate email
    existing_email = db.query(Doctor).filter(
        Doctor.hospital_email == email
    ).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Check duplicate phone
    existing_phone = db.query(Doctor).filter(
        Doctor.phone_number == phone
    ).first()

    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    # ✅ Save user
    new_doctor = Doctor(
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        hospital_email=email,
        phone_number=phone,
        role_requested="doctor",   # 🔥 force role (important)
        password=data.password     # plain password (as you want)
    )

    db.add(new_doctor)
    db.commit()

    return {
        "message": "Doctor registered successfully",
        "role": "doctor"
    }
@app.post("/doctor/login")
def doctor_login(data: DoctorLogin, db: Session = Depends(get_db)):

    # Validate input
    if not data.hospital_email.strip():
        raise HTTPException(status_code=400, detail="Email required")

    if not data.password.strip():
        raise HTTPException(status_code=400, detail="Password required")

    # Check doctor
    doctor = db.query(Doctor).filter(
        Doctor.hospital_email == data.hospital_email
    ).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if doctor.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    # ✅ FINAL CORRECT RESPONSE
    return {
        "message": "Login successful",
        "role": "doctor",
        "doctor": {
            "id": doctor.id,
            "first_name": doctor.first_name,
            "last_name": doctor.last_name,
            "name": f"{doctor.first_name} {doctor.last_name}"
        }
    }

@app.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()

    return [
        {
            "doctor_id": d.id,
            "name": f"{d.first_name} {d.last_name}"
        }
        for d in doctors
    ]

@app.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(Doctor).filter(Doctor.hospital_email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")
    otp = str(random.randint(100000, 999999))
    verification_codes[data.email] = {
        "otp": otp,
        "expiry": datetime.utcnow() + timedelta(minutes=5)
    }
    if not send_otp_email(data.email, otp):
        raise HTTPException(status_code=500, detail="Failed to send OTP")
    return {"message": "OTP sent successfully"}

@app.post("/verify-otp")
def verify_otp(data: VerifyOTPRequest):
    record = verification_codes.get(data.email)
    if not record:
        raise HTTPException(status_code=400, detail="OTP not generated")
    if datetime.utcnow() > record["expiry"]:
        verification_codes.pop(data.email, None)
        raise HTTPException(status_code=400, detail="OTP expired")
    if record["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"message": "OTP verified successfully"}

@app.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):

    # 1️⃣ Check password match
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # 2️⃣ Find doctor
    doctor = db.query(Doctor).filter(
        Doctor.hospital_email == data.email
    ).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # 3️⃣ Update password
    doctor.password = data.new_password

    # 4️⃣ Save changes
    db.commit()
    db.refresh(doctor)

    return {"message": "Password reset successfully"}
# =====================================================
# TRIAGE APIs
# =====================================================
@app.post("/add-case")
def add_case(data: AddCaseRequest, db: Session = Depends(get_db)):

    new_case = TriageCase(
        doctor_id=data.doctor_id,   # ✅ IMPORTANT LINE
        patient_name=data.patient_name,
        patient_age=data.patient_age,
        diagnosis=data.diagnosis,
        priority=data.priority,
        image_url=data.image_url
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return {
        "message": "Case added successfully",
        "doctor_id": data.doctor_id
    }

# =====================================================
# CREATE PATIENT
# =====================================================
class CreatePatientRequest(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    mrn: str
    reason_for_xray: str


@app.get("/case-queue")
def get_case_queue(doctor_id: int, db: Session = Depends(get_db)):

    cases = db.query(TriageCase).filter(
        TriageCase.doctor_id == doctor_id,
        TriageCase.status != StatusEnum.COMPLETED   # ✅ FIX
    ).order_by(TriageCase.created_at.desc()).all()

    print("🔥 Queue count:", len(cases))  # ✅ DEBUG

    result = []

    for case in cases:
        result.append({
            "case_id": case.id,
            "patient_name": case.patient_name,
            "age": case.patient_age,
            "diagnosis": case.diagnosis,
            "priority": str(case.priority),
            "status": str(case.status),
            "date": case.created_at.strftime("%b %d, %Y %I:%M %p")
        })

    return result



# =====================================================
# CRITICAL ALERTS
# =====================================================
@app.get("/critical-alerts")
def critical_alerts(doctor_id: int, db: Session = Depends(get_db)):

    return db.query(TriageCase).filter(
        TriageCase.doctor_id == doctor_id,
        TriageCase.priority.in_([PriorityEnum.CRITICAL, PriorityEnum.URGENT])
    ).all()

    if priority:
        query = query.filter(TriageCase.priority == PriorityEnum(priority))
    else:
        query = query.filter(
            (TriageCase.priority == PriorityEnum.CRITICAL) |
            (TriageCase.priority == PriorityEnum.URGENT)
        )

    return query.all()

@app.get("/triage-dashboard")
def get_dashboard(doctor_id: int, db: Session = Depends(get_db)):

    cases = db.query(TriageCase).filter(
        TriageCase.doctor_id == doctor_id
    ).all()

    print("🔥 Dashboard cases count:", len(cases))

    return cases

def _priority_meta(priority: Optional[PriorityEnum]):
    """Return UI metadata for a priority value.

    This is used by the Case Queue / Critical Alerts screens.

    """

    if priority == PriorityEnum.CRITICAL:
        return {"priority_label": "High", "priority_color": "#E84C4C"}
    if priority == PriorityEnum.URGENT:
        return {"priority_label": "Urgent", "priority_color": "#F5A623"}
    if priority == PriorityEnum.ROUTINE:
        return {"priority_label": "Routine", "priority_color": "#1072E0"}

    return {"priority_label": str(priority) if priority is not None else None, "priority_color": None}


def get_case_obj(case_id: int, db: Session):
    # Prefer the triage queue case record (used by the UI case review flow).
    case = db.query(TriageCase).filter(TriageCase.id == case_id).first()
    if case:
        return case

    # Fallback to the legacy Case table if no triage case exists.
    case = db.query(Case).filter(Case.id == case_id).first()
    if case:
        return case

    raise HTTPException(status_code=404, detail="Case not found")

# Merged into line 435 for consistency


@app.put("/case/{case_id}/accept")
def accept_case(case_id: int, data: SignRequest, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)
    case_obj.decision = DecisionEnum.ACCEPTED
    case_obj.status = StatusEnum.COMPLETED
    case_obj.signed_by = data.doctor_name
    case_obj.reviewed_at = datetime.utcnow()
    db.commit()
    return {"message": "Case accepted successfully"}

@app.put("/case/{case_id}/reject")
def reject_case(case_id: int, data: SignRequest, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)
    case_obj.decision = DecisionEnum.REJECTED
    case_obj.status = StatusEnum.COMPLETED
    case_obj.signed_by = data.doctor_name
    case_obj.reviewed_at = datetime.utcnow()
    db.commit()
    return {"message": "Case rejected successfully"}

@app.put("/case/{case_id}/edit-notes")
def edit_notes(case_id: int, data: EditNotesRequest, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)
    case_obj.doctor_notes = data.doctor_notes
    db.commit()
    return {"message": "Doctor notes updated"}

@app.get("/case-history")
def case_history(doctor_id: int, db: Session = Depends(get_db)):

    cases = db.query(TriageCase).filter(
        TriageCase.doctor_id == doctor_id,
        TriageCase.status == StatusEnum.COMPLETED
    ).order_by(TriageCase.created_at.desc()).all()

    result = []

    for case in cases:
        result.append({
            "case_id": case.id,
            "patient_name": case.patient_name,
            "diagnosis": case.final_diagnosis or case.diagnosis,
            "priority": str(case.priority),
            "status": str(case.status),
            "date": case.created_at.strftime("%b %d, %Y"),
            "reviewed_at": case.reviewed_at.strftime("%b %d, %Y %I:%M %p") if case.reviewed_at else None
        })

    return result



# =====================================================
# MEDICAL HISTORY (Timeline)
# =====================================================
@app.get("/medical-history/{patient_name}")
def medical_history(patient_name: str, doctor_id: int, db: Session = Depends(get_db)):

    cases = db.query(TriageCase).filter(
        TriageCase.doctor_id == doctor_id,
        TriageCase.status == StatusEnum.COMPLETED,
        TriageCase.patient_name == patient_name
    ).order_by(TriageCase.created_at.desc()).all()

    return cases

# =====================================================
# PATIENT DETAIL + SCAN HISTORY
# =====================================================
@app.get("/patient/{patient_id}")
def patient_detail(patient_id: int, db: Session = Depends(get_db)):

    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    scans = db.query(TriageCase).filter(
        TriageCase.patient_id == patient_id
    ).order_by(TriageCase.created_at.desc()).all()

    scan_history = []

    for case in scans:
        scan_history.append({
            "case_id": case.id,
            "scan_type": case.diagnosis,
            "result": case.final_diagnosis,
            "priority": case.priority,
            "status": case.status,
            "date": case.created_at.strftime("%b %d, %Y")
        })

    return {
        "patient": {
            "patient_id": patient.id,        # 👈 THIS IS WHAT YOU WANT
            "mrn": patient.mrn,
            "name": patient.full_name,
            "gender": patient.gender,
            "mrn": patient.mrn,
            "date_of_birth": patient.date_of_birth,
            "gender": patient.gender,
            "reason_for_xray": patient.reason_for_xray
        },
        "scan_history": scan_history
    }

# =====================================================
# FINAL DIAGNOSIS APIs
# =====================================================
@app.get("/case/{case_id}/final-diagnosis")
def final_diagnosis(case_id: int, db: Session = Depends(get_db)):
    return get_case(case_id, db)

@app.put("/case/{case_id}/confirm-ai")
def confirm_ai(case_id: int, data: dict, db: Session = Depends(get_db)):

    case_obj = get_case_obj(case_id, db)

    doctor_name = data.get("doctor_name")
    notes = data.get("notes")

    case_obj.final_diagnosis = case_obj.diagnosis
    case_obj.doctor_notes = notes
    case_obj.signed_by = doctor_name

    case_obj.finalized = True
    case_obj.status = StatusEnum.COMPLETED   # ✅ FIXED

    db.commit()
    db.refresh(case_obj)

    return {
        "message": "AI diagnosis confirmed and case finalized"
    }
# =====================================================
# DOWNLOAD REPORT PDF
# =====================================================
def _build_report_pdf(case_obj):
    # Store generated reports in a dedicated folder so they can be reused.
    os.makedirs("reports", exist_ok=True)

    # Make the filename safe (remove spaces/special characters).
    safe_name = "".join(c for c in case_obj.patient_name if c.isalnum() or c in ("_", "-"))
    file_name = f"Medical_Report_{safe_name}.pdf"
    file_path = os.path.join("reports", file_name)

    doc = SimpleDocTemplate(file_path)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"<b>Medical Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph(f"Report ID: {case_obj.report_id}", styles["Normal"]))
    elements.append(Paragraph(f"Patient Name: {case_obj.patient_name}", styles["Normal"]))
    elements.append(Paragraph(f"Age: {case_obj.patient_age}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>AI Findings:</b>", styles["Heading2"]))
    elements.append(Paragraph(case_obj.ai_findings or "N/A", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Final Diagnosis:</b>", styles["Heading2"]))
    elements.append(Paragraph(case_obj.final_diagnosis or "N/A", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Doctor Notes:</b>", styles["Heading2"]))
    elements.append(Paragraph(case_obj.doctor_notes or "N/A", styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph(f"Signed By: {case_obj.signed_by}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {case_obj.reviewed_at}", styles["Normal"]))

    doc.build(elements)

    return file_path, file_name


@app.get("/case/{case_id}/download-pdf")
def download_pdf(case_id: int, db: Session = Depends(get_db)):

    case_obj = get_case_obj(case_id, db)

    if not case_obj.finalized:
        raise HTTPException(status_code=400, detail="Report not finalized")

    file_path, file_name = _build_report_pdf(case_obj)
    return FileResponse(file_path, media_type='application/pdf', filename=file_name)


@app.get("/case/{case_id}/report-sent")
def report_sent(case_id: int, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)
    if not case_obj.finalized:
        raise HTTPException(status_code=400, detail="Report not finalized")

    file_path, file_name = _build_report_pdf(case_obj)
    file_size = None
    try:
        file_size = os.path.getsize(file_path)
    except OSError:
        pass

    return {
        "file_name": file_name,
        "file_size_bytes": file_size,
        "download_url": f"/case/{case_id}/download-pdf",
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.put("/case/{case_id}/mark-normal")
def mark_normal(case_id: int, data: ConfirmDiagnosisRequest, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)
    case_obj.final_diagnosis = "Normal / No Findings"
    case_obj.status = StatusEnum.COMPLETED
    case_obj.decision = DecisionEnum.ACCEPTED
    case_obj.doctor_notes = data.notes
    case_obj.signed_by = data.doctor_name
    case_obj.reviewed_at = datetime.utcnow()
    db.commit()
    return {"message": "Marked normal"}


@app.post("/case/create")
def create_case(scan_id: int, doctor_id: int, db: Session = Depends(get_db)):
    new_case = Case(
        scan_id=scan_id,
        doctor_id=doctor_id,
        status="pending"
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case

@app.put("/case/{case_id}/other-condition")
def other_condition(case_id: int, data: OtherConditionRequest, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)
    case_obj.final_diagnosis = data.other_condition
    case_obj.status = StatusEnum.COMPLETED
    case_obj.decision = DecisionEnum.ACCEPTED
    case_obj.doctor_notes = data.notes
    case_obj.signed_by = data.doctor_name
    case_obj.reviewed_at = datetime.utcnow()
    db.commit()
    return {"message": "Other condition saved"}

@app.put("/case/{case_id}/update-notes")
def update_notes(case_id: int, data: NotesRequest, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)
    case_obj.doctor_notes = data.notes
    db.commit()
    return {"message": "Notes updated"}


@app.put("/case/{case_id}/finalize-sign")
def finalize_case(case_id: int, data: FinalizeRequest, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)

    case_obj.finalized = True
    case_obj.status = StatusEnum.COMPLETED
    case_obj.decision = DecisionEnum.ACCEPTED
    case_obj.signed_by = data.doctor_name
    case_obj.reviewed_at = datetime.utcnow()
    
    # Save clinical findings for report generation
    if data.impression:
        case_obj.final_diagnosis = data.impression
    if data.recommendation:
        case_obj.doctor_notes = data.recommendation

    db.commit()

    return {"message": "Case finalized successfully"}

@app.get("/case/{case_id}/generate-report")
def generate_report(case_id: int, db: Session = Depends(get_db)):
    return get_case(case_id, db)

# =====================================================
# REPORT PREVIEW + FINALIZE
# =====================================================
@app.get("/case/{case_id}/report-preview")
def report_preview(case_id: int, db: Session = Depends(get_db)):
    case_obj = get_case_obj(case_id, db)
    if not case_obj.report_id:
        case_obj.report_id = f"RPT-{datetime.utcnow().year}-{case_obj.id}"
        db.commit()
    return {
        "app_name": "MediScan",
        "report_number": case_obj.report_id,
        "patient": {
            "name": case_obj.patient_name,
            "age": case_obj.patient_age
        },
        "findings": case_obj.ai_findings,
        "impression": case_obj.final_diagnosis,
        "signature": f"Signed, {case_obj.signed_by}" if case_obj.signed_by else None,
        "finalized": case_obj.finalized
    }



@app.post("/doctor/ai-diagnose")
async def doctor_ai_diagnose(file: UploadFile = File(...)):

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        buffer.write(file.file.read())

    disease, confidence = predict_disease(temp_path)

    os.remove(temp_path)

    return {
        "ai_result": disease,
        "confidence": round(confidence * 100, 2)
    }

@app.get("/doctor/profile/{email}")
def get_profile(email: str, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.hospital_email == email).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Calculate real stats
    cases_reviewed = db.query(Case).filter(Case.doctor_id == doctor.id, Case.status == "Reviewed").count()
    
    from datetime import datetime, date
    today = date.today()
    month_start = datetime(today.year, today.month, 1)
    cases_this_month = db.query(Case).filter(Case.doctor_id == doctor.id, Case.status == "Reviewed", Case.created_at >= month_start).count()

    return {
        "id": doctor.id,
        "full_name": f"{doctor.first_name} {doctor.last_name}",
        "email": doctor.hospital_email,
        "phone": doctor.phone_number,
        "role": doctor.role_requested,
        "specialization": doctor.specialization,
        "photo_url": doctor.profile_photo,
        "joined_at": doctor.created_at.isoformat() if hasattr(doctor, 'created_at') and doctor.created_at else None,
        "stats": {
            "cases_reviewed": cases_reviewed,
            "cases_this_month": cases_this_month,
            "accuracy": "94.3%",
            "review_time": "12m"
        }
    }

@app.get("/doctor/stats/{doctor_id}")
def get_doctor_stats(doctor_id: int, db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Get last 6 months
    stats = []
    today = datetime.utcnow()
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=i*30)
        start_date = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month_date.month == 12:
            end_date = month_date.replace(year=month_date.year+1, month=1, day=1)
        else:
            end_date = month_date.replace(month=month_date.month+1, day=1)
            
        month_label = start_date.strftime("%b")
        count_reviewed = db.query(Case).filter(Case.doctor_id == doctor_id, Case.status == "Reviewed", Case.created_at >= start_date, Case.created_at < end_date).count()
        count_reports = count_reviewed # For now, same
        
        stats.append({
            "month": month_label,
            "reviewed": count_reviewed,
            "reports": count_reports
        })
        
    return stats


class UpdateProfile(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    email: str
    specialization: Optional[str] = None


@app.put("/doctor/update-profile")
def update_profile(data: UpdateProfile, db: Session = Depends(get_db)):
    try:
        # Prefer finding by ID for reliability
        doctor = db.query(Doctor).filter(Doctor.id == data.id).first()
        
        # Fallback to email search for legacy/initial setup cases
        if not doctor:
            doctor = db.query(Doctor).filter(Doctor.hospital_email == data.email).first()
            
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor account not found")
            
        # Update every field
        doctor.first_name = data.first_name
        doctor.last_name = data.last_name
        doctor.hospital_email = data.email
        doctor.phone_number = data.phone_number
        doctor.specialization = data.specialization
        
        db.commit()
        db.refresh(doctor)
        return {"message": "Profile updated successfully", "doctor_id": doctor.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/doctor/upload-photo/{email}")
def upload_photo(email: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.hospital_email == email).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    import re
    # Slugify: lowercase, replace spaces/special chars with underscores
    clean_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', file.filename.lower()).replace(' ', '_')
    file_path = f"profile_photos/{clean_filename}"
    os.makedirs("profile_photos", exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doctor.profile_photo = file_path
    db.commit()

    return {"message": "Photo uploaded successfully", "photo": file_path}




@app.delete("/doctor/remove-photo/{email}")
def remove_photo(email: str, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.hospital_email == email).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.profile_photo = None
    db.commit()

    return {"message": "Photo removed"}




@app.get("/language/{doctor_id}")
def get_language(doctor_id: int, db: Session = Depends(get_db)):

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        "preferred_language": doctor.preferred_language
    }


@app.put("/language/{doctor_id}")
def update_language(
    doctor_id: int,
    data: LanguageUpdateRequest,
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.preferred_language = data.preferred_language
    db.commit()

    return {"message": "Language updated successfully"}

@app.get("/faqs")
def get_faqs(db: Session = Depends(get_db)):
    faqs = db.query(FAQ).all()
    return faqs

class HelpRequest(BaseModel):
    email: str
    message: str


@app.post("/help-support")
def help_support(data: HelpRequest, db: Session = Depends(get_db)):
    # Note: assuming notifications table exists or should be handled via SupportTicket model
    # For now, let's just use the SupportTicket model if available or stick to the logic
    # but the previous one used a cursor on a non-existent 'notifications' table?
    # Actually support_tickets table exists (line 328)
    
    new_ticket = SupportTicket(
        doctor_id=0, # Placeholder since we don't have ID, maybe should use email
        message=data.message,
        status="OPEN"
    )
    db.add(new_ticket)
    db.commit()

    return {"message": "Support request sent"}


@app.post("/logout/{doctor_id}")
def logout(doctor_id: int, db: Session = Depends(get_db)):

    sessions = db.query(DoctorSession).filter(
        DoctorSession.doctor_id == doctor_id,
        DoctorSession.is_active == True
    ).all()

    for session in sessions:
        session.is_active = False

    db.commit()

    return {"message": "Logged out successfully"}

@app.post("/ai-chat")
async def ai_chat(req: ChatRequest):

    reply = generate_ai_response(
        req.disease,
        req.confidence,
        req.triage,
        req.question
    )

    return {
        "reply": reply
    }




@app.post("/technician/register")
def register_technician(data: TechnicianRegister, db: Session = Depends(get_db)):

    # ✅ Password match check
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # ✅ Normalize
    email = data.email.lower().strip()
    phone = data.phone_number.strip()

    # ✅ Check duplicate email
    existing_email = db.query(Technician).filter(
        Technician.email == email
    ).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ (Optional but recommended) check phone duplicate
    existing_phone = db.query(Technician).filter(
        Technician.phone_number == phone
    ).first()

    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone already registered")

    # ✅ Save technician
    technician = Technician(
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        email=email,
        phone_number=phone,
        role_requested="technician",   # 🔥 force role
        password=data.password
    )

    db.add(technician)
    db.commit()

    return {
        "message": "Technician account created successfully",
        "role": "technician"
    }


@app.post("/technician/login")
def technician_login(data: TechnicianLogin, db: Session = Depends(get_db)):

    # Validate input
    if not data.email.strip():
        raise HTTPException(status_code=400, detail="Email required")

    if not data.password.strip():
        raise HTTPException(status_code=400, detail="Password required")

    # Check user
    technician = db.query(Technician).filter(
        Technician.email == data.email
    ).first()

    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    if technician.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    # ✅ FIXED RESPONSE (IMPORTANT)
    return {
        "message": "Login successful",
        "role": "technician",
        "technician": {
            "id": technician.id,
            "name": f"{technician.first_name} {technician.last_name}"
        }
    }
    
from datetime import timedelta

@app.post("/technician/forgot-password")
def send_verification_code(data: ForgotPasswordRequest, db: Session = Depends(get_db)):

    technician = db.query(Technician).filter(
        Technician.email == data.email
    ).first()

    if not technician:
        raise HTTPException(status_code=404, detail="Email not registered")

    otp = str(random.randint(100000, 999999))

    expiry_time = datetime.utcnow() + timedelta(minutes=5)

    otp_entry = TechnicianPasswordResetOTP(
        email=data.email,
        otp_code=otp,
        expires_at=expiry_time
    )

    db.add(otp_entry)
    db.commit()
    
    send_otp_email(data.email, otp)
    return {
        "message": "Verification code sent to your email"
}


class VerifyOTPRequest(BaseModel):
    email: str
    otp: str


@app.post("/technician/verify-otp")
def verify_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):

    otp_entry = db.query(TechnicianPasswordResetOTP).filter(
        TechnicianPasswordResetOTP.email == data.email,
        TechnicianPasswordResetOTP.otp_code == data.otp,
        TechnicianPasswordResetOTP.is_used == False
    ).first()

    if not otp_entry:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    otp_entry.is_used = True
    db.commit()

    return {"message": "OTP verified successfully"}


class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str
    confirm_password: str


@app.post("/technician/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):

    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    technician = db.query(Technician).filter(
        Technician.email == data.email
    ).first()

    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    technician.password = data.new_password   # plain text (as per your setup)
    db.commit()

    return {"message": "Password reset successfully"}


@app.get("/technician/dashboard/{technician_id}")
def get_dashboard(technician_id: int, db: Session = Depends(get_db)):

    today = datetime.utcnow().date()

    # Today scans
    today_count = db.query(Scan).filter(
        Scan.technician_id == technician_id,
        Scan.created_at >= today
    ).count()

    # Pending scans
    pending_count = db.query(Scan).filter(
        Scan.technician_id == technician_id,
        Scan.status == "Pending"
    ).count()

    # Total scans
    total_count = db.query(Scan).filter(
        Scan.technician_id == technician_id
    ).count()

    # Recent scans (last 5)
    recent_scans = db.query(Scan).filter(
        Scan.technician_id == technician_id
    ).order_by(Scan.created_at.desc()).limit(5).all()

    result = []

    for scan in recent_scans:
        patient = db.query(Patient).filter(Patient.id == scan.patient_id).first()

        result.append({
            "patient_name": patient.full_name if patient else "",
            "mrn": patient.mrn if patient else "",
            "status": scan.status,
            "time": scan.created_at
        })

    return {
        "today": today_count,
        "pending": pending_count,
        "total": total_count,
        "recent_scans": result
    }


@app.get("/technician/dashboard-stats/{technician_id}")
def get_dashboard_stats(technician_id: int, db: Session = Depends(get_db)):
    today = datetime.utcnow().date()

    # Today scans
    today_count = db.query(Scan).filter(
        Scan.technician_id == technician_id,
        Scan.created_at >= today
    ).count()

    # Completed scans
    completed_count = db.query(Scan).filter(
        Scan.technician_id == technician_id,
        Scan.status == "Completed"
    ).count()

    # Pending scans
    pending_count = db.query(Scan).filter(
        Scan.technician_id == technician_id,
        Scan.status == "Pending"
    ).count()

    # Total scans
    total_count = db.query(Scan).filter(
        Scan.technician_id == technician_id
    ).count()

    return {
        "today": today_count,
        "completed": completed_count,
        "pending": pending_count,
        "total": total_count
    }


@app.post("/technician/register-patient")
def create_patient(data: PatientRegisterRequest, db: Session = Depends(get_db)):

    new_patient = Patient(
        full_name=data.full_name,
        date_of_birth=data.date_of_birth,
        gender=data.gender,
        mrn=data.mrn,
        reason_for_xray=data.reason_for_xray
    )

    db.add(new_patient)        # ✅ Add to DB
    db.commit()                # ✅ SAVE (VERY IMPORTANT)
    db.refresh(new_patient)    # ✅ Get ID

    return {
        "patient_id": new_patient.id,
        "mrn": new_patient.mrn,
        "message": "Patient registered successfully"
    }


@app.get("/patient/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):

    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "patient_id": f"PAT-{patient.id}",
        "full_name": patient.full_name,
        "date_of_birth": patient.date_of_birth,
        "gender": patient.gender,
        "mrn": patient.mrn
    }


import random

import random

@app.post("/start-scan/{patient_id}")
def start_scan(patient_id: int, technician_id: int, db: Session = Depends(get_db)):

    scan_count = db.query(Scan).count() + 1
    scan_code = f"SCN-{1000 + scan_count}"

    scan = Scan(
        patient_id=patient_id,
        technician_id=technician_id,   # ✅ ADD THIS LINE
        scan_code=scan_code,
        scan_status="Started",
        status="started"
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return {
        "message": "Scan started",
        "scan_id": scan.id,
        "scan_code": scan.scan_code
    }

@app.post("/scan-preparation/{scan_id}")
def save_scan_preparation(scan_id: int,
                          data: ScanPreparationRequest,
                          db: Session = Depends(get_db)):

    # Check scan exists
    scan = db.query(Scan).filter(Scan.id == scan_id).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    preparation = ScanPreparation(
        scan_id=scan_id,
        position_patient=data.position_patient,
        proper_distance=data.proper_distance,
        radiation_safety=data.radiation_safety,
        remove_metal=data.remove_metal,
        calibration_verified=data.calibration_verified,
        exposure_settings=data.exposure_settings
    )

    db.add(preparation)
    db.commit()
    db.refresh(preparation)

    return {
        "message": "Scanner preparation saved successfully",
        "scan_id": scan_id
    }


def assign_priority(disease, confidence, tech_urgency="Routine"):
    # AI assigned priority based strictly on image severity
    if confidence >= 0.85:
        ai_prio = PriorityEnum.CRITICAL
    elif confidence >= 0.65:
        ai_prio = PriorityEnum.URGENT
    else:
        ai_prio = PriorityEnum.ROUTINE
        
    # Standardize values: 3 (Critical), 2 (Urgent), 1 (Routine)
    val_map = {
        "CRITICAL": 3, "STAT (Emergency)": 3, "STAT": 3,
        "URGENT": 2, "Urgent": 2,
        "ROUTINE": 1, "Routine": 1
    }
    
    ai_val = val_map.get(ai_prio.value if hasattr(ai_prio, "value") else str(ai_prio), 1)
    tech_val = val_map.get(tech_urgency, 1)
    
    # Priority defaults to the highest level indicated by either AI or the Technician
    max_val = max(ai_val, tech_val)
    if max_val == 3:
        return PriorityEnum.CRITICAL
    elif max_val == 2:
        return PriorityEnum.URGENT
    return PriorityEnum.ROUTINE

@app.post("/upload-scan/{scan_id}")
def upload_scan(
    scan_id: int,
    doctor_id: int,
    technician_urgency: str = "Routine",
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 🔥 FIX 1: Validate doctor_id
    if doctor_id is None or doctor_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid doctor_id")

    print("🔥 doctor_id received:", doctor_id)

    # 🔥 FIX 2: Check doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Get scan
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    # Get patient
    patient = db.query(Patient).filter(Patient.id == scan.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Save image
    upload_dir = "uploaded_scans"
    os.makedirs(upload_dir, exist_ok=True)

    file_location = f"{upload_dir}/scan_{scan_id}.jpg"

    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    scan.image_path = file_location
    scan.uploaded_at = datetime.utcnow()

    # AI
    disease, confidence = predict_disease(file_location)
    priority = assign_priority(disease, confidence, technician_urgency)

    # Calculate age
    from datetime import date
    today = date.today()

    age = today.year - patient.date_of_birth.year - (
        (today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day)
    )

    # Save case
    new_case = TriageCase(
        patient_id=scan.patient_id,
        patient_name=patient.full_name,
        patient_age=age,
        diagnosis=disease,
        priority=priority,
        image_url=file_location,
        ai_findings=f"Detected {disease}",
        ai_confidence=int(confidence * 100),
        ai_result=disease,
        doctor_id=doctor_id,   # ✅ NOW SAFE
        status=StatusEnum.PENDING,
        decision=DecisionEnum.PENDING
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    new_case.case_code = f"SC-{5500 + new_case.id}"
    db.commit()

    return {
        "message": "Scan uploaded and AI analyzed",
        "case_id": new_case.id,
        "doctor_id": doctor_id,
        "doctor_name": f"{doctor.first_name} {doctor.last_name}",
        "disease": disease,
        "confidence": int(confidence * 100)
    }
    
@app.post("/retake-scan/{scan_id}")
def retake_scan(scan_id: int, db: Session = Depends(get_db)):

    scan = db.query(Scan).filter(Scan.id == scan_id).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    scan.review_status = "Rejected"
    scan.scan_status = "Retake Required"
    scan.quality_validated_at = datetime.utcnow()

    db.commit()

    return {"message": "Scan marked for retake"}


@app.post("/accept-scan/{scan_id}")
def accept_scan(scan_id: int, db: Session = Depends(get_db)):

    scan = db.query(Scan).filter(Scan.id == scan_id).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    scan.review_status = "Accepted"
    scan.scan_status = "Completed"
    scan.quality_validated_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Scan accepted and sent to doctor",
        "scan_id": scan_id
    }





@app.get("/scan-details/{value}")
def scan_details(value: str, db: Session = Depends(get_db)):

    scan = None

    # If number → search by ID
    if value.isdigit():
        scan = db.query(Scan).filter(Scan.id == int(value)).first()

    # Otherwise search by scan_code
    if not scan:
        scan = db.query(Scan).filter(Scan.scan_code == value).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    return get_scan_details(scan.scan_code, db)

    

@app.post("/create-study/{scan_id}")
def create_study(scan_id: int, doctor_id: int, db: Session = Depends(get_db)):

    scan = db.query(Scan).filter(Scan.id == scan_id).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    session_id = f"{uuid.uuid4().hex[:6].upper()}-XP-SAFE"

    study = Study(
        scan_id=scan_id,
        session_id=session_id,
        dicom_path=f"dicom_packages/scan_{scan_id}.dcm",
        file_size_mb=14.2,
        upload_progress=0,
        study_status="Processing",
        assigned_doctor=f"Dr. {doctor.first_name} {doctor.last_name}",
        encrypted=True
    )

    db.add(study)
    db.commit()
    db.refresh(study)

    return {
        "study_id": study.id,   # ✅ ADD THIS LINE
        "session_id": study.session_id,
        "progress": study.upload_progress,
        "status": study.study_status
    }

@app.post("/update-study-progress/{study_id}")
def update_progress(study_id: int,
                    progress: int,
                    db: Session = Depends(get_db)):

    study = db.query(Study).filter(Study.id == study_id).first()

    if not study:
        raise HTTPException(status_code=404, detail="Study not found")

    study.upload_progress = progress

    if progress >= 100:
        study.study_status = "Uploaded"

    db.commit()

    return {
        "progress": study.upload_progress,
        "status": study.study_status
    }

@app.post("/finalize-study/{study_id}")
def finalize_study(study_id: int, db: Session = Depends(get_db)):

    study = db.query(Study).filter(Study.id == study_id).first()

    if not study:
        raise HTTPException(status_code=404, detail="Study not found")

    study.study_status = "Sent to Doctor"
    db.commit()

    return {
        "message": "Study securely forwarded to doctor",
        "session_id": study.session_id
    }


@app.post("/distribute-study/{study_id}")
def distribute_study(study_id: int, db: Session = Depends(get_db)):

    study = db.query(Study).filter(Study.id == study_id).first()

    if not study:
        raise HTTPException(status_code=404, detail="Study not found")

    # 1️⃣ PACS Archive
    pacs = PACSArchive(
        study_id=study_id,
        archive_location=f"PACS_SERVER/study_{study_id}.dcm"
    )
    db.add(pacs)

    # 2️⃣ RIS Worklist
    ris = RISWorklist(
        study_id=study_id,
        patient_id=study.scan_id,
        assigned_doctor=study.assigned_doctor
    )
    db.add(ris)

    # 3️⃣ AI Analysis (Simulated)
    ai = AIAnalysis(
        study_id=study_id,
        ai_status="Completed",
        confidence_score=0.94,
        ai_result="No critical abnormalities detected"
    )
    db.add(ai)

    study.study_status = "Distributed"

    db.commit()

    return {
        "message": "Study archived, added to RIS, and AI processed successfully",
        "study_id": study_id
    }


@app.get("/study/{session_id}")
def get_study_status(session_id: str, db: Session = Depends(get_db)):
    """Return processing progress/states for the given study session."""

    study = db.query(Study).filter(Study.session_id == session_id).first()
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")

    pacs = db.query(PACSArchive).filter(PACSArchive.study_id == study.id).order_by(PACSArchive.archived_at.desc()).first()
    ris = db.query(RISWorklist).filter(RISWorklist.study_id == study.id).order_by(RISWorklist.created_at.desc()).first()
    ai = db.query(AIAnalysis).filter(AIAnalysis.study_id == study.id).order_by(AIAnalysis.processed_at.desc()).first()

    return {
        "session_id": study.session_id,
        "study_status": study.study_status,
        "upload_progress": study.upload_progress,
        "pacs": {
            "completed": bool(pacs),
            "archived_at": pacs.archived_at if pacs else None,
            "archive_location": pacs.archive_location if pacs else None,
        },
        "ris": {
            "completed": bool(ris),
            "created_at": ris.created_at if ris else None,
            "assigned_doctor": ris.assigned_doctor if ris else None,
        },
        "ai": {
            "completed": bool(ai),
            "processed_at": ai.processed_at if ai else None,
            "confidence_score": ai.confidence_score if ai else None,
            "ai_result": ai.ai_result if ai else None,
        },
    }


@app.get("/scan-history")
def get_scan_history(technician_id: int, db: Session = Depends(get_db)):

    results = db.query(Scan, Patient, Technician).join(
        Patient, Scan.patient_id == Patient.id
    ).outerjoin(
        Technician, Scan.technician_id == Technician.id
    ).filter(
        Scan.technician_id == technician_id
    ).order_by(Scan.created_at.desc()).all()

    response = []

    for scan, patient, technician in results:
        tc = db.query(TriageCase).filter(TriageCase.patient_id == scan.patient_id).order_by(TriageCase.created_at.desc()).first()
        tech_name = f"{technician.first_name} {technician.last_name}" if technician else "N/A"
        date_iso = scan.created_at.isoformat() if scan.created_at else None
        
        response.append({
            "scan_id": scan.scan_code,
            "patient_name": patient.full_name,
            "mrn": patient.mrn,
            "status": scan.scan_status if scan.scan_status else (scan.status if scan.status else "started"),
            "date": date_iso,
            "created_at": date_iso,
            "ai_finding": tc.ai_result if tc else "N/A",
            "technician_name": tech_name
        })

    return response


@app.get("/scan/{scan_code}")
def get_scan_details(scan_code: str, db: Session = Depends(get_db)):
    """Return all information needed to render the scan details screen."""

    scan = db.query(Scan).filter(Scan.scan_code == scan_code).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    patient = db.query(Patient).filter(Patient.id == scan.patient_id).first()

    study = db.query(Study).filter(Study.scan_id == scan.id).order_by(Study.created_at.desc()).first()
    ai = None
    review = None
    if study:
        ai = db.query(AIAnalysis).filter(AIAnalysis.study_id == study.id).order_by(AIAnalysis.processed_at.desc()).first()
        review = db.query(RadiologistReview).filter(RadiologistReview.study_id == study.id).order_by(RadiologistReview.reviewed_at.desc()).first()

    timeline = []

    timeline.append({
        "step": "X-Ray Captured",
        "status": "completed",
        "timestamp": scan.created_at,
    })

    quality_status = "pending"
    quality_timestamp = scan.quality_validated_at
    if scan.review_status and scan.review_status.lower() in ["accepted", "rejected"]:
        quality_status = "completed"
    elif scan.scan_status == "Retake Required":
        quality_status = "needs_action"

    timeline.append({
        "step": "Quality Validated",
        "status": quality_status,
        "timestamp": quality_timestamp,
        "note": scan.review_status or "Pending validation",
    })

    upload_status = "pending"
    upload_timestamp = scan.uploaded_at
    if scan.image_path:
        upload_status = "completed"

    timeline.append({
        "step": "Uploaded to Server",
        "status": upload_status,
        "timestamp": upload_timestamp,
        "note": scan.image_path or "Not uploaded yet",
    })

    ai_status = "pending"
    ai_note = "Awaiting AI analysis"
    ai_timestamp = None
    if ai:
        ai_status = ai.ai_status or "pending"
        ai_note = ai.ai_result or "Analyzing..."
        ai_timestamp = ai.processed_at

    timeline.append({
        "step": "AI Analysis",
        "status": ai_status,
        "timestamp": ai_timestamp,
        "note": ai_note,
    })

    review_status = "pending"
    review_note = "Pending doctor review"
    review_timestamp = None
    if review:
        review_status = review.review_status or "pending"
        review_note = review.review_notes or "No notes"
        review_timestamp = review.reviewed_at

    timeline.append({
        "step": "Doctor Review",
        "status": review_status,
        "timestamp": review_timestamp,
        "note": review_note,
    })

    # Quality assurance data (used by the mobile app UI)
    quality_check = {
        "passed": False,
        "message": "Awaiting AI quality check",
        "image_quality": None,
        "next_steps": []
    }

    if ai:
        # Basic heuristic: high confidence means pass and optimal image
        passed = ai.confidence_score is not None and ai.confidence_score >= 0.85
        quality_check["passed"] = passed
        quality_check["image_quality"] = "Optimal" if passed else "Needs Attention"
        quality_check["message"] = "AI Quality Check: Passed" if passed else "AI Quality Check: Failed"
        quality_check["next_steps"] = [
            "Scan forwarded to Radiologist Queue",
            "DICOM metadata successfully indexed"
        ]

    tc = db.query(TriageCase).filter(TriageCase.patient_id == scan.patient_id).order_by(TriageCase.created_at.desc()).first()
    tech = db.query(Technician).filter(Technician.id == scan.technician_id).first()
    tech_name = f"{tech.first_name} {tech.last_name}" if tech else "Unknown Technician"

    return {
        "scan_id": scan.scan_code,
        "scan_status": scan.scan_status,
        "created_at": scan.created_at,
        "technician_name": tech_name,
        "ai_finding": f"{tc.ai_result} ({int(tc.ai_confidence or 0)}%)" if tc else "N/A",
        "patient": {
            "full_name": patient.full_name if patient else None,
            "mrn": patient.mrn if patient else None,
            "date_of_birth": patient.date_of_birth if patient else None,
            "gender": patient.gender if patient else None,
        },
        "timeline": timeline,
        "quality_check": quality_check,
    }



# ==============================
# AI PREDICTION (TECHNICIAN SIDE)
# ==============================

def predict_disease(image_path: str):
    img = image.load_img(image_path, target_size=(224,224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    normal_prob = prediction[0][0]
    pneumonia_prob = prediction[0][1]

    if normal_prob > pneumonia_prob:
        disease = "Normal"
        confidence = float(normal_prob)
    else:
        disease = "Pneumonia"
        confidence = float(pneumonia_prob)

    return disease, confidence



@app.get("/technician/profile/{technician_id}")
def get_technician_profile(technician_id: int, db: Session = Depends(get_db)):

    technician = db.query(Technician).filter(
        Technician.id == technician_id
    ).first()

    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    return {
        "id": technician.id,
        "full_name": technician.first_name + " " + technician.last_name,
        "email": technician.email,
        "phone_number": technician.phone_number,
        "role": technician.role_requested
    }


@app.put("/technician/profile/{technician_id}")
def update_technician_profile(
    technician_id: int,
    data: UpdateTechnicianProfile,
    db: Session = Depends(get_db)
):

    technician = db.query(Technician).filter(
        Technician.id == technician_id
    ).first()

    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    technician.first_name = data.first_name
    technician.last_name = data.last_name
    technician.phone_number = data.phone_number

    db.commit()

    return {"message": "Profile updated successfully"}


@app.put("/technician/update-profile")
def update_technician_profile(data: UpdateTechnicianProfile, db: Session = Depends(get_db)):

    technician = db.query(Technician).filter(Technician.email == data.email).first()

    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    technician.first_name = data.first_name
    technician.last_name = data.last_name
    technician.phone_number = data.phone_number

    db.commit()

    return {"message": "Technician profile updated successfully"}


@app.post("/technician/upload-photo/{email}")
def upload_technician_photo(email: str, file: UploadFile = File(...), db: Session = Depends(get_db)):

    technician = db.query(Technician).filter(Technician.email == email).first()

    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    os.makedirs("profile_photos", exist_ok=True)

    file_path = f"profile_photos/{email}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    technician.profile_photo = file_path
    db.commit()

    return {
        "message": "Photo uploaded successfully",
        "photo": file_path
    }


@app.get("/technician/profile/{email}")
def get_technician_profile(email: str, db: Session = Depends(get_db)):

    technician = db.query(Technician).filter(Technician.email == email).first()

    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    return {
        "id": technician.id,
        "first_name": technician.first_name,
        "last_name": technician.last_name,
        "email": technician.email,
        "phone": technician.phone_number,
        "role": technician.role_requested,
        "profile_photo": technician.profile_photo
    }


@app.post("/technician/send-feedback")
async def send_feedback(
    technician_id: int,
    feedback_type: str,
    subject: str,
    description: str,
    screenshot: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    screenshot_path = None

    # Save screenshot if uploaded
    if screenshot:
        file_path = f"{FEEDBACK_UPLOAD_DIR}/{technician_id}_{screenshot.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(screenshot.file, buffer)

        screenshot_path = file_path

    feedback = Feedback(
        technician_id=technician_id,
        feedback_type=feedback_type,
        subject=subject,
        description=description,
        screenshot_path=screenshot_path
    )

    db.add(feedback)
    db.commit()

    return {
        "message": "Feedback submitted successfully"
    }


@app.post("/technician/logout/{technician_id}")
def technician_logout(technician_id: int):

    return {
        "message": "Technician logged out successfully"
    }




@app.get("/doctor/dashboard-summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    new_cases = db.query(TriageCase).filter(TriageCase.status == StatusEnum.PENDING).count()
    critical = db.query(TriageCase).filter(
        (TriageCase.priority == PriorityEnum.CRITICAL) | 
        (TriageCase.priority == PriorityEnum.URGENT)
    ).count()
    in_review = db.query(TriageCase).filter(
        TriageCase.status == StatusEnum.PENDING,
        TriageCase.decision == DecisionEnum.PENDING
    ).count()
    completed = db.query(TriageCase).filter(TriageCase.status == StatusEnum.COMPLETED).count()
    
    return {
        "new": new_cases,
        "critical": critical,
        "in_review": in_review,
        "completed": completed
    }

from sqlalchemy import desc

def time_ago(dt):
    if not dt: return "Just now"
    diff = datetime.utcnow() - dt
    seconds = diff.total_seconds()
    if seconds < 60: return "Just now"
    if seconds < 3600: return f"{int(seconds // 60)} min ago"
    if seconds < 86400: return f"{int(seconds // 3600)} hr ago"
    return f"{int(seconds // 86400)} days ago"

@app.get("/notifications/{user_id}")
def get_notifications(user_id: int, role: str = "doctor", db: Session = Depends(get_db)):
    if role == "doctor":
        cases = db.query(TriageCase).filter(TriageCase.doctor_id == user_id).order_by(desc(TriageCase.created_at)).limit(8).all()
        notifs = []
        for c in cases:
            pval = c.priority.value if hasattr(c.priority, 'value') else str(c.priority)
            if pval == "CRITICAL" or pval == "STAT" or pval == "STAT (Emergency)":
                ntype = "critical"
                title = "Critical Finding"
            elif pval == "URGENT" or pval == "Urgent":
                ntype = "critical"
                title = "Urgent Scan Alert"
            else:
                ntype = "info"
                title = "AI Analysis Complete"
            
            notifs.append({
                "id": c.id,
                "case_id": c.id,
                "type": ntype,
                "title": title,
                "message": f"{c.patient_name} — {c.ai_result or 'Results Ready'}",
                "time": time_ago(c.created_at),
                "read": False
            })
        return notifs
    return []

@app.put("/case/{case_id}/diagnosis")
def update_case_diagnosis_endpoint(case_id: int, data: DiagnosisUpdateRequest, db: Session = Depends(get_db)):
    case_obj = db.query(TriageCase).filter(TriageCase.id == case_id).first()
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case not found")
        
    # Standardize findings as primary diagnosis
    case_obj.final_diagnosis = ", ".join(data.confirmed_findings)
    
    # Prepend ICD code to clinical notes if it exists
    full_notes = f"ICD-10: {data.icd_code}\n\n{data.clinical_notes}" if data.icd_code else data.clinical_notes
    case_obj.doctor_notes = full_notes
    
    # Status and Decision updates
    if data.status == "COMPLETED":
        case_obj.status = StatusEnum.COMPLETED
        case_obj.decision = DecisionEnum.ACCEPTED
        case_obj.reviewed_at = datetime.utcnow()
        
    db.commit()
    return {"message": "Diagnosis updated successfully"}

# =====================================================
# RUN SERVER
# =====================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List
from datetime import datetime

# ---------- Auth ----------

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# ---------- Visa ----------

VisaPurpose = Literal["tourist", "student", "work", "business", "medical", "transit"]

class VisaQuery(BaseModel):
    from_country: str = "IN"
    to_country: str          # ISO-2, e.g. "US"
    purpose: VisaPurpose = "tourist"
    occupation: Optional[str] = None
    duration_days: Optional[int] = None

class DocumentItem(BaseModel):
    name: str
    mandatory: bool
    notes: Optional[str] = None

class VisaResponse(BaseModel):
    corridor: str
    purpose: str
    visa_type: str
    processing_days: str
    fee_usd: Optional[float]
    documents: List[DocumentItem]
    ai_tips: Optional[List[str]] = None

# ---------- Chat ----------

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    message: str
    corridor: Optional[str] = None
    history: List[ChatMessage] = []

# ---------- Tracker ----------

TrackerStatus = Literal["not_started", "in_progress", "submitted", "approved", "rejected"]

class TrackerCreate(BaseModel):
    from_country: str = "IN"
    to_country: str
    purpose: VisaPurpose
    notes: Optional[str] = None

class TrackerUpdate(BaseModel):
    status: Optional[TrackerStatus] = None
    notes: Optional[str] = None
    appointment_date: Optional[datetime] = None

class TrackerItem(BaseModel):
    id: str
    from_country: str
    to_country: str
    purpose: str
    status: TrackerStatus
    notes: Optional[str]
    appointment_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

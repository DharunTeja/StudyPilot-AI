from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MaterialCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None
    subject: Optional[str] = None


class MaterialResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    subject: Optional[str] = None
    file_type: Optional[str] = None
    created_at: datetime
    summary: Optional[str] = None
    key_concepts: Optional[List[str]] = None


class MaterialInDB(BaseModel):
    user_id: str
    title: str
    content: str
    subject: Optional[str] = None
    file_type: Optional[str] = None
    original_filename: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    summary: Optional[str] = None
    key_concepts: Optional[List[str]] = None
    flashcards: Optional[List[dict]] = None
    quizzes: Optional[List[dict]] = None
    study_plan: Optional[dict] = None

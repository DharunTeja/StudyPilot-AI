from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuizAttempt(BaseModel):
    material_id: str
    score: float
    total_questions: int
    correct_answers: int
    time_spent: int  # seconds
    answers: List[dict]


class ProgressEntry(BaseModel):
    user_id: str
    material_id: str
    activity_type: str  # 'quiz', 'flashcard_review', 'study_session'
    score: Optional[float] = None
    time_spent: int = 0  # seconds
    created_at: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[dict] = None


class ProgressStats(BaseModel):
    total_materials: int = 0
    total_quizzes: int = 0
    average_score: float = 0.0
    total_study_time: int = 0  # minutes
    study_streak: int = 0
    weak_topics: List[str] = []
    strong_topics: List[str] = []
    recent_activities: List[dict] = []

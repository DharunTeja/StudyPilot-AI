from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from app.utils.helpers import get_current_user
from app.models.progress import QuizAttempt
from app.services.analytics import analytics_service

router = APIRouter(prefix="/api/progress", tags=["Progress"])

db = None

def set_db(database):
    global db
    db = database

@router.post("/quiz-attempt")
async def save_quiz_attempt(attempt: QuizAttempt, user_id: str = Depends(get_current_user)):
    progress_doc = {
        "user_id": user_id,
        "material_id": attempt.material_id,
        "activity_type": "quiz",
        "score": attempt.score,
        "total_questions": attempt.total_questions,
        "correct_answers": attempt.correct_answers,
        "time_spent": attempt.time_spent,
        "answers": attempt.answers,
        "created_at": datetime.utcnow()
    }

    await db.progress.insert_one(progress_doc)

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        quizzes_taken = user.get("quizzes_taken", 0) + 1
        current_avg = user.get("average_score", 0.0)
        new_avg = ((current_avg * (quizzes_taken - 1)) + (attempt.score * 100)) / quizzes_taken

        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "quizzes_taken": quizzes_taken,
                    "average_score": round(new_avg, 1)
                }
            }
        )

    return {"message": "Quiz attempt saved successfully"}

@router.post("/study-session")
async def save_study_session(
    material_id: str,
    time_spent: int,
    user_id: str = Depends(get_current_user)
):
    progress_doc = {
        "user_id": user_id,
        "material_id": material_id,
        "activity_type": "study_session",
        "time_spent": time_spent,
        "created_at": datetime.utcnow()
    }

    await db.progress.insert_one(progress_doc)

    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"total_study_time": time_spent // 60}}
    )

    return {"message": "Study session logged"}

@router.get("/stats")
async def get_progress_stats(user_id: str = Depends(get_current_user)):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    activities = []
    cursor = db.progress.find({"user_id": user_id}).sort("created_at", -1)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        activities.append(doc)

    quiz_results = [a for a in activities if a["activity_type"] == "quiz"]

    study_streak = analytics_service.calculate_study_streak(activities)
    weak_topics = analytics_service.identify_weak_topics(quiz_results)
    strong_topics = analytics_service.identify_strong_topics(quiz_results)
    average_score = analytics_service.calculate_average_score(quiz_results)
    time_breakdown = analytics_service.get_study_time_breakdown(activities)
    recommendations = analytics_service.generate_recommendations(
        weak_topics, strong_topics, study_streak, average_score
    )

    return {
        "total_materials": user.get("materials_count", 0),
        "total_quizzes": user.get("quizzes_taken", 0),
        "average_score": average_score,
        "total_study_time": user.get("total_study_time", 0),
        "study_streak": study_streak,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "time_breakdown": time_breakdown,
        "recommendations": recommendations,
        "recent_activities": activities[:10]
    }

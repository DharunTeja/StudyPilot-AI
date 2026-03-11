from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from app.utils.helpers import get_current_user
from app.services.ai_engine import ai_engine

router = APIRouter(prefix="/api/ai", tags=["AI Generation"])

db = None

def set_db(database):
    global db
    db = database

async def get_material_doc(material_id: str, user_id: str):
    try:
        doc = await db.materials.find_one({
            "_id": ObjectId(material_id),
            "user_id": user_id
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
        
    return doc

@router.post("/{material_id}/summarize")
async def generate_summary(material_id: str, user_id: str = Depends(get_current_user)):
    doc = await get_material_doc(material_id, user_id)
    summary = await ai_engine.generate_summary(doc["content"])
    key_concepts = await ai_engine.extract_key_concepts(doc["content"])

    await db.materials.update_one(
        {"_id": ObjectId(material_id)},
        {"$set": {"summary": summary, "key_concepts": key_concepts}}
    )

    return {"summary": summary, "key_concepts": key_concepts}

@router.post("/{material_id}/quiz")
async def generate_quiz(material_id: str, num_questions: int = 10, user_id: str = Depends(get_current_user)):
    doc = await get_material_doc(material_id, user_id)
    quizzes = await ai_engine.generate_quiz(doc["content"], num_questions)

    await db.materials.update_one(
        {"_id": ObjectId(material_id)},
        {"$set": {"quizzes": quizzes}}
    )

    return {"quizzes": quizzes}

@router.post("/{material_id}/flashcards")
async def generate_flashcards(material_id: str, num_cards: int = 15, user_id: str = Depends(get_current_user)):
    doc = await get_material_doc(material_id, user_id)
    flashcards = await ai_engine.generate_flashcards(doc["content"], num_cards)

    await db.materials.update_one(
        {"_id": ObjectId(material_id)},
        {"$set": {"flashcards": flashcards}}
    )

    return {"flashcards": flashcards}

@router.post("/{material_id}/study-plan")
async def generate_study_plan(material_id: str, days: int = 7, user_id: str = Depends(get_current_user)):
    doc = await get_material_doc(material_id, user_id)
    study_plan = await ai_engine.generate_study_plan(doc["content"], days)

    await db.materials.update_one(
        {"_id": ObjectId(material_id)},
        {"$set": {"study_plan": study_plan}}
    )

    return {"study_plan": study_plan}

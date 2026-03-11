import os
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, status
from typing import Optional
from bson import ObjectId
from app.utils.helpers import get_current_user
from app.services.document_processor import DocumentProcessor

router = APIRouter(prefix="/api/materials", tags=["Materials"])

db = None
UPLOAD_DIR = ""

def set_db(database):
    global db
    db = database

def set_upload_dir(upload_dir: str):
    global UPLOAD_DIR
    UPLOAD_DIR = upload_dir

@router.post("/upload")
async def upload_material(
    file: Optional[UploadFile] = File(None),
    title: str = Form(...),
    content: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    user_id: str = Depends(get_current_user)
):
    """Upload study material."""
    extracted_text = ""
    file_type = None
    original_filename = None

    if file:
        file_ext = file.filename.split(".")[-1].lower()
        file_type = file_ext
        original_filename = file.filename
        unique_name = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_path, "wb") as f:
            file_content = await file.read()
            f.write(file_content)

        try:
            extracted_text = DocumentProcessor.process_file(file_path, file_ext)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to process file: {str(e)}"
            )
    elif content:
        extracted_text = DocumentProcessor.process_text(content)
        file_type = "text"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either a file or text content must be provided"
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text could be extracted"
        )

    material_doc = {
        "user_id": user_id,
        "title": title,
        "content": extracted_text,
        "subject": subject,
        "file_type": file_type,
        "original_filename": original_filename,
        "created_at": datetime.utcnow(),
        "summary": None,
        "key_concepts": None,
        "flashcards": None,
        "quizzes": None,
        "study_plan": None
    }

    result = await db.materials.insert_one(material_doc)

    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"materials_count": 1}}
    )

    return {
        "message": "Material uploaded successfully",
        "material": {
            "id": str(result.inserted_id),
            "title": title,
            "content_preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            "subject": subject,
            "file_type": file_type,
            "created_at": material_doc["created_at"].isoformat()
        }
    }

@router.get("/")
async def get_materials(user_id: str = Depends(get_current_user)):
    """Get all materials for user."""
    materials = []
    cursor = db.materials.find({"user_id": user_id}).sort("created_at", -1)

    async for doc in cursor:
        materials.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "content_preview": doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"],
            "subject": doc.get("subject"),
            "file_type": doc.get("file_type"),
            "created_at": doc["created_at"].isoformat(),
            "has_summary": doc.get("summary") is not None,
            "has_flashcards": doc.get("flashcards") is not None,
            "has_quizzes": doc.get("quizzes") is not None,
            "has_study_plan": doc.get("study_plan") is not None
        })

    return {"materials": materials}

@router.get("/{material_id}")
async def get_material(material_id: str, user_id: str = Depends(get_current_user)):
    """Get specific material."""
    try:
        doc = await db.materials.find_one({
            "_id": ObjectId(material_id),
            "user_id": user_id
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "content": doc["content"],
        "subject": doc.get("subject"),
        "file_type": doc.get("file_type"),
        "original_filename": doc.get("original_filename"),
        "created_at": doc["created_at"].isoformat(),
        "summary": doc.get("summary"),
        "key_concepts": doc.get("key_concepts"),
        "flashcards": doc.get("flashcards"),
        "quizzes": doc.get("quizzes"),
        "study_plan": doc.get("study_plan")
    }

@router.delete("/{material_id}")
async def delete_material(material_id: str, user_id: str = Depends(get_current_user)):
    """Delete a material."""
    try:
        result = await db.materials.delete_one({
            "_id": ObjectId(material_id),
            "user_id": user_id
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"materials_count": -1}}
    )

    return {"message": "Material deleted successfully"}

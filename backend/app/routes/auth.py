from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserLogin
from app.utils.helpers import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

db = None

def set_db(database):
    global db
    db = database

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """Register a new user."""
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_doc = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "created_at": datetime.utcnow(),
        "study_streak": 0,
        "total_study_time": 0,
        "materials_count": 0,
        "quizzes_taken": 0,
        "average_score": 0.0
    }

    result = await db.users.insert_one(user_doc)
    token = create_access_token({"sub": str(result.inserted_id)})

    return {
        "message": "Registration successful",
        "token": token,
        "user": {
            "id": str(result.inserted_id),
            "name": user.name,
            "email": user.email
        }
    }

@router.post("/login")
async def login(user: UserLogin):
    """Login an existing user."""
    db_user = await db.users.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": str(db_user["_id"])})

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(db_user["_id"]),
            "name": db_user["name"],
            "email": db_user["email"]
        }
    }

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import auth, materials, ai, progress
from app.utils.helpers import get_current_user

# Database setup
client = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db
    import certifi
    print("🚀 Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(
        settings.MONGODB_URL, 
        tls=True,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    db = client[settings.DB_NAME]

    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.materials.create_index("user_id")
    await db.progress.create_index("user_id")
    await db.progress.create_index("created_at")

    auth.set_db(db)
    materials.set_db(db)
    materials.set_upload_dir(settings.UPLOAD_DIR)
    ai.set_db(db)
    progress.set_db(db)

    print("✅ Connected to MongoDB Atlas successfully!")
    print(f"📡 Server running on http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API docs at http://{settings.HOST}:{settings.PORT}/docs")

    yield

    print("🔌 Disconnecting from MongoDB...")
    client.close()

app = FastAPI(
    title="StudyPilot AI",
    description="🎓 AI-Powered Study Assistant for Smart Learning",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(materials.router)
app.include_router(ai.router)
app.include_router(progress.router)

@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "🎓 StudyPilot AI Backend is running with MongoDB Atlas!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/user/profile", tags=["User"])
async def get_profile(user_id: str = Depends(get_current_user)):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found"}

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"].isoformat(),
        "study_streak": user.get("study_streak", 0),
        "total_study_time": user.get("total_study_time", 0),
        "materials_count": user.get("materials_count", 0),
        "quizzes_taken": user.get("quizzes_taken", 0),
        "average_score": user.get("average_score", 0.0)
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

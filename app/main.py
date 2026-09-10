from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.tutor import router as tutor_router
from app.api.quiz import router as quiz_router
from app.api.planner import router as planner_router
from app.api.revision import router as revision_router
from app.api.assistant import router as assistant_router
from app.database.database import Base, engine
from app.models.progress import StudyProgress
from app.api.progress import router as progress_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Personal Study Assistant",
    description="GenAI-powered personal study assistant using RAG and AI agents",
    version="1.0.0",
)


app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(tutor_router)
app.include_router(quiz_router)
app.include_router(planner_router)
app.include_router(revision_router)
app.include_router(assistant_router)
app.include_router(progress_router)

@app.get("/")
def root():
    return {
        "message": "AI Personal Study Assistant is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
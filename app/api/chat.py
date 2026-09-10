from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.rag_chain import ask_documents


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: list[dict]


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:

        result = ask_documents(
            question=request.message,
            top_k=5
        )

        return ChatResponse(
            response=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
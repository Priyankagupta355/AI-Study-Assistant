from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.tutor_agent import tutor_answer


router = APIRouter(
    prefix="/tutor",
    tags=["AI Tutor"]
)


class TutorRequest(BaseModel):
    question: str


class TutorResponse(BaseModel):
    answer: str
    sources: list[dict]


@router.post("", response_model=TutorResponse)
def tutor(request: TutorRequest):

    try:

        result = tutor_answer(
            question=request.question,
            top_k=5
        )

        return TutorResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
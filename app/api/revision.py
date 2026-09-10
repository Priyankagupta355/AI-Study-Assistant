from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.revision_agent import create_revision


router = APIRouter(
    prefix="/revision",
    tags=["Revision"]
)


class RevisionRequest(BaseModel):
    topic: str


class RevisionResponse(BaseModel):
    summary: str
    key_points: list[str]
    revision_questions: list[str]
    sources: list[dict]


@router.post("", response_model=RevisionResponse)
def revision(request: RevisionRequest):

    try:

        result = create_revision(
            topic=request.topic,
            top_k=5
        )

        return RevisionResponse(
            summary=result["summary"],
            key_points=result["key_points"],
            revision_questions=result["revision_questions"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
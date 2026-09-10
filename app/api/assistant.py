from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.orchestractor import process_message


router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"]
)


class AssistantRequest(BaseModel):
    message: str


class AssistantResponse(BaseModel):
    agent: str
    response: str
    sources: list[dict]


@router.post("", response_model=AssistantResponse)
def assistant(request: AssistantRequest):

    try:

        result = process_message(
            message=request.message
        )

        return AssistantResponse(
            agent=result["agent"],
            response=result["response"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
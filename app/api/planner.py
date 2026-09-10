import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.study_planner_agent import create_study_plan


router = APIRouter(
    prefix="/planner",
    tags=["Study Planner"]
)


class PlannerRequest(BaseModel):
    subjects: list[str]
    days: int
    hours_per_day: float
    exam_goal: str = "Complete syllabus and revise"


class PlannerResponse(BaseModel):
    plan: list[dict]
    tips: list[str]


@router.post("", response_model=PlannerResponse)
def create_plan(request: PlannerRequest):

    try:

        response = create_study_plan(
            subjects=request.subjects,
            days=request.days,
            hours_per_day=request.hours_per_day,
            exam_goal=request.exam_goal
        )

        response = response.strip()

        # Remove markdown if LLM adds it
        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        # Extract JSON from response
        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:
            response = response[start:end + 1]

        data = json.loads(response)

        return PlannerResponse(
            plan=data.get("plan", []),
            tips=data.get("tips", [])
        )

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="The AI returned an invalid study plan."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
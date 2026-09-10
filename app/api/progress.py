from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.progress import StudyProgress


router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)


class ProgressRequest(BaseModel):

    subject: str
    topic: str
    study_hours: float = 0
    quiz_score: float = 0
    status: str = "in_progress"


@router.post("")
def add_progress(
    request: ProgressRequest,
    db: Session = Depends(get_db)
):

    progress = StudyProgress(
        subject=request.subject,
        topic=request.topic,
        study_hours=request.study_hours,
        quiz_score=request.quiz_score,
        status=request.status
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)

    return {
        "message": "Progress saved successfully",
        "id": progress.id
    }


@router.get("")
def get_progress(
    db: Session = Depends(get_db)
):

    progress = (
        db.query(StudyProgress)
        .order_by(StudyProgress.created_at.desc())
        .all()
    )

    return [
        {
            "id": item.id,
            "subject": item.subject,
            "topic": item.topic,
            "study_hours": item.study_hours,
            "quiz_score": item.quiz_score,
            "status": item.status,
            "created_at": item.created_at
        }
        for item in progress
    ]


@router.get("/summary")
def get_progress_summary(
    db: Session = Depends(get_db)
):

    progress = (
        db.query(StudyProgress)
        .order_by(StudyProgress.created_at.desc())
        .all()
    )

    if not progress:
        return {
            "total_study_hours": 0,
            "average_quiz_Score": 0,
            "completed_topics": 0,
            "total_topics": 0
        }


    total_study_hours = sum(
        item.study_hours or 0
        for item in progress
    )


    average_quiz_score = sum(
        item.quiz_score or 0
        for item in progress
    ) / len(progress)

    completed_topics = sum(
        1
        for item in progress
        if item.status == "completed"
    )

    return {
        "total_study_hours": round(total_study_hours, 2),
        "average_quiz_score": round(average_quiz_score, 2),
        "completed_topics": completed_topics,
        "total_topics": len(progress)
    }


@router.get("/subjects")
def get_subject_progress(
    db: Session = Depends(get_db)
):

    progress = (
        db.query(StudyProgress)
        .order_by(StudyProgress.subject)
        .all()
    )

    subjects = {}

    for item in progress:

        subject = item.subject

        if subject not in subjects:
            subjects[subject] = {
                "subject": subject,
                "total_study_hours": 0,
                "quiz_scores": [],
                "completed_topics": 0,
                "total_topics": 0
            }

        subjects[subject]["total_study_hours"] += (
            item.study_hours or 0
        )

        subjects[subject]["quiz_scores"].append(
            item.quiz_score or 0
        )

        subjects[subject]["total_topics"] += 1

        if item.status == "completed":
            subjects[subject]["completed_topics"] += 1

    result = []

    for subject_data in subjects.values():

        scores = subject_data["quiz_scores"]

        average_score = (
            sum(scores) / len(scores)
            if scores
            else 0
        )

        result.append({
            "subject": subject_data["subject"],
            "total_study_hours": round(
                subject_data["total_study_hours"],
                2
            ),
            "average_quiz_score": round(
                average_score,
                2
            ),
            "completed_topics": subject_data[
                "completed_topics"
            ],
            "total_topics": subject_data[
                "total_topics"
            ]
        })

    return result
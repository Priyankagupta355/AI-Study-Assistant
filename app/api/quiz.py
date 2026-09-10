from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from pydantic import BaseModel
from app.database.database import get_db
from app.models.progress import StudyProgress

from app.agents.quiz_agent import generate_quiz


router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


class MCQQuestion(BaseModel):
    question: str
    options: dict[str, str]
    correct_answer: str
    explanation: str


class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5


class QuizResponse(BaseModel):
    questions: list[MCQQuestion]
    sources: list[dict]


@router.post("", response_model=QuizResponse)
def quiz(request: QuizRequest):

    try:

        result = generate_quiz(
            topic=request.topic,
            num_questions=request.num_questions
        )

        return QuizResponse(
            questions=result["questions"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


class QuizSubmission(BaseModel):
    subject: str
    topic: str
    answers: dict[str, str]
    questions: list[MCQQuestion]


@router.post("/submit")
def submit_quiz(
    submission: QuizSubmission,
    db: Session = Depends(get_db)
):

    if not submission.questions:
        raise HTTPException(
            status_code=400,
            detail="No quiz questions provided"
        )

    total_questions = len(submission.questions)
    correct_answers = 0

    for index, question in enumerate(submission.questions):

        question_key = str(index)

        user_answer = submission.answers.get(
            question_key
        )

        if user_answer == question.correct_answer:
            correct_answers += 1

    score = (
        correct_answers / total_questions
    ) * 100

    progress = StudyProgress(
        subject=submission.subject,
        topic=submission.topic,
        study_hours=0,
        quiz_score=score,
        status="completed"
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)

    return {
        "message": "Quiz submitted successfully",
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score": round(score, 2),
        "progress_id": progress.id
    }
    
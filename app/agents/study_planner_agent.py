from app.llm.groq_client import generate_response


def create_study_plan(
    subjects: list[str],
    days: int,
    hours_per_day: float,
    exam_goal: str = "Complete syllabus and revise"
) -> str:

    subjects_text = ", ".join(subjects)

    system_message = """
You are an AI Study Planner.

Your job is to create a practical and balanced study plan for students.

Rules:
1. Divide the available study time realistically.
2. Cover all provided subjects.
3. Include revision sessions.
4. Include practice or quiz sessions.
5. Give extra attention to difficult or important subjects.
6. Do not overload a single day.
7. Keep the plan simple and achievable.
8. Return the plan in clear JSON format.
9. Do not use markdown code fences.
"""

    user_message = f"""
Create a study plan using these details:

Subjects:
{subjects_text}

Number of days:
{days}

Study hours per day:
{hours_per_day}

Goal:
{exam_goal}

Create a day-by-day study plan.

Return this JSON structure:

{{
    "plan": [
        {{
            "day": 1,
            "tasks": [
                {{
                    "subject": "Subject name",
                    "activity": "Topic or activity",
                    "hours": 1.5
                }}
            ]
        }}
    ],
    "tips": [
        "Study tip 1",
        "Study tip 2"
    ]
}}
"""

    response = generate_response(
        user_message=user_message,
        system_message=system_message
    )

    return response
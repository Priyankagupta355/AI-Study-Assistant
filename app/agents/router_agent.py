import json

from app.llm.groq_client import generate_response


def route_query(message: str) -> dict:

    system_message = """
You are an AI Study Assistant Router.

Your job is to identify what the student wants and select the correct agent.

Available agents:

1. chat
   - General questions
   - Questions about uploaded study notes
   - Normal conversation

2. tutor
   - Student wants an explanation
   - Student wants to learn a concept
   - Student asks "explain", "teach", "how does this work"

3. quiz
   - Student wants MCQs
   - Student wants a quiz
   - Student wants practice questions

4. planner
   - Student wants a study schedule
   - Student wants a day-wise study plan
   - Student asks how to prepare for an exam

5. revision
   - Student wants revision notes
   - Student wants summary
   - Student wants key points
   - Student wants quick revision

Return ONLY valid JSON.

Format:

{
    "agent": "chat",
    "reason": "short reason"
}

The agent must be exactly one of:
chat, tutor, quiz, planner, revision
"""

    user_message = f"""
Student message:

{message}

Select the most appropriate agent.
"""

    response = generate_response(
        user_message=user_message,
        system_message=system_message
    )

    response = response.strip()

    # Remove markdown code fences
    if response.startswith("```json"):
        response = response[7:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    # Extract JSON
    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1:
        response = response[start:end + 1]

    try:

        result = json.loads(response)

    except json.JSONDecodeError:

        raise ValueError(
            "Router returned invalid JSON."
        )

    agent = result.get("agent")

    allowed_agents = {
        "chat",
        "tutor",
        "quiz",
        "planner",
        "revision"
    }

    if agent not in allowed_agents:
        raise ValueError(
            f"Invalid agent selected: {agent}"
        )

    return {
        "agent": agent,
        "reason": result.get("reason", "")
    }
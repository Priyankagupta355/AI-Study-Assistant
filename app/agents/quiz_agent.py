import json

from app.llm.groq_client import generate_response
from app.rag.retriever import search_documents


def generate_quiz(
    topic: str,
    num_questions: int = 5,
    top_k: int = 5
) -> dict:

    results = search_documents(
        query=topic,
        top_k=top_k
    )

    if not results:
        return {
            "questions": [],
            "sources": []
        }

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    system_message = """
You are an AI Quiz Generator.

Generate multiple-choice questions using ONLY the provided study notes.

IMPORTANT:
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT use ```json.
- Do NOT add any explanation before or after the JSON.
- Create exactly the requested number of questions.
- Every question must have exactly 4 options: A, B, C, D.
- correct_answer must contain only A, B, C, or D.
"""

    user_message = f"""
Study Notes:

{context}

Topic:

{topic}

Generate exactly {num_questions} MCQs.

Return ONLY this JSON:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "A",
            "explanation": "Short explanation"
        }}
    ]
}}
"""

    response = generate_response(
        user_message=user_message,
        system_message=system_message
    )

    # Remove markdown code fences if the model adds them
    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    # Try to extract JSON if the model adds extra text
    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1:
        response = response[start:end + 1]

    try:

        quiz_data = json.loads(response)

    except json.JSONDecodeError as e:

        print("RAW AI RESPONSE:")
        print(response)

        raise ValueError(
            f"The AI returned invalid JSON: {str(e)}"
        )

    questions = quiz_data.get(
        "questions",
        []
    )

    if not isinstance(questions, list):
        raise ValueError(
            "Invalid quiz format: questions must be a list."
        )

    sources = []

    for result in results:

        metadata = result["metadata"]

        sources.append({
            "filename": metadata.get("filename"),
            "chunk_index": metadata.get("chunk_index")
        })

    return {
        "questions": questions,
        "sources": sources
    }
import json

from app.llm.groq_client import generate_response
from app.rag.retriever import search_documents


def create_revision(
    topic: str,
    top_k: int = 5
) -> dict:

    results = search_documents(
        query=topic,
        top_k=top_k
    )

    if not results:
        return {
            "summary": "",
            "key_points": [],
            "revision_questions": [],
            "sources": []
        }

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    system_message = """
You are an AI Revision Assistant.

Create revision material using ONLY the provided study notes.

Rules:
1. Keep the explanation concise and exam-friendly.
2. Extract the most important concepts.
3. Create short revision questions.
4. Do not invent information.
5. Return ONLY valid JSON.
6. Do not use markdown code fences.
"""

    user_message = f"""
Study Notes:

{context}

Topic:

{topic}

Create revision material.

Return exactly this JSON structure:

{{
    "summary": "A short summary of the topic",
    "key_points": [
        "Important point 1",
        "Important point 2",
        "Important point 3"
    ],
    "revision_questions": [
        "Question 1",
        "Question 2",
        "Question 3"
    ]
}}
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

        revision_data = json.loads(response)

    except json.JSONDecodeError as e:

        print("RAW AI RESPONSE:")
        print(response)

        raise ValueError(
            f"The AI returned invalid JSON: {str(e)}"
        )

    sources = []

    for result in results:

        metadata = result["metadata"]

        sources.append({
            "filename": metadata.get("filename"),
            "chunk_index": metadata.get("chunk_index")
        })

    return {
        "summary": revision_data.get("summary", ""),
        "key_points": revision_data.get("key_points", []),
        "revision_questions": revision_data.get(
            "revision_questions",
            []
        ),
        "sources": sources
    }
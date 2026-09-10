from app.rag.retriever import search_documents
from app.llm.groq_client import generate_response


def tutor_answer(
    question: str,
    top_k: int = 5
) -> dict:

    results = search_documents(
        query=question,
        top_k=top_k
    )

    if not results:
        return {
            "answer": "I could not find relevant information in your notes.",
            "sources": []
        }

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    system_message = """
You are an AI Personal Tutor.

Your job is to teach the student using the provided study notes.

Follow these rules:

1. Use only information from the provided notes.
2. Explain concepts in simple language.
3. Break difficult concepts into smaller parts.
4. Give a simple example when possible.
5. Mention important points clearly.
6. If the answer is not available in the notes, say so honestly.
7. Do not invent facts.
8. Encourage the student to understand the concept rather than just memorize it.
"""

    user_message = f"""
Study Notes:

{context}

Student Question:

{question}

Teach this topic to the student.
"""

    answer = generate_response(
        user_message=user_message,
        system_message=system_message
    )

    sources = []

    for result in results:
        metadata = result["metadata"]
        sources.append({
            "filename": metadata.get("filename"),
            "chunk_index": metadata.get("chunk_index")
        })

    return {
        "answer": answer,
        "sources": sources
    }

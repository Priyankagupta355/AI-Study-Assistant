from app.llm.groq_client import generate_response
from app.llm.groq_client import generate_general_response
from app.rag.retriever import search_documents


def ask_documents(
    question: str,
    top_k: int = 5
) -> dict:

    results = search_documents(
        query=question,
        top_k=top_k,
        max_distance=1.2
    )

    # No relevant information in uploaded notes
    if not results:

        answer = generate_general_response(
            question
        )

        return {
            "answer": answer,
            "sources": [],
            "source_type": "general_knowledge"
        }

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    system_message = """
You are an AI Personal Study Assistant.

Answer the student's question using the
provided study notes.

Rules:

1. Prefer information from the study notes.
2. Explain the answer in simple language.
3. Do not invent information.
4. If the notes do not contain the answer,
   clearly say that.
"""

    user_message = f"""
Study Notes:

{context}

Student Question:

{question}

Answer using the study notes.
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
        "sources": sources,
        "source_type": "uploaded_notes"
    }
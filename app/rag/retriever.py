from app.rag.vector_store import vector_store


def search_documents(
    query: str,
    top_k: int = 5,
    max_distance: float = 1.2
) -> list[dict]:

    query_embedding = (
        vector_store.embedding_model
        .encode(query)
        .tolist()
    )

    results = vector_store.collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved_chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        # Only keep relevant chunks
        if distance <= max_distance:

            retrieved_chunks.append({
                "text": document,
                "metadata": metadata,
                "distance": distance,
            })

    return retrieved_chunks
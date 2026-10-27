import re

from app.rag.vector_store import vector_store


def _query_variants(query: str) -> list[str]:
    variants = [query]
    words = re.findall(r"[\w+#.]+", query.lower())

    if "skill" in words or "skills" in words:
        question_words = {
            "about", "are", "can", "does", "do", "her", "his",
            "list", "me", "of", "please", "show", "tell", "the",
            "what", "you",
        }
        subject = " ".join(
            word for word in words
            if word not in question_words and word not in {"skill", "skills"}
        )
        variants.append(
            f"{subject} technical skills programming languages frameworks"
        )

    return list(dict.fromkeys(variant.strip() for variant in variants if variant.strip()))


def search_documents(
    query: str,
    top_k: int = 5,
    max_distance: float = 1.5
) -> list[dict]:

    collection_size = vector_store.collection.count()
    if collection_size == 0:
        return []

    candidates = {}

    for query_variant in _query_variants(query):
        query_embedding = (
            vector_store.embedding_model
            .encode(query_variant)
            .tolist()
        )

        results = vector_store.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k * 10, collection_size),
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            if distance <= max_distance:
                candidate = candidates.get(document)
                if candidate is None or distance < candidate["distance"]:
                    candidates[document] = {
                        "text": document,
                        "metadata": metadata,
                        "distance": distance,
                    }

    return sorted(
        candidates.values(),
        key=lambda result: result["distance"]
    )[:top_k]
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from app.config.settings import settings


class VectorStore:

    def __init__(self):
        self.embedding_model = SentenceTransformer(
            settings.embedding_model
        )

        Path(settings.chroma_db_path).mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=settings.chroma_db_path
        )

        self.collection = self.client.get_or_create_collection(
            name="study_documents"
        )

    def add_chunks(
        self,
        chunks: list[str],
        document_id: str,
        filename: str
    ):

        if not chunks:
            return 0

        # Create embeddings for chunks
        embeddings = self.embedding_model.encode(
            chunks
        ).tolist()

        # Unique ID for every chunk
        ids = [
            f"{document_id}_{index}"
            for index in range(len(chunks))
        ]

        # Metadata for every chunk
        metadatas = [
            {
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index
            }
            for index in range(len(chunks))
        ]

        # Store chunks in ChromaDB
        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return len(chunks)


vector_store = VectorStore()
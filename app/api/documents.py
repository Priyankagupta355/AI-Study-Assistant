from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.rag.document_loader import extract_text_from_pdf
from app.rag.text_splitter import split_text
from app.rag.vector_store import vector_store

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


DOCUMENTS_DIR = Path("data/documents")
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    file_id = str(uuid.uuid4())
    file_path = DOCUMENTS_DIR / f"{file_id}.pdf"

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(str(file_path))

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF",
            )

        chunks = split_text(text)

        stored_chunks = vector_store.add_chunks(
            chunks=chunks,
            document_id=file_id,
            filename=file.filename,
        )

        return {
            "message": "PDF uploaded  and indexed successfully",
            "filename": file.filename,
            "file_id": file_id,
            "pages_text_length": len(text),
            "chunks": len(chunks),
            "stored_chunks": stored_chunks,
            "status": "indexed and processed",
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
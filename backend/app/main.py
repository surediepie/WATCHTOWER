from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Depends,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import os
import shutil

from app.database import Base, engine, get_db
import app.models

from app.models import User
from app.schemas import UserCreate, UserLogin
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.dependencies import get_current_user

from app.services.pdf_service import extract_text
from app.services.chunk_service import chunk_text
from app.services.vector_service import (
    store_chunks,
    delete_document_embeddings,
)
from app.services.search_service import search_documents
from app.services.gemini_service import (
    summarize_document,
    explain_with_ai,
)
from app.services.document_service import (
    create_document,
    get_user_documents,
    get_document,
    delete_document,
)

app = FastAPI(title="WATCHTOWER API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def root():
    return {"message": "WATCHTOWER Backend Running"}


# -------------------------------------------------
# Upload PDF
# -------------------------------------------------

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_text(file_path)
    print("Pages:", len(pages))
    print(pages[:2])
    print("Pages extracted:", len(pages))
    print(pages[:2])

    chunks = chunk_text(pages)
    print("Chunks:", len(chunks))
    print("Chunks created:", len(chunks))

    try:
        print("Calling store_chunks...")

        store_chunks(
            chunks,
            current_user.id,
            file.filename,
        )

        print("store_chunks finished.")

    except Exception as e:
        print("STORE CHUNKS ERROR:")
        print(type(e).__name__)
        print(e)
        raise

    create_document(
        db=db,
        filename=file.filename,
        size=os.path.getsize(file_path),
        user_id=current_user.id,
    )

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "pages": len(pages),
        "chunks": len(chunks),
    }

# -------------------------------------------------
# Documents
# -------------------------------------------------

@app.get("/documents")
def documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    docs = get_user_documents(
        db,
        current_user.id,
    )

    return [
        {
            "id": doc.id,
            "name": doc.filename,
            "size": round(doc.size / 1024, 2),
        }
        for doc in docs
    ]

@app.delete("/documents/{document_id}")
def delete_user_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = get_document(
        db,
        document_id,
        current_user.id,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        document.filename,
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    delete_document_embeddings(
        current_user.id,
        document.filename,
    )

    delete_document(
        db,
        document,
    )

    return {
        "message": "Document deleted successfully",
    }


# -------------------------------------------------
# Register
# -------------------------------------------------

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(
        {"sub": new_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
        },
    }


# -------------------------------------------------
# Login
# -------------------------------------------------

@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        user.password,
        existing_user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(
        {"sub": existing_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": existing_user.id,
            "name": existing_user.name,
            "email": existing_user.email,
        },
    }


# -------------------------------------------------
# Chat
# -------------------------------------------------

class ChatRequest(BaseModel):
    question: str


# -------------------------------------------------
# Chat
# -------------------------------------------------

class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    results = search_documents(
        request.question,
        current_user.id,
    )

    context = "\n\n".join(
        source["text"]
        for source in results
    )

    document_answer = summarize_document(
        request.question,
        context,
    )

    ai_answer = explain_with_ai(
        request.question,
        document_answer,
    )

    print("DOCUMENT ANSWER:")
    print(document_answer)

    print("AI ANSWER:")
    print(ai_answer)

    return {
        "question": request.question,
        "document_answer": document_answer,
        "ai_answer": ai_answer,
        "sources": results,
    }
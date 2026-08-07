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
from app.services.vector_service import store_chunks
from app.services.search_service import search_documents
from app.services.gemini_service import ask_gemini
from app.services.document_service import (
    create_document,
    get_user_documents,
)

app = FastAPI(title="WATCHTOWER API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
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

    text = extract_text(file_path)

    chunks = chunk_text(text)

    store_chunks(
        chunks,
        current_user.id,
        file.filename,
    )

    create_document(
        db=db,
        filename=file.filename,
        size=os.path.getsize(file_path),
        user_id=current_user.id,
    )

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "characters": len(text),
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

    return {
        "message": "User registered successfully",
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

    answer = ask_gemini(
        request.question,
        context,
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": results,
    }
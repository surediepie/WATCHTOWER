from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import shutil

from app.services.pdf_service import extract_text
from app.services.chunk_service import chunk_text
from app.services.vector_service import store_chunks
from app.services.search_service import search_documents
from app.services.gemini_service import ask_gemini
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.auth import hash_password
from app.database import engine, Base
import app.models

app = FastAPI(title="WATCHTOWER API")
Base.metadata.create_all(bind=engine)

# CORS
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


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    chunks = chunk_text(text)

    print("About to call store_chunks()")

    store_chunks(chunks, file.filename)

    print("Returned from store_chunks()")

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
        "preview": chunks[0],
    }

@app.get("/documents")
def get_documents():
    documents = []

    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.isfile(path):
            documents.append({
                "name": filename,
                "size": round(os.path.getsize(path) / 1024, 2)
            })

    return documents

class ChatRequest(BaseModel):
    question: str

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return {"message": "Email already registered"}

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    results = search_documents(request.question)

    context = "\n\n".join(
        source["text"] for source in results
    )

    answer = ask_gemini(request.question, context)

    return {
        "question": request.question,
        "answer": answer,
        "sources": results,
    }
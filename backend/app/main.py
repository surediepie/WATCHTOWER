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
    search_documents,
)
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


# -------------------------------------------------
# FastAPI App
# -------------------------------------------------

app = FastAPI(title="WATCHTOWER API")


# -------------------------------------------------
# Database
# -------------------------------------------------

Base.metadata.create_all(bind=engine)


# -------------------------------------------------
# CORS
# -------------------------------------------------

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


# -------------------------------------------------
# Vercel Services Prefix Middleware
# -------------------------------------------------

class ServicePrefixMiddleware:
    def __init__(self, app, prefix: str) -> None:
        self.app = app
        self.prefix = prefix
        self.prefix_bytes = prefix.encode()

    async def __call__(self, scope, receive, send):
        if scope["type"] in {"http", "websocket"}:
            path = scope.get("path", "")

            if path == self.prefix or path.startswith(
                f"{self.prefix}/"
            ):
                scope = {
                    **scope,
                    "path": path[len(self.prefix):] or "/",
                    "root_path": (
                        f"{scope.get('root_path', '')}"
                        f"{self.prefix}"
                    ),
                }

                raw_path = scope.get("raw_path")

                if (
                    isinstance(raw_path, bytes)
                    and raw_path.startswith(self.prefix_bytes)
                ):
                    scope["raw_path"] = (
                        raw_path[len(self.prefix_bytes):] or b"/"
                    )

        await self.app(scope, receive, send)


app.add_middleware(
    ServicePrefixMiddleware,
    prefix="/svc/api",
)


# -------------------------------------------------
# Upload Configuration
# -------------------------------------------------

UPLOAD_FOLDER = "/tmp/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True,
)


# -------------------------------------------------
# Root
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "WATCHTOWER Backend Running"
    }


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
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    pages = extract_text(file_path)

    print("Pages:", len(pages))
    print(pages[:2])

    chunks = chunk_text(pages)

    print("Chunks:", len(chunks))

    document = create_document(
        db=db,
        filename=file.filename,
        size=os.path.getsize(file_path),
        user_id=current_user.id,
    )

    try:
        print("Calling store_chunks...")

        store_chunks(
            chunks,
            current_user.id,
            file.filename,
            document.id,
        )

        print("store_chunks finished.")

    except Exception as e:
        print("STORE CHUNKS ERROR:")
        print(type(e).__name__)
        print(e)
        raise

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
            "size": round(
                doc.size / 1024,
                2,
            ),
        }
        for doc in docs
    ]


# -------------------------------------------------
# Delete Document
# -------------------------------------------------

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
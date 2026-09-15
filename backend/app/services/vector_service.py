import os

from dotenv import load_dotenv
from google import genai
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import DocumentChunk


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not configured"
    )

client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768


def create_embedding(text: str, task_type: str):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config={
            "task_type": task_type,
            "output_dimensionality": EMBEDDING_DIMENSION,
        },
    )

    return response.embeddings[0].values


def store_chunks(chunks, user_id, source, document_id):
    db: Session = SessionLocal()

    try:
        for chunk in chunks:
            embedding = create_embedding(
                chunk["text"],
                "RETRIEVAL_DOCUMENT",
            )

            db_chunk = DocumentChunk(
                document_id=document_id,
                user_id=user_id,
                source=source,
                page=chunk["page"],
                text=chunk["text"],
                embedding=embedding,
            )

            db.add(db_chunk)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def delete_document_embeddings(user_id, source):
    db: Session = SessionLocal()

    try:
        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.user_id == user_id,
                DocumentChunk.source == source,
            )
            .all()
        )

        for chunk in chunks:
            db.delete(chunk)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def search_documents(query, user_id, n_results=5):
    db: Session = SessionLocal()

    try:
        query_embedding = create_embedding(
            query,
            "RETRIEVAL_QUERY",
        )

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        )

        statement = (
            select(DocumentChunk, distance.label("distance"))
            .where(DocumentChunk.user_id == user_id)
            .order_by(distance)
            .limit(n_results)
        )

        rows = db.execute(statement).all()

        results = []

        for chunk, distance_value in rows:
            results.append(
                {
                    "text": chunk.text,
                    "source": chunk.source,
                    "page": chunk.page,
                    "distance": float(distance_value),
                }
            )

        return results

    finally:
        db.close()
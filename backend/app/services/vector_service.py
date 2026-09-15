import json
import math

from google import genai
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import DocumentChunk


client = genai.Client()

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
                embedding=json.dumps(embedding),
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


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_documents(query, user_id, n_results=5):
    db: Session = SessionLocal()

    try:
        query_embedding = create_embedding(
            query,
            "RETRIEVAL_QUERY",
        )

        chunks = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.user_id == user_id)
            .all()
        )

        scored_chunks = []

        for chunk in chunks:
            embedding = json.loads(chunk.embedding)

            similarity = cosine_similarity(
                query_embedding,
                embedding,
            )

            scored_chunks.append(
                (similarity, chunk)
            )

        scored_chunks.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        results = []

        for similarity, chunk in scored_chunks[:n_results]:
            results.append(
                {
                    "text": chunk.text,
                    "source": chunk.source,
                    "page": chunk.page,
                    "distance": 1 - similarity,
                }
            )

        return results

    finally:
        db.close()
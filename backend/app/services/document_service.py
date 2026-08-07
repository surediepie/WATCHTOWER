from sqlalchemy.orm import Session

from app.models import Document


def create_document(
    db: Session,
    filename: str,
    size: int,
    user_id: int,
):
    document = Document(
        filename=filename,
        size=size,
        user_id=user_id,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_user_documents(
    db: Session,
    user_id: int,
):
    return (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.id.desc())
        .all()
    )


def delete_document(
    db: Session,
    document_id: int,
    user_id: int,
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == user_id,
        )
        .first()
    )

    if document:
        db.delete(document)
        db.commit()

    return document
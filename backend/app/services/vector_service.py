print("HELLO FROM VECTOR SERVICE")

import chromadb
from sentence_transformers import SentenceTransformer

print("Loading ChromaDB...")

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="watchtower_documents"
)

print("Collection ready!")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")


def store_chunks(chunks, user_id, source):
    print(f"Storing {len(chunks)} chunks...")

    print("USER:", user_id)
    print("Stored user_id type:", type(user_id))
    print("SOURCE:", source)
    print("CHUNKS:", len(chunks))

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(texts).tolist()

    ids = [
        f"user{user_id}_{source}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "user_id": user_id,
            "source": source,
            "page": chunk["page"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print("Chunks stored successfully!")
    print("COLLECTION COUNT:", collection.count())
    print("PEEK:", collection.peek())

def delete_document_embeddings(user_id, source):
    results = collection.get(
        where={
            "$and": [
                {
                    "user_id": user_id,
                },
                {
                    "source": source,
                },
            ]
        }
    )

    if results["ids"]:
        collection.delete(
            ids=results["ids"],
        )

        print(
            f"Deleted {len(results['ids'])} embeddings."
        )
    else:
        print("No embeddings found.")
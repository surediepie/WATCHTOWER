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


def store_chunks(chunks, source):
    print(f"Storing {len(chunks)} chunks...")

    embeddings = model.encode(chunks).tolist()

    ids = [f"{source}_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": source}] * len(chunks),
    )

    print("Chunks stored successfully!")
    print("Total documents in ChromaDB:", collection.count())
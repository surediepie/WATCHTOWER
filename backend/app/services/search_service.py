from app.services.vector_service import collection, model

def search_documents(query, user_id, n_results=5):
    print("=" * 50)
    print("SEARCH CALLED")
    print("Query:", query)
    print("User ID:", user_id)

    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        where={
            "user_id": user_id,
        },
    )

    print("RAW RESULTS:")
    print(results)

    sources = []

    if not results["documents"] or not results["documents"][0]:
        print("NO DOCUMENTS FOUND")
        return sources

    for i in range(len(results["documents"][0])):
        sources.append(
            {
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "page": results["metadatas"][0][i]["page"],
                "distance": results["distances"][0][i],
            }
        )

    print("FOUND", len(sources), "MATCHES")
    return sources
from app.services.vector_service import collection, model


def search_documents(query, user_id, n_results=5):
    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        where={"user_id": user_id},
    )

    sources = []

    for i in range(len(results["documents"][0])):
        sources.append(
            {
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i],
            }
        )

    return sources
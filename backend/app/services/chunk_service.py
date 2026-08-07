def chunk_text(pages, chunk_size=500, overlap=100):
    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(
                    {
                        "text": chunk,
                        "page": page_number,
                    }
                )

            start += chunk_size - overlap

    return chunks
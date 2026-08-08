# WATCHTOWER Document Agent

## Purpose

The WATCHTOWER Document Agent handles document-grounded question answering.

## Workflow

1. Receive the authenticated user's question.
2. Identify the user's document scope.
3. Generate a semantic representation of the question.
4. Search the user's document embeddings in ChromaDB.
5. Retrieve the most relevant document chunks.
6. Pass the retrieved context to Gemini.
7. Generate a clear answer grounded in the retrieved documents.
8. Preserve source and page information when available.

## Grounding Rules

- Prefer retrieved document context over general knowledge.
- Do not invent information that is absent from the retrieved context.
- Keep document information tied to the authenticated user.
- Clearly distinguish document-grounded answers from additional explanations.

## Security Rules

- Never expose API keys or credentials.
- Never retrieve another user's documents.
- Never bypass authentication or authorization.
- Treat uploaded documents as user-owned data.

## Project Components

- Frontend: Next.js
- Backend: FastAPI
- PDF extraction: PyMuPDF
- Embeddings: Sentence Transformers
- Vector database: ChromaDB
- Language model: Google Gemini
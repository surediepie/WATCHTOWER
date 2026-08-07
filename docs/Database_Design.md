# Database Design

# Overview

WATCHTOWER stores user accounts, uploaded documents, chat history, and document metadata.

---

# Users

Stores user account information.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique user ID |
| name | String | Full name |
| email | String | Email address |
| password | String | Encrypted password |
| created_at | Timestamp | Account creation date |

---

# Documents

Stores uploaded document information.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Document ID |
| user_id | UUID | Owner of document |
| title | String | Document name |
| file_path | String | File location |
| upload_date | Timestamp | Upload time |

---

# Chat History

Stores previous conversations.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Chat ID |
| user_id | UUID | User |
| question | Text | User question |
| answer | Text | AI response |
| created_at | Timestamp | Time |

---

# Embeddings

Stores vector embeddings used for semantic search.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Embedding ID |
| document_id | UUID | Related document |
| page_number | Integer | Source page |
| embedding | Vector | Vector representation |

---

# Relationships

- One User can upload many Documents.
- One User can have many Chat History records.
- One Document can have many Embeddings.
- Every Chat response references one or more Documents.

---

# Database Technologies

- PostgreSQL — User accounts, documents, chat history.
- ChromaDB — Document embeddings for semantic search.
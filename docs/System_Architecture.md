# System Architecture

# Project Name

WATCHTOWER

---

# Overview

WATCHTOWER follows a client-server architecture where users interact with a web application to upload documents, ask questions, and receive verified answers with citations.

The system processes uploaded documents, stores their contents, retrieves relevant information when a question is asked, and generates a response backed by evidence from the original documents.

---

# High-Level Architecture

User
│
▼
Frontend (Next.js)
│
▼
Backend API (FastAPI)
│
├──────────────┐
│              │
▼              ▼
PostgreSQL   ChromaDB
(User Data) (Document Embeddings)
│              │
└───────┬──────┘
        ▼
    Gemini API
        │
        ▼
Answer + Citation
        │
        ▼
Frontend
        │
        ▼
User

---

# Components

## Frontend

Responsibilities:

- User authentication
- Dashboard
- Document upload
- Chat interface
- Display citations
- Display chat history

Technology:

- Next.js
- Tailwind CSS

---

## Backend

Responsibilities:

- Handle API requests
- Process uploaded documents
- Generate embeddings
- Retrieve relevant document sections
- Communicate with Gemini
- Return answers

Technology:

- FastAPI

---

## Database

PostgreSQL stores:

- Users
- Uploaded document metadata
- Chat history

---

## Vector Database

ChromaDB stores:

- Document embeddings
- Semantic search index

This allows WATCHTOWER to quickly find relevant sections from uploaded documents.

---

## AI Model

Gemini is responsible for:

- Understanding user questions
- Generating answers
- Producing natural language responses
- Using retrieved document context to answer accurately

---

# Application Workflow

Step 1

User logs into WATCHTOWER.

↓

Step 2

User uploads one or more PDF documents.

↓

Step 3

The backend extracts text from the documents.

↓

Step 4

The extracted content is converted into embeddings and stored in ChromaDB.

↓

Step 5

The user asks a question.

↓

Step 6

The backend searches ChromaDB for the most relevant document sections.

↓

Step 7

Relevant context is sent to Gemini.

↓

Step 8

Gemini generates an answer based only on the retrieved context.

↓

Step 9

The backend returns:

- Answer
- Document Name
- Page Number
- Supporting Citation

↓

Step 10

The frontend displays the response to the user.

---

# Security

- User authentication
- Secure document storage
- Protected API endpoints
- No exposure of API keys
- User data isolation

---

# Deployment

Frontend

- Vercel

Backend

- Railway or Render

Database

- PostgreSQL

Vector Database

- ChromaDB

AI

- Google Gemini API
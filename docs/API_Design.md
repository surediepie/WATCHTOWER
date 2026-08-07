# API Design

## Overview

The WATCHTOWER API enables communication between the frontend and backend. It handles user authentication, document management, document search, chat requests, and profile management.

---

# Authentication

## Register User

**Endpoint**

POST /api/auth/register

**Purpose**

Creates a new user account.

---

## Login User

**Endpoint**

POST /api/auth/login

**Purpose**

Authenticates a user and grants access to the application.

---

# Documents

## Upload Document

**Endpoint**

POST /api/documents/upload

**Purpose**

Uploads one or more PDF documents for processing.

---

## Get Documents

**Endpoint**

GET /api/documents

**Purpose**

Returns all uploaded documents for the current user.

---

## Delete Document

**Endpoint**

DELETE /api/documents/{id}

**Purpose**

Removes a document from the system.

---

# Chat

## Ask Question

**Endpoint**

POST /api/chat

**Purpose**

Accepts a user question, searches the uploaded documents, and returns an answer with citations.

---

## Chat History

**Endpoint**

GET /api/chat/history

**Purpose**

Returns previous conversations of the logged-in user.

---

# Search

## Search Documents

**Endpoint**

GET /api/search

**Purpose**

Searches across uploaded documents using keywords or natural language.

---

# User

## Get Profile

**Endpoint**

GET /api/user/profile

**Purpose**

Returns the current user's profile information.

---

## Update Profile

**Endpoint**

PUT /api/user/profile

**Purpose**

Updates user profile details.

---

# API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/auth/register | Register a new user |
| POST | /api/auth/login | Login user |
| POST | /api/documents/upload | Upload PDF documents |
| GET | /api/documents | Retrieve uploaded documents |
| DELETE | /api/documents/{id} | Delete a document |
| POST | /api/chat | Ask a question |
| GET | /api/chat/history | Retrieve chat history |
| GET | /api/search | Search documents |
| GET | /api/user/profile | Get user profile |
| PUT | /api/user/profile | Update user profile |
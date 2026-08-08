# WATCHTOWER Agents and Skills

## Custom Agent

### WATCHTOWER Document Agent

**Location:** `agents/watchtower-document-agent.md`

The Document Agent defines the workflow for processing user questions,
retrieving relevant document context, maintaining user isolation, and
generating grounded responses.

## Custom Skill

### Document Retrieval Skill

**Location:** `skills/document-retrieval/SKILL.md`

The Document Retrieval Skill defines the semantic retrieval process used
to search uploaded documents through ChromaDB and provide relevant context
for AI response generation.

## Workflow

```text
User Question
      |
      v
WATCHTOWER Document Agent
      |
      v
Document Retrieval Skill
      |
      v
Query Embedding
      |
      v
ChromaDB Semantic Search
      |
      v
Relevant Document Chunks
      |
      v
Gemini
      |
      v
Grounded Response
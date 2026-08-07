import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)


def summarize_document(question, context):
    prompt = f"""
You are WATCHTOWER.

Your job is ONLY to answer from the uploaded document.

Rules:
- Do NOT use outside knowledge.
- Summarize only what exists in the document.
- If the document does not contain the answer, reply exactly:

NOT_FOUND

Document:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
    )

    return response.text.strip()


def explain_with_ai(question):
    prompt = f"""
You are an expert networking professor.

Explain the following topic clearly using your own knowledge.

Question:
{question}

Requirements:
- Beginner friendly
- Give examples
- Explain concepts clearly
- Use bullet points when useful
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
    )

    return response.text.strip()
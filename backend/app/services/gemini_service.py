import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def summarize_document(question, context):
    """
    Generates a summary ONLY from the uploaded document.
    """

    if not context.strip():
        return None

    prompt = f"""
You are WATCHTOWER.

Your ONLY job is to answer using the uploaded document.

Rules:
- ONLY use the document.
- Do NOT use outside knowledge.
- Summarize the relevant information.
- Keep the answer concise.
- If the document does not contain the answer, reply ONLY with:

NOT_FOUND

Uploaded Document:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )

    answer = response.text.strip()

    if answer == "NOT_FOUND":
        return None

    return answer


def explain_with_ai(question, document_answer=None):
    """
    Generates an AI explanation.
    If a document summary exists, it expands upon it.
    Otherwise it answers using general knowledge.
    """

    if document_answer:
        prompt = f"""
You are WATCHTOWER.

The following answer was extracted from the uploaded document.

Document Answer:

{document_answer}

Your task:

- Expand upon the document.
- Make it easier to understand.
- Use your own knowledge where helpful.
- Give practical examples.
- Do NOT contradict the uploaded document.
- Do NOT repeat the document word-for-word.
- Assume the reader is a beginner.

User Question:
{question}
"""

    else:
        prompt = f"""
You are WATCHTOWER.

The uploaded documents do not contain the requested information.

Answer the user's question using your own knowledge.

Requirements:

- Beginner friendly.
- Clear explanation.
- Practical examples.
- Bullet points where appropriate.

User Question:
{question}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )

    return response.text.strip()
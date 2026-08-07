
print("========== GEMINI SERVICE LOADED ==========")
print(__file__)
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash"

print("========== GEMINI SERVICE LOADED ==========")
print("Using model:", MODEL)


def summarize_document(question, context):
    """
    Returns an answer ONLY from the uploaded document.
    """

    if not context.strip():
        return None

    prompt = f"""
You are WATCHTOWER.

Your ONLY job is to answer using the uploaded document.

Rules:
- ONLY use the uploaded document.
- Do NOT use outside knowledge.
- Keep the answer concise.
- If the answer is not present, reply ONLY with:

NOT_FOUND

Uploaded Document:
{context}

Question:
{question}
"""

    try:
        print("Calling Gemini (Document Summary)...")

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        answer = response.text.strip()

        print("Document Response:")
        print(answer)

        if answer == "NOT_FOUND":
            return None

        return answer

    except Exception as e:
        print("Gemini Document Error:")
        print(type(e).__name__)
        print(e)
        return None


def explain_with_ai(question, document_answer=None):
    """
    Returns a general AI explanation.
    """

    if document_answer:
        prompt = f"""
You are WATCHTOWER.

The following answer came from the uploaded document.

Document Answer:

{document_answer}

Expand upon it.

Requirements:
- Explain simply.
- Add useful examples.
- Do not contradict the document.
- Don't repeat it word-for-word.

Question:
{question}
"""
    else:
        prompt = f"""
You are WATCHTOWER.

The uploaded document does not contain the answer.

Answer using your own knowledge.

Question:
{question}
"""

    try:
        print("Calling Gemini (AI Explanation)...")

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        answer = response.text.strip()

        print("AI Response:")
        print(answer)

        return answer

    except Exception as e:
        print("Gemini AI Error:")
        print(type(e).__name__)
        print(e)
        return "Unable to connect to the AI service."
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def ask_gemini(question, context):
    prompt = f"""
You are WATCHTOWER.

Answer ONLY using the context below.

If the answer is not present in the context, reply:
"I couldn't find that information in the uploaded documents."

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents=prompt,
)

    return response.text
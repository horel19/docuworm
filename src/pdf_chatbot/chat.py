"""Send extracted PDF text and a user question to Gemini."""

from __future__ import annotations

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"

_SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions based on the "
    "provided PDF content. Use only the information in the document to "
    "answer. If the answer is not in the document, say so clearly."
)


def _get_client() -> genai.Client:
    """Return a Gemini client configured from the GEMINI_API_KEY env var."""
    return genai.Client()


def ask(document_text: str, question: str, history: list[dict] | None = None) -> str:
    """Send *question* along with *document_text* to Gemini and return the answer.

    *history* is an optional list of prior Content dicts to keep
    the conversation context across multiple turns.
    """
    client = _get_client()

    config = types.GenerateContentConfig(
        system_instruction=_SYSTEM_PROMPT,
    )

    chat = client.chats.create(model=MODEL_NAME, config=config, history=history)
    response = chat.send_message(
        f"Document:\n{document_text}\n\nQuestion: {question}"
    )
    return response.text

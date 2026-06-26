"""Pydantic models for chat messages and sessions."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single message in a chat conversation."""

    role: str = Field(..., pattern=r"^(user|assistant)$")
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatSession(BaseModel):
    """A conversation session tied to one uploaded PDF."""

    id: str = Field(default_factory=lambda: uuid4().hex)
    pdf_name: str
    pdf_text: str
    page_count: int = 0
    messages: list[ChatMessage] = Field(default_factory=list)

    def add_message(self, role: str, content: str) -> ChatMessage:
        """Append a message to the session and return it."""
        msg = ChatMessage(role=role, content=content)
        self.messages.append(msg)
        return msg

    def clear_messages(self) -> None:
        """Remove all chat messages, keeping the PDF context."""
        self.messages.clear()

"""models.py — Pydantic-модели API. Готово."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


class ExtractRequest(BaseModel):
    text: str


class Contact(BaseModel):
    """Схема, которую извлекаем из текста в /extract/contact."""
    name: str
    email: str
    phone: str

"""models.py — Pydantic-модели Task API. Готово."""

from pydantic import BaseModel


class TaskCreate(BaseModel):
    """Тело запроса на создание задачи (id присвоит БД)."""
    title: str


class Task(BaseModel):
    """Полная задача (то, что отдаём в ответах)."""
    id: int
    title: str
    done: bool = False

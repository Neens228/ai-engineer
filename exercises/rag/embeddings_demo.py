"""
RAG шаг 1 — эмбеддинги и смысловая близость.

Цель: увидеть, что похожие ПО СМЫСЛУ тексты дают близкие векторы.
Это фундамент векторного поиска в RAG.

Запуск:  uv run python exercises/rag/embeddings_demo.py
"""

import numpy as np
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "nomic-embed-text"


def get_embedding(text: str) -> list[float]:
    """Получить эмбеддинг (вектор чисел) для текста.
    Механика: client.embeddings.create(model=EMBED_MODEL, input=text)
    Вернуть: response.data[0].embedding
    """
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Косинусная близость двух векторов. Диапазон ~[-1..1], ближе к 1 = похожи по смыслу.
    Формула: dot(a, b) / (||a|| * ||b||).
    Используй numpy: np.dot(a, b) и np.linalg.norm(v).
    Верни обычный float.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def _check() -> None:
    cat = get_embedding("кот")
    kitten = get_embedding("котёнок")
    car = get_embedding("автомобиль")

    sim_close = cosine_similarity(cat, kitten)   # похожие по смыслу
    sim_far = cosine_similarity(cat, car)        # разные по смыслу

    print(f"кот ~ котёнок:    {sim_close:.3f}")
    print(f"кот ~ автомобиль: {sim_far:.3f}")

    # длина вектора эмбеддинга (размерность)
    print(f"размерность эмбеддинга: {len(cat)}")

    assert sim_close > sim_far, "похожие по смыслу тексты должны быть БЛИЖЕ"
    print("Работает: смысл отражается в близости векторов!")


if __name__ == "__main__":
    _check()

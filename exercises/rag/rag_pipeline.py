"""
RAG шаг 2 — чанкинг, векторная БД (Chroma), полный RAG-цикл.

Твои функции: chunk_text, retrieve, rag_answer. Обвязка Chroma готова.
Запуск:  uv run python exercises/rag/rag_pipeline.py
"""

import chromadb
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen2.5:7b"


def get_embedding(text: str) -> list[float]:
    """Готово (из шага 1)."""
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding


# --- Тестовый "документ" (база знаний вымышленной компании) ---
DOCUMENT = """
Компания ТехноСофт основана в 2015 году в Казани. Основатель — Алексей Смирнов.
Основной продукт компании — платформа СмартДок для электронного документооборота.
СмартДок поддерживает интеграцию с 1С, SAP и Битрикс24.
Тариф Базовый стоит 990 рублей в месяц за пользователя.
Тариф Корпоративный стоит 2490 рублей в месяц и включает приоритетную поддержку.
Техническая поддержка работает с 9:00 до 21:00 по московскому времени.
В компании работает 340 сотрудников, офисы в Казани, Москве и Новосибирске.
Пробный период составляет 30 дней, кредитная карта не требуется.
"""


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
    """Разбить текст на куски примерно по chunk_size символов с перекрытием overlap.
    Перекрытие нужно, чтобы мысль, разрезанная на границе, попала в оба куска.
    Пример: chunk_text("a"*500, 200, 50) -> куски [0:200], [150:350], [300:500]
    (каждый следующий начинается на chunk_size - overlap дальше предыдущего).
    Пустые куски не включать. Это та же логика, что в chunk() из задания на генераторы,
    только шаг = chunk_size - overlap.
    """
    result = []
    for i in range(0, len(text), chunk_size-overlap):
        chunk = text[i:i+chunk_size]
        if chunk:
            result.append(chunk)
    return result

# --- Chroma-обвязка (готово) ---
def build_index(chunks: list[str]) -> chromadb.Collection:
    """Создать in-memory коллекцию Chroma и сложить туда чанки с эмбеддингами."""
    db = chromadb.Client()                       # временная БД в памяти
    collection = db.create_collection("docs")
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks,
        embeddings=[get_embedding(c) for c in chunks],
    )
    return collection


def retrieve(collection: chromadb.Collection, question: str, top_k: int = 2) -> list[str]:
    """Найти top_k самых релевантных вопросу чанков.
    Механика Chroma: collection.query(query_embeddings=[<эмбеддинг вопроса>], n_results=top_k)
    вернёт dict; тексты лежат в result["documents"][0] (список строк).
    Верни этот список.
    """
    result = collection.query(query_embeddings=[get_embedding(question)], n_results=top_k)
    return result["documents"][0]

def rag_answer(collection: chromadb.Collection, question: str) -> str:
    """Полный RAG-цикл:
    1) chunks = retrieve(collection, question)
    2) собери контекст: склей найденные чанки через \\n
    3) промпт модели: system — "Отвечай ТОЛЬКО на основе контекста. Если ответа в
       контексте нет — скажи 'Не знаю'." ; user — f"Контекст:\\n{контекст}\\n\\nВопрос: {question}"
    4) верни ответ модели (content)
    """
    
    chunks = retrieve(collection, question)
    context = "\n".join(chunks)
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role":"system","content":"Отвечай ТОЛЬКО на основе контекста и только на русском языке. Если ответа вконтексте нет — скажи 'Не знаю'."},
            {"role":"user","content":f"Контекст:\\n{context}\\n\\nВопрос: {question}"},
            ],
        )
    return response.choices[0].message.content


def _check() -> None:
    chunks = chunk_text(DOCUMENT, chunk_size=200, overlap=50)
    print(f"Чанков: {len(chunks)}")
    assert len(chunks) >= 3, "документ должен разбиться на несколько чанков"

    collection = build_index(chunks)

    # retrieval: по вопросу о цене найтись должен чанк с тарифами
    found = retrieve(collection, "Сколько стоит тариф Базовый?")
    assert any("990" in c for c in found), f"в найденных чанках нет цены: {found}"
    print("retrieve -> нашёл чанк с ценой")

    # полный RAG: ответ должен опираться на документ
    a1 = rag_answer(collection, "Сколько стоит тариф Базовый?")
    print("Q: цена Базового ->", a1)
    assert "990" in a1, f"ответ должен содержать 990: {a1!r}"

    a2 = rag_answer(collection, "Кто основал компанию и когда?")
    print("Q: основатель ->", a2)
    assert "смирнов" in a2.lower() or "2015" in a2, f"ответ: {a2!r}"

    # проверка на галлюцинации: этого нет в документе
    a3 = rag_answer(collection, "Какая выручка компании за 2024 год?")
    print("Q: выручка (нет в доке) ->", a3)
    assert "не знаю" in a3.lower() or "нет" in a3.lower(), f"должен честно сказать 'не знаю': {a3!r}"

    print("Все проверки пройдены! RAG работает.")


if __name__ == "__main__":
    _check()

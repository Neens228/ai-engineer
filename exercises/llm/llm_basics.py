"""
Задание — основы LLM API (через Ollama, OpenAI-совместимо).

Формат: условие + примеры, решаешь сам. Документация: platform.openai.com/docs (раздел Chat).
Запуск:  uv run python exercises/llm/llm_basics.py
(Ответы небыстрые — модель на CPU. Это норма.)
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:7b"


def ask(question: str) -> str:
    """Задать модели вопрос и вернуть ТЕКСТ ответа (строку).
    Один user-message. Верни содержимое ответа (content), а не весь объект.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Ты дружелюбный ассистент. Отвечай кратко, на русском."},
            {"role": "user", "content": question},
    ],
    )
    return response.choices[0].message.content


def ask_with_system(question: str, system: str) -> str:
    """То же, но добавь system-сообщение, которое задаёт поведение модели.
    Порядок в messages: сначала system, потом user.
    Пример: ask_with_system("Кто ты?", "Ты кот. Отвечай мяуканьем.") -> что-то про мяу.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
    ],
    )
    return response.choices[0].message.content


def chat(messages: list[dict]) -> str:
    """Принять ГОТОВУЮ историю сообщений (список словарей с role/content) и вернуть ответ модели.
    Это основа multi-turn: модель stateless, поэтому контекст — это вся переданная история.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.choices[0].message.content


def _check() -> None:
    # 1) базовый вызов
    a = ask("Сколько будет 2+2? Ответь только числом.")
    assert isinstance(a, str) and len(a) > 0
    print("ask ->", a)

    # 2) system-промпт меняет поведение
    b = ask_with_system("Привет!", "Ты отвечаешь ТОЛЬКО заглавными буквами.")
    assert isinstance(b, str) and len(b) > 0
    print("ask_with_system ->", b)

    # 3) multi-turn: модель должна вспомнить имя из ИСТОРИИ (а не из одного сообщения)
    history = [
        {"role": "user", "content": "Меня зовут Игорь."},
        {"role": "assistant", "content": "Приятно познакомиться, Игорь!"},
        {"role": "user", "content": "Как меня зовут? Ответь одним словом."},
    ]
    c = chat(history)
    assert isinstance(c, str) and len(c) > 0
    assert "игор" in c.lower(), f"модель должна помнить имя из истории, ответ: {c!r}"
    print("chat (multi-turn) ->", c)

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

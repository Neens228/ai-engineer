"""
test_api.py — тесты AI-ассистента через TestClient.
Медленно (реальные вызовы LLM на CPU) — это норма.

Запуск (из папки projects/ai-assistant):  uv run python test_api.py
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _check() -> None:
    # health
    assert client.get("/").status_code == 200

    # /chat — ассистент должен через инструмент посчитать 15*4 = 60
    r = client.post("/chat", json={"message": "Сколько будет 15 умножить на 4?"})
    assert r.status_code == 200, r.text
    reply = r.json()["reply"]
    assert "60" in reply, f"ожидалось 60 в ответе: {reply!r}"
    print("chat ->", reply)

    # /extract/contact — извлечь структуру из текста
    r = client.post(
        "/extract/contact",
        json={"text": "Свяжитесь с Иваном Петровым: ivan@example.com, +7 999 123-45-67"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "иван" in data["name"].lower(), f"name: {data['name']}"
    assert "@" in data["email"], f"email: {data['email']}"
    print("extract ->", data)

    print("Все проверки API пройдены!")


if __name__ == "__main__":
    _check()

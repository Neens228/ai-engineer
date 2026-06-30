"""
first_call.py — первый запрос к локальной LLM (Qwen 2.5 7B через Ollama).

КЛЮЧЕВОЕ: используем ОФИЦИАЛЬНЫЙ OpenAI SDK, просто направленный на Ollama.
Тот же код будет работать с настоящим OpenAI — поменяются только base_url и api_key.

Запуск:  python first_call.py
(Первый ответ может занять 10-40 сек: модель грузится в память. Дальше быстрее.)
"""

from openai import OpenAI

# Ollama предоставляет OpenAI-совместимый эндпоинт на localhost:11434/v1
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",   # для Ollama ключ не нужен, но SDK требует непустую строку
)

response = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[
        {"role": "system", "content": "Ты дружелюбный ассистент. Отвечай кратко, на русском."},
        {"role": "user", "content": "Привет! Объясни в двух предложениях, что такое API."},
    ],
)

print("=== Ответ модели ===")
print(response.choices[0].message.content)

"""
llm.py — ядро работы с LLM. Готово (чистые версии твоих run_agent / extract).

Это переиспользуемый слой: НЕ знает про HTTP/FastAPI, только про модель.
main.py будет вызывать эти функции.
"""

import json
from openai import OpenAI
from pydantic import BaseModel

from tools import AVAILABLE, TOOLS

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:7b"

ASSISTANT_SYSTEM = (
    "Ты полезный ассистент. Отвечай на русском. Для арифметики и текущего времени "
    "ОБЯЗАТЕЛЬНО используй доступные инструменты, а не считай сам."
)


def assistant_chat(message: str) -> str:
    """Ответ ассистента с поддержкой инструментов (полный tool-calling цикл)."""
    messages = [
        {"role": "system", "content": ASSISTANT_SYSTEM},
        {"role": "user", "content": message},
    ]
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    msg = response.choices[0].message

    if not msg.tool_calls:
        return msg.content

    # модель попросила инструменты: выполняем и возвращаем результаты
    messages.append(msg)                      # ответ ассистента с tool_calls — ОДИН раз
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        result = AVAILABLE[tc.function.name](**args)
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    final = client.chat.completions.create(model=MODEL, messages=messages)
    return final.choices[0].message.content


def extract_data(text: str, schema: type[BaseModel]) -> BaseModel:
    """Извлечь структурированные данные из текста по Pydantic-схеме."""
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Извлеки данные из текста строго по заданной схеме."},
            {"role": "user", "content": text},
        ],
        response_format=schema,
    )
    return completion.choices[0].message.parsed

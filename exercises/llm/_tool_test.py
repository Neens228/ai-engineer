"""Проверка: умеет ли Qwen через Ollama в tool calling."""

import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:7b"


def get_weather(city: str) -> str:
    # фейковые данные для теста
    return f"В городе {city}: +15°C, ясно"


# Описание инструмента для модели (JSON Schema)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Узнать текущую погоду в указанном городе",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Название города"}
                },
                "required": ["city"],
            },
        },
    }
]

messages = [
    {
        "role": "system",
        "content": "Ты ассистент с доступом к инструментам. Когда нужна актуальная информация "
        "(погода и т.п.) — ОБЯЗАТЕЛЬНО вызывай подходящий инструмент, а не выдумывай ответ.",
    },
    {"role": "user", "content": "Какая сейчас погода в Москве?"},
]

# Шаг 1: модель решает, вызывать ли инструмент
response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
msg = response.choices[0].message
print("Модель попросила вызвать инструменты:", bool(msg.tool_calls))
print("Текст ответа модели:", repr(msg.content))

if msg.tool_calls:
    tc = msg.tool_calls[0]
    print("  функция:", tc.function.name)
    print("  аргументы:", tc.function.arguments)

    # Шаг 2: выполняем функцию
    args = json.loads(tc.function.arguments)
    result = get_weather(**args)
    print("  результат функции:", result)

    # Шаг 3: возвращаем результат модели
    messages.append(msg)  # ответ модели с tool_calls
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    # Шаг 4: финальный ответ человеку
    final = client.chat.completions.create(model=MODEL, messages=messages)
    print("Финальный ответ:", final.choices[0].message.content)

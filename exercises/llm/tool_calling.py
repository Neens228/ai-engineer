"""
Задание — Tool calling: мини-агент с инструментами.

Реализуй run_agent — полный цикл: модель выбирает инструмент -> ты выполняешь ->
возвращаешь результат -> модель отвечает. Образец механики — в _tool_test.py.

Запуск:  uv run python exercises/llm/tool_calling.py
"""

import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:7b"


# --- Инструменты (готовы) ---
def calculate(a: float, b: float, op: str) -> str:
    table = {"+": a + b, "-": a - b, "*": a * b, "/": (a / b if b else "деление на ноль")}
    return str(table.get(op, "неизвестная операция"))


def get_time() -> str:
    return datetime.now().strftime("%H:%M")


# Диспетчер: имя -> функция (пригодится, чтобы вызвать функцию по имени от модели)
AVAILABLE = {"calculate": calculate, "get_time": get_time}


# Описания инструментов для модели (готовы)
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Выполнить арифметику над двумя числами",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                    "op": {"type": "string", "description": "Один из: + - * /"},
                },
                "required": ["a", "b", "op"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Узнать текущее время",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

SYSTEM = (
    "Ты ассистент с инструментами. Для арифметики и текущего времени "
    "ОБЯЗАТЕЛЬНО используй инструменты, а не считай сам."
)


def run_agent(question: str) -> str:
    """Полный цикл tool calling:
    1) messages = [system (SYSTEM), user (question)]
    2) запрос модели с tools=tools
    3) если msg.tool_calls — для КАЖДОГО вызова:
         - распарси аргументы (json.loads(tc.function.arguments))
         - выполни нужную функцию через AVAILABLE[tc.function.name](**args)
         - добавь в messages ответ модели (msg) и результат: {"role":"tool", "tool_call_id": tc.id, "content": <результат>}
       затем ещё раз запроси модель и верни её финальный content
    4) если tool_calls нет — верни msg.content сразу
    Образец — в _tool_test.py (там один инструмент; тебе нужно поддержать несколько в цикле).
    """
    messages =[{"role":"system", "content":SYSTEM},
            {"role":"user", "content":question}]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )
    msg = response.choices[0].message
    if msg.tool_calls:
        messages.append(msg)
        for tc in msg.tool_calls:
            result = AVAILABLE[tc.function.name](**json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        final = client.chat.completions.create(model=MODEL, messages=messages)
        return final.choices[0].message.content
    else:
        return msg.content

def _check() -> None:
    a = run_agent("Сколько будет 15 умножить на 4?")
    print("calc ->", a)
    assert "60" in a, f"ожидалось 60 в ответе: {a!r}"

    t = run_agent("Который сейчас час? Назови время.")
    print("time ->", t)
    assert ":" in t, f"ожидалось время (ЧЧ:ММ) в ответе: {t!r}"

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

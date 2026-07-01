"""tools.py — инструменты ассистента и их описания для модели. Готово."""

from datetime import datetime


def calculate(a: float, b: float, op: str) -> str:
    table = {"+": a + b, "-": a - b, "*": a * b, "/": (a / b if b else "деление на ноль")}
    return str(table.get(op, "неизвестная операция"))


def get_time() -> str:
    return datetime.now().strftime("%H:%M")


# Диспетчер: имя (от модели) -> функция
AVAILABLE = {"calculate": calculate, "get_time": get_time}


# Описания инструментов для LLM (JSON Schema)
TOOLS = [
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

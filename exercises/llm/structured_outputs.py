"""
Задание — Structured Outputs: универсальный экстрактор данных.

Напиши ОДНУ функцию extract, которая достаёт структурированные данные из текста
по любой Pydantic-схеме. Образец механики — в _structured_test.py.

Запуск:  uv run python exercises/llm/structured_outputs.py
"""

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:7b"


class Product(BaseModel):
    name: str
    price: float
    in_stock: bool


class Order(BaseModel):
    customer: str
    items: list[str]      # вложенный список — модель должна разобрать перечисление
    total: float


def extract(text: str, schema: type[BaseModel]) -> BaseModel:
    """Извлечь из text данные по Pydantic-схеме schema и вернуть готовый объект schema.
    - используй client.beta.chat.completions.parse
    - response_format = schema
    - дай разумный system-промпт (типа "Извлеки данные из текста по схеме")
    - верни completion.choices[0].message.parsed
    """
    response = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Извлеки данные из текста по заданной схеме"},
            {"role": "user", "content": text},
        ],
        response_format=schema
    )
    return response.choices[0].message.parsed
def _check() -> None:
    # Product
    p = extract("Ноутбук стоит 50000 рублей, есть в наличии.", Product)
    assert isinstance(p, Product)
    assert p.price == 50000, f"price: {p.price}"
    assert p.in_stock is True
    print("Product ->", p)

    # Order с вложенным списком items
    o = extract("Заказ от Анны: молоко, хлеб, сыр. Итого 350 рублей.", Order)
    assert isinstance(o, Order)
    assert "анн" in o.customer.lower(), f"customer: {o.customer}"
    assert len(o.items) == 3, f"items: {o.items}"
    assert o.total == 350, f"total: {o.total}"
    print("Order ->", o)

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

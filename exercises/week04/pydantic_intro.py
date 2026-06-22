"""
Задание 8 — Pydantic: модели, валидация, вложенность (Неделя 4).

ВАЖНО: запускать через uv (чтобы подхватился .venv с pydantic):
    uv run python exercises/week04/pydantic_intro.py

Класс User уже готов как образец — изучи его. Реализуй Product, Order и total_price.
Цель: "Все проверки пройдены!".
"""

from pydantic import BaseModel, ValidationError


# ============================================================
# ОБРАЗЕЦ (готов) — изучи
# ============================================================

class User(BaseModel):
    name: str
    age: int
    is_active: bool = True       # поле со значением по умолчанию

    # У моделей Pydantic тоже могут быть методы:
    def greet(self) -> str:
        return f"Привет, {self.name}!"


# ============================================================
# ТВОИ МОДЕЛИ
# ============================================================

class Product(BaseModel):
    """Товар. Поля:
        name: str
        price: float
        quantity: int = 1       (по умолчанию 1)
    Просто опиши три поля с аннотациями — тело класса как у User, без методов."""
    # TODO: опиши поля name, price, quantity
    name: str
    price: float
    quantity: int = 1



def total_price(product: "Product") -> float:
    """Вернуть полную стоимость товара: price * quantity.
    HINT: обращайся к полям через product.price и product.quantity."""
    return product.price * product.quantity


class Order(BaseModel):
    """Заказ. Поля:
        customer: str
        products: list[Product]    (СПИСОК товаров — вложенная модель!)
    Pydantic сам превратит список словарей в список объектов Product и провалидирует их."""
    # TODO: опиши поля customer и products
    customer : str
    products: list[Product]


def _check() -> None:
    # --- Образец User ---
    u = User(name="Игорь", age=25)
    assert u.age == 25 and u.is_active is True
    assert u.greet() == "Привет, Игорь!"
    # преобразование типов: строка -> int
    assert User(name="Анна", age="30").age == 30
    # в словарь и обратно
    assert u.model_dump() == {"name": "Игорь", "age": 25, "is_active": True}
    # валидация: плохой возраст -> ошибка
    try:
        User(name="X", age="не число")
        raise AssertionError("ожидалась ValidationError")
    except ValidationError:
        pass

    # --- Product ---
    p = Product(name="Книга", price=500.0)
    assert p.quantity == 1                       # значение по умолчанию
    assert total_price(p) == 500.0
    # преобразование: строки -> float и int
    p2 = Product(name="Ручка", price="10.5", quantity="3")
    assert p2.price == 10.5 and p2.quantity == 3
    assert total_price(p2) == 31.5
    # валидация: цена не число -> ошибка
    try:
        Product(name="X", price="дорого")
        raise AssertionError("ожидалась ValidationError")
    except ValidationError:
        pass

    # --- Order с вложенными Product ---
    order = Order(
        customer="Игорь",
        products=[
            {"name": "A", "price": 100},
            {"name": "B", "price": 200, "quantity": 2},
        ],
    )
    assert len(order.products) == 2
    # КЛЮЧЕВОЕ: словари превратились в объекты Product автоматически
    assert isinstance(order.products[0], Product)
    assert order.products[1].quantity == 2
    assert total_price(order.products[1]) == 400.0

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

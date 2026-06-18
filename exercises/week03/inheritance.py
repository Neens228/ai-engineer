"""
Задание 5.1 — ООП: наследование, super(), dataclasses (ПРОБЕЛ недели 3).

Две темы:
  ЧАСТЬ A — наследование и super() (классы Shape -> Circle/Square)
  ЧАСТЬ B — dataclasses (готовый пример Point + твой класс User)

Запуск:  python inheritance.py
Цель:    "Все проверки пройдены!"
"""

from dataclasses import dataclass
import math


# ============================================================
# ЧАСТЬ A — НАСЛЕДОВАНИЕ
# ============================================================

class Shape:
    """Базовый класс (родитель). Хранит имя фигуры и задаёт 'контракт' area()."""

    def __init__(self, name: str) -> None:
        self.name = name

    def area(self) -> float:
        # Базовая версия. Дочерние классы ПЕРЕОПРЕДЕЛЯТ этот метод под себя.
        return 0.0

    def describe(self) -> str:
        # Этот метод НЕ переопределяем — он достанется наследникам как есть (DRY).
        # round(..., 2) округляет до 2 знаков.
        return f"{self.name} с площадью {round(self.area(), 2)}"


class Circle(Shape):
    """Круг. Наследует Shape. Площадь = pi * r^2."""

    def __init__(self, radius: float) -> None:
        # Вызови конструктор родителя через super().__init__(...) с именем "circle",
        # затем сохрани self.radius = radius.
        super().__init__("circle")
        self.radius = radius

    def area(self) -> float:
        # Переопредели: верни площадь круга. Используй math.pi.
        return math.pi * self.radius ** 2


class Square(Shape):
    """Квадрат. Наследует Shape. Площадь = side^2."""

    def __init__(self, side: float) -> None:
        # super().__init__("square"), затем self.side = side.
        super().__init__("square")
        self.side = side

    def area(self) -> float:
        # Переопредели: верни площадь квадрата.
        return self.side ** 2


# ============================================================
# ЧАСТЬ B — DATACLASSES
# ============================================================
#
# dataclass — это способ создать класс ТОЛЬКО для хранения данных без ручного __init__.
# Декоратор @dataclass автоматически генерирует __init__, __repr__ и __eq__.
#
# ОБРАЗЕЦ (готов) — сравни, насколько короче обычного класса:

@dataclass
class Point:
    x: int
    y: int
    # Всё! __init__(self, x, y) сгенерирован автоматически.
    # Можно: p = Point(1, 2); p.x -> 1; p == Point(1, 2) -> True

    def distance_to_origin(self) -> float:
        # В dataclass тоже можно добавлять обычные методы:
        return math.sqrt(self.x ** 2 + self.y ** 2)


# ТВОЯ ОЧЕРЕДЬ: сделай dataclass User с полями:
#   name: str
#   age: int
#   is_active: bool = True      # поле со значением по умолчанию
#
# И добавь метод greet(self) -> str, возвращающий "Привет, <name>!".
# Напиши класс User здесь (с декоратором @dataclass):

# <-- твой код тут

@dataclass
class User:
    name: str
    age: int
    is_active: bool = True

    def greet(self) -> str:
        return f"Привет, {self.name}!" 



def _check() -> None:
    # ЧАСТЬ A
    c = Circle(2)
    assert abs(c.area() - 12.566370614359172) < 1e-9   # pi * 2^2
    assert c.name == "circle"
    assert c.describe() == "circle с площадью 12.57"

    s = Square(3)
    assert s.area() == 9
    assert s.name == "square"
    assert s.describe() == "square с площадью 9"

    # Полиморфизм: один и тот же describe() работает для разных фигур
    shapes = [Circle(1), Square(2)]
    descriptions = [shape.describe() for shape in shapes]
    assert descriptions == ["circle с площадью 3.14", "square с площадью 4"]

    # ЧАСТЬ B — образец Point
    p = Point(3, 4)
    assert p.x == 3 and p.y == 4
    assert p.distance_to_origin() == 5.0
    assert Point(1, 2) == Point(1, 2)        # dataclass сам сделал сравнение по значениям

    # ЧАСТЬ B — твой User
    u = User("Игорь", 25)
    assert u.name == "Игорь"
    assert u.age == 25
    assert u.is_active is True                # значение по умолчанию
    assert u.greet() == "Привет, Игорь!"
    u2 = User("Анна", 30, is_active=False)
    assert u2.is_active is False

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

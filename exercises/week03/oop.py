"""
Задание 5 — ООП: классы, __init__, self, методы, состояние (Неделя 3).

ВАЖНО: первый класс Rectangle уже написан ПОЛНОСТЬЮ как образец — изучи его
и комментарии. Остальные три класса (Counter, BankAccount, Stack) — твои:
замени `raise NotImplementedError` в методах своим кодом.

Запуск:  python oop.py
Цель:    "Все проверки пройдены!"
"""


# ============================================================
# ОБРАЗЕЦ (уже готов) — изучи внимательно, дальше по аналогии
# ============================================================

class Rectangle:
    """Прямоугольник: хранит ширину и высоту, умеет считать площадь и периметр."""

    def __init__(self, width: int, height: int) -> None:
        # __init__ вызывается автоматически при Rectangle(...).
        # self — это создаваемый объект. Сохраняем данные В нём:
        self.width = width
        self.height = height

    def area(self) -> int:
        # Метод обращается к данным своего объекта через self:
        return self.width * self.height

    def perimeter(self) -> int:
        return 2 * (self.width + self.height)


# ============================================================
# ТВОИ КЛАССЫ — реализуй методы
# ============================================================

class Counter:
    """Счётчик. Хранит число (старт 0), умеет увеличивать и сбрасывать.
    Пример:
        c = Counter()
        c.increment(); c.increment()
        c.value  -> 2
        c.reset()
        c.value  -> 0
    """

    def __init__(self) -> None:
        # Заведи атрибут self.value со стартовым значением 0.
        self.value = 0

    def increment(self) -> None:
        # Увеличь self.value на 1. Ничего возвращать не нужно.
        self.value +=1

    def reset(self) -> None:
        # Сбрось self.value обратно в 0.
        self.value = 0


class BankAccount:
    """Банковский счёт. Хранит баланс (по умолчанию 0).
        deposit(amount)  — пополнить (увеличить баланс).
        withdraw(amount) — снять: если хватает денег, уменьшить баланс и вернуть True;
                           если НЕ хватает (amount > balance) — баланс не трогать, вернуть False.
    Пример:
        a = BankAccount()      # баланс 0
        a.deposit(100)         # баланс 100
        a.withdraw(30)         # -> True,  баланс 70
        a.withdraw(1000)       # -> False, баланс остаётся 70
    """

    def __init__(self, balance: int = 0) -> None:
        # Сохрани переданный balance в self.balance (по умолчанию 0).
        self.balance = balance

    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False


class Stack:
    """Стек (структура LIFO — last in, first out): кладём и снимаем с вершины.
    Внутри храни элементы в обычном списке self.items.
        push(item) — положить элемент на вершину.
        pop()      — снять и ВЕРНУТЬ верхний элемент.
        peek()     — вернуть верхний элемент, НЕ снимая его.
        is_empty() — True, если стек пуст, иначе False.
        size()     — количество элементов.
    Пример:
        s = Stack()
        s.push(1); s.push(2); s.push(3)
        s.size()     -> 3
        s.peek()     -> 3      (не снимает)
        s.pop()      -> 3      (снимает)
        s.size()     -> 2
        s.is_empty() -> False
    HINT: список уже умеет почти всё — .append(x), .pop(), [-1], len(...).
    """

    def __init__(self) -> None:
        # Заведи пустой список self.items.
        self.items = []

    def push(self, item: int) -> None:
        self.items.append(item)

    def pop(self) -> int:
       return self.items.pop()

    def peek(self) -> int:
       return self.items[-1]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def size(self) -> int:
       return len(self.items)


def _check() -> None:
    # Rectangle (образец)
    r = Rectangle(3, 4)
    assert r.area() == 12
    assert r.perimeter() == 14

    # Counter
    c = Counter()
    assert c.value == 0
    c.increment()
    c.increment()
    assert c.value == 2
    c.reset()
    assert c.value == 0

    # BankAccount
    a = BankAccount()
    assert a.balance == 0
    a.deposit(100)
    assert a.balance == 100
    assert a.withdraw(30) is True
    assert a.balance == 70
    assert a.withdraw(1000) is False
    assert a.balance == 70

    # BankAccount с начальным балансом
    a2 = BankAccount(50)
    assert a2.balance == 50

    # Stack
    s = Stack()
    assert s.is_empty() is True
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.size() == 3
    assert s.peek() == 3
    assert s.size() == 3          # peek не снимает
    assert s.pop() == 3
    assert s.size() == 2
    assert s.is_empty() is False

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

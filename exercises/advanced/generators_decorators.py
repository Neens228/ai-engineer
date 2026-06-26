"""
Углубление A — Генераторы и декораторы.

Формат новый: даны УСЛОВИЕ и ПРИМЕРЫ. Пошаговых подсказок нет — думай сам.
Гуглить синтаксис ("python yield", "python decorator with arguments") — нормально.

Запуск:  python generators_decorators.py
Цель:    "Все проверки пройдены!"
"""

import functools


# ============================================================
# ГЕНЕРАТОРЫ (используй yield, НЕ возвращай готовый список)
# ============================================================

def countdown(n: int):
    """Генератор: выдаёт числа от n до 1 включительно, по убыванию.
    list(countdown(3)) -> [3, 2, 1]
    """
    while n != 0:
        yield n
        n = n-1
        


def fibonacci(n: int):
    """Генератор первых n чисел Фибоначчи, начиная с 0, 1.
    list(fibonacci(7)) -> [0, 1, 1, 2, 3, 5, 8]
    list(fibonacci(1)) -> [0]
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b



def chunk(items: list, size: int):
    """Генератор: выдаёт список кусками по size элементов (последний может быть короче).
    list(chunk([1, 2, 3, 4, 5], 2)) -> [[1, 2], [3, 4], [5]]
    """
    for i in range(0, len(items), size):
        yield items[i:i+size]
        



def take(iterable, n: int) -> list:
    """Вернуть СПИСОК из первых n значений итерируемого (генератора).
    Должно работать с БЕСКОНЕЧНЫМ генератором — то есть нельзя делать list(iterable) целиком.
    take(countdown(100), 3) -> [100, 99, 98]
    """
    result = []
    for item in iterable:
        if len(result) == n:
            break
        result.append(item)
    return result  



# ============================================================
# ДЕКОРАТОРЫ
# ============================================================

def uppercase(func):
    """Декоратор: берёт функцию, возвращающую строку, и делает результат заглавным.
    @uppercase
    def greet(name): return f"hi {name}"
    greet("bob") -> "HI BOB"
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs) 
        modified_result = result.upper() 
        return modified_result    
    return wrapper 
    


def count_calls(func):
    """Декоратор: считает, сколько раз функцию вызвали.
    Счётчик доступен как атрибут .calls у обёрнутой функции.
    @count_calls
    def ping(): return "pong"
    ping(); ping()
    ping.calls -> 2
    """

    def wrapper(*args, **kwargs):
        wrapper.calls += 1 
        return func(*args, **kwargs)
    wrapper.calls = 0    
    return wrapper


def repeat(times: int):
    """Декоратор С АРГУМЕНТОМ: вызывает функцию `times` раз и возвращает СПИСОК результатов.
    @repeat(3)
    def roll(): return 7
    roll() -> [7, 7, 7]
    """
    result = []
    def decorator(func):
        def wrapper(*args, **kwargs):
            temp = func(*args)
            return [temp for i in range(times)]
        return wrapper
    return decorator
    
def _check() -> None:
    # --- Генераторы ---
    import types
    assert isinstance(countdown(3), types.GeneratorType), "countdown должен быть генератором (yield)"
    assert list(countdown(3)) == [3, 2, 1]
    assert list(countdown(1)) == [1]
    assert list(fibonacci(7)) == [0, 1, 1, 2, 3, 5, 8]
    assert list(fibonacci(1)) == [0]
    assert list(chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(chunk([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]
    assert take(countdown(100), 3) == [100, 99, 98]

    # --- Декораторы ---
    @uppercase
    def greet(name):
        return f"hi {name}"
    
    assert greet("bob") == "HI BOB"

    @count_calls
    def ping():
        return "pong"
    ping()
    ping()
    ping()
    
    assert ping.calls == 3

    @repeat(3)
    def roll():
        return 7
    
    assert roll() == [7, 7, 7]

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

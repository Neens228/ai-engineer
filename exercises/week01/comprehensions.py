"""
Задание 3 — List & dict comprehensions (Неделя 1, финал).

ЦЕЛЬ: научиться писать циклы-сборщики компактно.
Каждую функцию реши ОДНИМ comprehension (одной строкой после return).

Шаблоны для опоры:
    [ <что кладём>  for <элемент> in <источник> ]
    [ <что кладём>  for <элемент> in <источник>  if <условие> ]
    { <ключ>: <значение>  for <элемент> in <источник> }   # это dict comprehension

Если буксуешь — сначала напиши ОБЫЧНЫЙ цикл с append на черновике,
а потом сожми его в comprehension. Это нормальный способ.

Запуск:  python comprehensions.py
Цель:    "Все проверки пройдены!"
"""


def squares(n: int) -> list[int]:
    """Квадраты чисел от 0 до n-1. squares(5) -> [0, 1, 4, 9, 16].
    HINT: [x * x for x in range(n)]."""
    return [x * x for x in range(n)]


def evens(numbers: list[int]) -> list[int]:
    """Только чётные числа из списка, в том же порядке. evens([1,2,3,4,5,6]) -> [2,4,6].
    HINT: comprehension с условием if."""
    return [x for x in numbers if x % 2 == 0]


def lengths(words: list[str]) -> list[int]:
    """Длины слов. lengths(["a", "bb", "ccc"]) -> [1, 2, 3]."""
    return [len(x) for x in words]


def upper_long(words: list[str]) -> list[str]:
    """Слова длиннее 3 символов, переведённые в ВЕРХНИЙ регистр.
    upper_long(["hi", "hello", "code", "ok"]) -> ["HELLO", "CODE"].
    HINT: и преобразование (.upper()), и фильтр (if len(...) > 3) в одном comprehension."""
    return [x.upper() for x in words if len(x) > 3] 

def no_vowels(text: str) -> str:
    """Убрать все гласные (a,e,i,o,u) из строки, регистр входа сохраняем для согласных.
    no_vowels("Hello World") -> "Hll Wrld".
    HINT: comprehension по символам + условие, что символ.lower() НЕ в "aeiou",
    потом "".join(...) чтобы собрать обратно в строку."""
    return "".join([x for x in text if x.lower() not in "aeiou"])


def square_map(n: int) -> dict[int, int]:
    """dict {число: его квадрат} для чисел от 1 до n включительно.
    square_map(3) -> {1: 1, 2: 4, 3: 9}.
    HINT: dict comprehension {x: x * x for x in range(1, n + 1)}."""
    return {x: x * x  for x in range(1, n + 1)}


def _check() -> None:
    assert squares(5) == [0, 1, 4, 9, 16]
    assert evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6]
    assert lengths(["a", "bb", "ccc"]) == [1, 2, 3]
    assert upper_long(["hi", "hello", "code", "ok"]) == ["HELLO", "CODE"]
    assert no_vowels("Hello World") == "Hll Wrld"
    assert square_map(3) == {1: 1, 2: 4, 3: 9}
    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

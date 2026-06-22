"""
Задание 7a — Кортежи (tuple). Мини-тема.

Замени `raise NotImplementedError` своим кодом. Сигнатуры не меняй.
Запуск:  python tuples.py
Цель:    "Все проверки пройдены!"
"""


def swap(a: int, b: int) -> tuple[int, int]:
    """Вернуть пару с переставленными местами значениями.
    swap(1, 2) -> (2, 1).
    HINT: можно просто return b, a — Python сам сделает кортеж."""
    return b,a


def first_last(items: list[int]) -> tuple[int, int]:
    """Вернуть кортеж (первый элемент, последний элемент) списка.
    first_last([10, 20, 30, 40]) -> (10, 40)."""
    return (items[0],items[-1])


def divmod_pair(a: int, b: int) -> tuple[int, int]:
    """Вернуть кортеж (частное, остаток) от деления a на b.
    divmod_pair(17, 5) -> (3, 2)   # 17 = 5*3 + 2
    HINT: // это целочисленное деление, % это остаток."""
    return (a//b, a%b)


def split_evens_odds(numbers: list[int]) -> tuple[list[int], list[int]]:
    """Разделить числа на чётные и нечётные. Вернуть кортеж (чётные, нечётные).
    split_evens_odds([1, 2, 3, 4, 5]) -> ([2, 4], [1, 3, 5]).
    HINT: заведи два списка, пройди циклом, верни их как (evens, odds)."""
    evens = []
    odds = []
    for number in numbers:
        if number % 2 == 0:
            evens.append(number)
        else:
            odds.append(number)
    return (evens,odds)


def _check() -> None:
    assert swap(1, 2) == (2, 1)

    # распаковка результата-кортежа в две переменные:
    x, y = swap(10, 20)
    assert x == 20 and y == 10

    assert first_last([10, 20, 30, 40]) == (10, 40)
    assert divmod_pair(17, 5) == (3, 2)
    assert split_evens_odds([1, 2, 3, 4, 5]) == ([2, 4], [1, 3, 5])

    # проверка неизменяемости кортежа:
    t = (1, 2, 3)
    try:
        t[0] = 99            # должно бросить TypeError
        raise AssertionError("кортеж не должен меняться!")
    except TypeError:
        pass                 # ожидаемо — кортежи неизменяемы

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

"""
Задание 4 — Функции, *args/**kwargs, sorted(key=), set, распаковка (Неделя 2).

Новые темы этой недели. По каждой — короткая функция.
Принцип прежний: замени `raise NotImplementedError` своим кодом, сигнатуры не трогай.

Запуск:  python functions.py
Цель:    "Все проверки пройдены!"
"""


# --- Аргументы по умолчанию ---

def power(base: int, exp: int = 2) -> int:
    """Возвести base в степень exp. Если exp не передан — по умолчанию 2 (квадрат).
    power(5) -> 25 ;  power(2, 3) -> 8.
    HINT: оператор ** возводит в степень. Значение по умолчанию уже задано в сигнатуре."""
    return base**exp


# --- *args: произвольное число позиционных аргументов ---

def total(*numbers: int) -> int:
    """Сумму ВСЕХ переданных чисел, сколько бы их ни было.
    total(1, 2, 3) -> 6 ;  total() -> 0 ;  total(10) -> 10.
    HINT: внутри функции `numbers` это кортеж (tuple) всех аргументов. Пройди по нему циклом
    или используй встроенную sum()."""
    total = 0
    for number in numbers:
        total += number
    return total


# --- **kwargs: произвольное число именованных аргументов ---

def build_url(base: str, **params: str) -> str:
    """Собрать URL со строкой запроса из именованных аргументов.
    build_url("site.com") -> "site.com"
    build_url("site.com", page="2", sort="new") -> "site.com?page=2&sort=new"
    HINT: `params` внутри — это dict {имя: значение}. Если он пустой — верни base.
    Иначе собери части "ключ=значение" и склей их через "&", добавив "?" после base.
    Порядок именованных аргументов в Python сохраняется."""
    
    if len(params) == 0:
        return base
    base = base + "?"
    return base+"&".join(f"{key}={val}" for key,val in params.items())


# --- Возврат нескольких значений (кортеж) ---

def min_max(numbers: list[int]) -> tuple[int, int]:
    """Вернуть пару (минимум, максимум). Тут можно использовать встроенные min() и max().
    min_max([3, 1, 9, 4]) -> (1, 9).
    HINT: return min(numbers), max(numbers) — Python сам сделает кортеж."""
    return (min(numbers),max(numbers))


# --- Распаковка в цикле: dict.items() ---

def format_pairs(data: dict[str, int]) -> list[str]:
    """Превратить словарь в список строк "ключ=значение".
    format_pairs({"a": 1, "b": 2}) -> ["a=1", "b=2"].
    HINT: for key, value in data.items(): ... — это распаковка пары прямо в цикле."""
    return [key+"="+str(val) for key,val in data.items()]

# --- set: множество (уникальные элементы, быстрая проверка) ---

def common(a: list[int], b: list[int]) -> list[int]:
    """Вернуть ОТСОРТИРОВАННЫЙ список чисел, которые есть И в a, И в b (без повторов).
    common([1, 2, 3, 4], [2, 4, 6]) -> [2, 4].
    HINT: set(a) & set(b) даёт пересечение множеств. sorted(...) превратит в отсортированный список."""
    return sorted(set(a) & set(b))


# --- sorted с key= и lambda ---

def sort_by_length(words: list[str]) -> list[str]:
    """Отсортировать слова по ДЛИНЕ (от короткого к длинному).
    sort_by_length(["ccc", "a", "bb"]) -> ["a", "bb", "ccc"].
    HINT: sorted(words, key=len). key — это функция, по которой считается "вес" для сортировки."""
    return sorted(words, key=len)



def sort_by_second(pairs: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Отсортировать список пар (имя, число) по ЧИСЛУ (второму элементу), по возрастанию.
    sort_by_second([("a", 3), ("b", 1), ("c", 2)]) -> [("b", 1), ("c", 2), ("a", 3)].
    HINT: sorted(pairs, key=lambda pair: pair[1]).
    lambda — это безымянная функция-однострочник: `lambda x: x[1]` берёт второй элемент пары."""
    return sorted(pairs, key=lambda pair: pair[1])

def _check() -> None:
    assert power(5) == 25
    assert power(2, 3) == 8
    assert total(1, 2, 3) == 6
    assert total() == 0
    assert total(10) == 10
    assert build_url("site.com") == "site.com"
    assert build_url("site.com", page="2", sort="new") == "site.com?page=2&sort=new"
    assert min_max([3, 1, 9, 4]) == (1, 9)
    assert format_pairs({"a": 1, "b": 2}) == ["a=1", "b=2"]
    assert common([1, 2, 3, 4], [2, 4, 6]) == [2, 4]
    assert sort_by_length(["ccc", "a", "bb"]) == ["a", "bb", "ccc"]
    assert sort_by_second([("a", 3), ("b", 1), ("c", 2)]) == [("b", 1), ("c", 2), ("a", 3)]
    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

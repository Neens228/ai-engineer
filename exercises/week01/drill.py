"""
Задание 2 — Drill: списки, словари, циклы, строки (Неделя 1, закрепление).

ЦЕЛЬ: довести базовые операции до автоматизма через повторение.
10 коротких функций. Принцип тот же: замени `raise NotImplementedError` своим кодом.

Совет: сначала пробуй сам. Гуглить СИНТАКСИС ("python как ...") — можно.
Но прежде чем писать, скажи себе вслух, ЧТО должна делать функция. Логику — сам.

Запуск:  python drill.py
Цель:    внизу печатается "Все проверки пройдены!"
"""


# --- Списки ---

def last_three(items: list[int]) -> list[int]:
    """Вернуть последние 3 элемента списка. last_three([1,2,3,4,5]) -> [3,4,5].
    HINT: срез list[-3:]."""
    return items[-3:]

def maximum(numbers: list[int]) -> int:
    """Вернуть наибольшее число БЕЗ встроенной max(). Делай через цикл.
    maximum([3, 9, 2, 7]) -> 9."""
    result = float('-inf')
    for number in numbers:
        if number > result:
            result = number
    return result


def count_positives(numbers: list[int]) -> int:
    """Сколько чисел в списке строго больше нуля. count_positives([-1, 0, 2, 5]) -> 2."""
    count = 0
    for number in numbers:
        if number > 0:
            count = count+1
    return count


def unique(items: list[int]) -> list[int]:
    """Вернуть список без повторов, СОХРАНИВ порядок первого появления.
    unique([1, 2, 2, 3, 1]) -> [1, 2, 3].
    HINT: заведи пустой список результата и проверяй `if x not in result`."""
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


# --- Строки ---

def count_vowels(text: str) -> int:
    """Сколько гласных (a, e, i, o, u) в строке. Регистр не важен.
    count_vowels("Hello") -> 2.
    HINT: гласные собери в строку "aeiou", приведи текст к нижнему регистру,
    иди циклом по символам и проверяй `if ch in "aeiou"`."""
    count = 0
    for texts in text.lower():
        if texts in "aeiou":
            count +=1
    return count


def is_palindrome(text: str) -> bool:
    """True, если строка читается одинаково в обе стороны. is_palindrome("argentina") -> False,
    is_palindrome("level") -> True. HINT: сравни строку с её разворотом text[::-1]."""
    return text == text[::-1]


def initials(full_name: str) -> str:
    """Вернуть инициалы заглавными через точку. initials("ivan petrov") -> "I.P.".
    HINT: split() по словам, у каждого слова возьми [0], сделай .upper()."""
    names = full_name.split()
    result = ""
    for name in names:
        result = result + name[0].upper() + "."
    return result

# --- Словари ---

def merge_counts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """Сложить два словаря-счётчика. Если ключ есть в обоих — значения суммируются.
    merge_counts({"x": 1, "y": 2}, {"y": 3, "z": 5}) -> {"x": 1, "y": 5, "z": 5}.
    HINT: начни с копии a (dict(a)), потом пройди по b.items()."""
    summary = a
    for char in b:
        if char in a:
            summary[char] = summary[char] + b[char]
        else:
            summary[char] = b[char]
    return summary



def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Сгруппировать слова по их длине.
    group_by_length(["a", "bb", "cc", "ddd"]) -> {1: ["a"], 2: ["bb", "cc"], 3: ["ddd"]}.
    HINT: ключ = len(word). Если ключа нет — создай пустой список, потом append."""
    result = {}
    for word in words:
        if len(word) in result:
            result[len(word)].append(word)
        else:
            result[len(word)] = [word]
    return result


def most_common(text: str) -> str:
    """Вернуть самое частое слово в тексте (слова разделены пробелами, регистр не важен).
    most_common("a b a c a b") -> "a".
    HINT: переиспользуй идею word_count, потом найди ключ с максимальным значением."""
    count = {}
    max = 0
    max_result =""
    text = text.split()
    for txt in text:
        if txt in count:
            count[txt] = count[txt]+1
        else:
            count[txt] = 1
        if max < count[txt]:
            max = count[txt]
            max_result = txt
    return max_result


def _check() -> None:
    assert last_three([1, 2, 3, 4, 5]) == [3, 4, 5]
    assert last_three([1, 2]) == [1, 2]
    assert maximum([3, 9, 2, 7]) == 9
    assert maximum([-5, -1, -10]) == -1
    assert count_positives([-1, 0, 2, 5]) == 2
    assert unique([1, 2, 2, 3, 1]) == [1, 2, 3]
    assert count_vowels("Hello") == 2
    assert count_vowels("PYTHON") == 1
    assert is_palindrome("level") is True
    assert is_palindrome("argentina") is False
    assert initials("ivan petrov") == "I.P."
    assert merge_counts({"x": 1, "y": 2}, {"y": 3, "z": 5}) == {"x": 1, "y": 5, "z": 5}
    assert group_by_length(["a", "bb", "cc", "ddd"]) == {1: ["a"], 2: ["bb", "cc"], 3: ["ddd"]}
    assert most_common("a b a c a b") == "a"
    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

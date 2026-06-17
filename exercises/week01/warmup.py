"""
Задание 1 — Рефреш Python (Неделя 1).

Как делать:
1. Заполни тело каждой функции вместо `raise NotImplementedError`.
2. НЕ меняй имена функций и их сигнатуры (имена и типы аргументов).
3. Запусти файл:  python warmup.py
4. Если всё верно — внизу напечатается "Все проверки пройдены!".

Метка HINT — небольшая подсказка. Гуглить и читать документацию — нормально и нужно.
"""


def greet(name: str) -> str:
    """Вернуть приветствие. greet("Игорь") -> "Привет, Игорь!" (HINT: f-строки)."""
    return f"Привет, {name}!"


def is_even(n: int) -> bool:
    """True, если число чётное, иначе False. HINT: оператор % (остаток от деления)."""
    return True if n%2 == 0 else False


def sum_even(numbers: list[int]) -> int:
    """Сумма только чётных чисел списка. sum_even([1, 2, 3, 4, 10]) -> 16."""
    sum = 0
    for number in numbers:
        if number%2 == 0:
            sum = sum + number
    return sum


def fizzbuzz(n: int) -> list[str]:
    """
    Вернуть список строк для чисел от 1 до n включительно:
      - кратно 3 и 5 -> "FizzBuzz"
      - кратно 3     -> "Fizz"
      - кратно 5     -> "Buzz"
      - иначе        -> само число строкой, например "7"
    fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
    """
    fizzbuzz_list = []
    for i in range(1,n+1):
        if i%3 == 0 and i%5 == 0:
            fizzbuzz_list.append("FizzBuzz")
        elif i%5 == 0:
            fizzbuzz_list.append("Buzz")
        elif i%3 == 0:
            fizzbuzz_list.append("Fizz")
        else:
            fizzbuzz_list.append(str(i))
    return fizzbuzz_list

def word_count(text: str) -> dict[str, int]:
    """
    Посчитать, сколько раз встречается каждое слово (слова разделены пробелами).
    Регистр не важен: word_count("Кот кот") -> {"кот": 2}.
    HINT: .lower(), .split(), обычный словарь.
    """
    counts = {}
    words = text.lower().split()
    for word in words:
        if word in counts:
            counts[word] = counts[word]+1
        else:
            counts[word] = 1
    return counts


def reverse_words(sentence: str) -> str:
    """Перевернуть порядок слов. reverse_words("я люблю python") -> "python люблю я"."""
    results = sentence.split()
    result_sentence = results[::-1]
    result_sentence = " ".join(result_sentence)
    return result_sentence

print(reverse_words("я люблю python"))

def _check() -> None:
    assert greet("Игорь") == "Привет, Игорь!"
    assert is_even(4) is True
    assert is_even(7) is False
    assert sum_even([1, 2, 3, 4, 10]) == 16
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert fizzbuzz(15)[-1] == "FizzBuzz"
    assert word_count("Кот кот КОТ пёс") == {"кот": 3, "пёс": 1}
    assert reverse_words("я люблю python") == "python люблю я"
    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

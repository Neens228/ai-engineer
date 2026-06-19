"""
textutils.py — модуль с функциями для работы с текстом.

Ещё один отдельный модуль. Реализуй две функции ниже.
"""


def shout(text: str) -> str:
    """Вернуть текст ЗАГЛАВНЫМИ буквами с восклицательным знаком в конце.
    shout("hello") -> "HELLO!"."""
    return text.upper() + "!"

def word_count(text: str) -> int:
    """Количество слов в строке (слова разделены пробелами).
    word_count("раз два три") -> 3."""
    return len(text.split())


if __name__ == "__main__":
    print("Демо textutils:")
    print("  shout:", shout("hello"))
    print("  word_count:", word_count("раз два три"))

"""
main.py — ГЛАВНЫЙ модуль. Импортирует функции из geometry.py и textutils.py
и использует их. Это демонстрация того, как файлы программы соединяются.

ВАЖНО: этот файл НИЧЕГО не реализует сам — он только импортирует чужие функции.
Твоя задача — дописать ИМПОРТЫ вверху (две строки), чтобы код заработал.

Запуск (из папки modules):  python main.py
Цель:    "Все проверки пройдены!"
"""

# TODO: добавь сюда два импорта:
#   1) из модуля geometry  импортируй  circle_area  и  rectangle_area
#   2) из модуля textutils импортируй  shout        и  word_count
# Подсказка по форме:  from <имя_файла_без_py> import <функция1>, <функция2>

# <-- твои импорты тут
from geometry import circle_area, rectangle_area
from textutils import shout, word_count



def _check() -> None:
    # Используем функции, импортированные из ДРУГИХ файлов:
    assert abs(circle_area(2) - 12.566370614359172) < 1e-9
    assert rectangle_area(3, 4) == 12
    assert shout("hello") == "HELLO!"
    assert word_count("раз два три") == 3
    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

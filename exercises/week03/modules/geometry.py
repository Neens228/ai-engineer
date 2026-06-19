"""
geometry.py — модуль с геометрическими функциями.

Это ОТДЕЛЬНЫЙ файл (модуль). Другой файл сможет импортировать эти функции так:
    from geometry import circle_area, rectangle_area

Задание: реализуй две функции ниже.
"""

import math


def circle_area(radius: float) -> float:
    """Площадь круга: pi * r^2."""
    return radius**2 * math.pi


def rectangle_area(width: float, height: float) -> float:
    """Площадь прямоугольника: width * height."""
    return width*height


# Этот блок выполнится ТОЛЬКО при прямом запуске `python geometry.py`,
# но НЕ при импорте этого файла из другого модуля.
if __name__ == "__main__":
    print("Демо geometry:")
    print("  круг r=2:", circle_area(2))
    print("  прямоугольник 3x4:", rectangle_area(3, 4))

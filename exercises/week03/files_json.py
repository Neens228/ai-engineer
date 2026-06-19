"""
Задание 6 — Исключения, файлы, JSON (Неделя 3).

Три темы:
  A) Исключения: try/except
  B) Файлы: open + with
  C) JSON: dump/load

Замени `raise NotImplementedError` своим кодом. Сигнатуры не меняй.

Запуск:  python files_json.py
Цель:    "Все проверки пройдены!"
"""

import json
from pathlib import Path


# ============================================================
# A) ИСКЛЮЧЕНИЯ
# ============================================================

def safe_divide(a: float, b: float) -> float | None:
    """Вернуть a / b. Если b == 0 — поймать ZeroDivisionError и вернуть None.
    safe_divide(10, 2) -> 5.0 ;  safe_divide(10, 0) -> None.
    HINT: оберни деление в try, поймай except ZeroDivisionError."""
    try:
        return a/b
    except ZeroDivisionError:
        return None


def parse_int(text: str) -> int | None:
    """Превратить строку в число. Если не получается (ValueError) — вернуть None.
    parse_int("42") -> 42 ;  parse_int("abc") -> None.
    HINT: int(text) бросает ValueError на нечисловой строке."""
    try:
        return int(text)
    except ValueError:
        return None


def safe_get(data: dict, key: str) -> str:
    """Вернуть data[key]. Если ключа нет (KeyError) — вернуть строку "нет данных".
    safe_get({"a": "1"}, "a") -> "1" ;  safe_get({}, "x") -> "нет данных".
    HINT: можно через try/except KeyError. (Да, есть .get(), но тут тренируем except.)"""
    try:
        return data[key]
    except KeyError:
        return "нет данных"


# ============================================================
# B) ФАЙЛЫ
# ============================================================

def write_text(path: str, content: str) -> None:
    """Записать строку content в файл по пути path (режим "w", encoding="utf-8").
    HINT: with open(path, "w", encoding="utf-8") as f: f.write(content)."""

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ============================================================
# C) JSON
# ============================================================

def save_json(path: str, data: dict) -> None:
    """Сохранить словарь data в JSON-файл по пути path.
    HINT: with open(path, "w", encoding="utf-8") as f: json.dump(data, f).
    Совет на будущее: json.dump(data, f, ensure_ascii=False, indent=2) — читаемее,
    но для прохождения теста достаточно простого json.dump(data, f)."""

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def _check() -> None:
    # A) исключения
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) is None
    assert parse_int("42") == 42
    assert parse_int("abc") is None
    assert safe_get({"a": "1"}, "a") == "1"
    assert safe_get({}, "x") == "нет данных"

    # B) файлы (с очисткой временного файла через try/finally)
    tmp_txt = Path("_tmp_check.txt")
    try:
        write_text(str(tmp_txt), "привет\nмир")
        assert read_text(str(tmp_txt)) == "привет\nмир"
    finally:
        tmp_txt.unlink(missing_ok=True)

    # C) json (записать -> прочитать -> данные совпали)
    tmp_json = Path("_tmp_check.json")
    try:
        data = {"name": "Игорь", "age": 25, "tags": ["python", "ai"]}
        save_json(str(tmp_json), data)
        assert load_json(str(tmp_json)) == data
    finally:
        tmp_json.unlink(missing_ok=True)

    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()

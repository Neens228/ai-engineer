"""
models.py — модель данных задачи (Task).

Это самый нижний слой приложения: описывает, ЧТО такое задача.
Он не знает ни про базу данных, ни про команды пользователя — только структура.

Запуск проверки (из корня ai-engineer):
    uv run python projects/task-cli/models.py
"""

from pydantic import BaseModel


class Task(BaseModel):
    """Задача в списке дел. Поля:
        id: int             — порядковый номер задачи
        title: str          — текст задачи
        done: bool = False  — выполнена ли (по умолчанию нет)
    Опиши три поля с аннотациями — как делал в задании про Pydantic.
    """
    id: int
    title: str
    done: bool = False


if __name__ == "__main__":
    # Быстрая проверка модели
    t = Task(id=1, title="Купить молоко")
    print("Создана задача:", t)
    assert t.id == 1
    assert t.title == "Купить молоко"
    assert t.done is False          # значение по умолчанию

    # done можно задать явно
    t2 = Task(id=2, title="Помыть посуду", done=True)
    assert t2.done is True

    # Pydantic валидирует: id должен быть числом
    print("Модель Task работает!")

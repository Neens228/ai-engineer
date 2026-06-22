"""
storage.py — слой хранения задач в SQLite.

Этот слой знает про базу данных и про Task, но НЕ знает про команды пользователя.
get_connection и init_db уже написаны как образец. Реализуй три функции ниже.

Запуск проверки (из папки projects/task-cli):
    python storage.py
    # (или, когда заработает uv: uv run python storage.py)
"""

import sqlite3
from models import Task

DB_PATH = "tasks.db"


# ============================================================
# ОБРАЗЕЦ (готов) — изучи паттерн работы с sqlite3
# ============================================================

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Открыть соединение с базой. row_factory позволяет обращаться к колонкам по имени."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row      # строки можно читать как row["title"]
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Создать таблицу tasks, если её ещё нет."""
    conn = get_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            done  INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


# ============================================================
# ТВОИ ФУНКЦИИ
# ============================================================

def add_task(title: str, db_path: str = DB_PATH) -> Task:
    """Добавить задачу в БД и вернуть её как объект Task (с присвоенным id).
    Шаги:
      1) conn = get_connection(db_path)
      2) cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
      3) conn.commit()
      4) new_id = cursor.lastrowid          # id, который БД присвоила автоматически
      5) conn.close()
      6) return Task(id=new_id, title=title, done=False)
    """
    conn = get_connection(db_path)
    cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)",(title,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return Task(id=new_id, title=title, done=False)


def get_all_tasks(db_path: str = DB_PATH) -> list[Task]:
    """Вернуть список всех задач, отсортированный по id.
    Шаги:
      1) conn = get_connection(db_path)
      2) rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
      3) conn.close()
      4) собрать список: Task(id=row["id"], title=row["title"], done=bool(row["done"]))
         (done в БД хранится как 0/1, bool(...) превратит в False/True)
    HINT: подойдёт list comprehension по rows.
    """
    conn = get_connection(db_path)
    rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [Task(id=row["id"], title=row["title"], done=bool(row["done"])) for row in rows] 


def mark_done(task_id: int, db_path: str = DB_PATH) -> None:
    """Отметить задачу с данным id как выполненную (done = 1).
    Шаги:
      1) conn = get_connection(db_path)
      2) conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
      3) conn.commit()
      4) conn.close()
    """
    conn = get_connection(db_path)
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?",(task_id,))
    conn.commit()
    conn.close()


def _check() -> None:
    import os

    test_db = "_test_tasks.db"
    if os.path.exists(test_db):
        os.remove(test_db)

    try:
        init_db(test_db)

        # пустая база
        assert get_all_tasks(test_db) == []

        # добавление
        t1 = add_task("Купить молоко", test_db)
        assert t1.id == 1
        assert t1.title == "Купить молоко"
        assert t1.done is False

        t2 = add_task("Помыть посуду", test_db)
        assert t2.id == 2

        # чтение всех
        tasks = get_all_tasks(test_db)
        assert len(tasks) == 2
        assert tasks[0].title == "Купить молоко"

        # отметить выполненной
        mark_done(1, test_db)
        tasks = get_all_tasks(test_db)
        assert tasks[0].done is True       # задача 1 теперь выполнена
        assert tasks[1].done is False      # задача 2 ещё нет

        print("storage.py работает! Все проверки пройдены.")
    finally:
        if os.path.exists(test_db):
            os.remove(test_db)


if __name__ == "__main__":
    _check()

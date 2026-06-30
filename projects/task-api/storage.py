"""
storage.py — слой SQLite для Task API. Готово (ты это писал в task-cli).
Функции возвращают True/False для «найдено/не найдено», чтобы эндпоинты решали про 404.
"""

import sqlite3
from models import Task

DB_PATH = "tasks_api.db"


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
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


def get_all_tasks(db_path: str = DB_PATH) -> list[Task]:
    conn = get_connection(db_path)
    rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [Task(id=r["id"], title=r["title"], done=bool(r["done"])) for r in rows]


def get_task(task_id: int, db_path: str = DB_PATH) -> Task | None:
    conn = get_connection(db_path)
    row = conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return Task(id=row["id"], title=row["title"], done=bool(row["done"]))


def add_task(title: str, db_path: str = DB_PATH) -> Task:
    conn = get_connection(db_path)
    cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return Task(id=new_id, title=title, done=False)


def set_done(task_id: int, db_path: str = DB_PATH) -> bool:
    """Вернёт True, если задача нашлась и обновлена; False, если такой id нет."""
    conn = get_connection(db_path)
    cur = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed


def delete_task(task_id: int, db_path: str = DB_PATH) -> bool:
    """Вернёт True, если задача нашлась и удалена; False, если такой id нет."""
    conn = get_connection(db_path)
    cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed

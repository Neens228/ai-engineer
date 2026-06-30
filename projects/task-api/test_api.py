"""
test_api.py — автопроверка Task API через FastAPI TestClient.
TestClient гоняет запросы к приложению БЕЗ реального запуска сервера.

Запуск (из папки projects/task-api):
    python test_api.py
Цель: "Все проверки API пройдены!"
"""

import os

# Чистим тестовую БД ДО импорта приложения (чтобы старт был с нуля).
if os.path.exists("tasks_api.db"):
    os.remove("tasks_api.db")

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _check() -> None:
    # пустой список
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []

    # создать (POST с телом)
    r = client.post("/tasks", json={"title": "Купить молоко"})
    assert r.status_code == 201, f"ожидался 201, получен {r.status_code}"
    task = r.json()
    assert task["id"] == 1 and task["title"] == "Купить молоко" and task["done"] is False

    # ещё одна
    client.post("/tasks", json={"title": "Помыть посуду"})

    # список из двух
    r = client.get("/tasks")
    assert len(r.json()) == 2

    # одна по id
    r = client.get("/tasks/1")
    assert r.status_code == 200
    assert r.json()["title"] == "Купить молоко"

    # несуществующая -> 404
    r = client.get("/tasks/999")
    assert r.status_code == 404

    # отметить выполненной
    r = client.patch("/tasks/1/done")
    assert r.status_code == 200
    assert r.json()["done"] is True

    # done для несуществующей -> 404
    assert client.patch("/tasks/999/done").status_code == 404

    # удалить
    r = client.delete("/tasks/1")
    assert r.status_code == 200

    # delete несуществующей -> 404
    assert client.delete("/tasks/999").status_code == 404

    # осталась одна
    assert len(client.get("/tasks").json()) == 1

    print("Все проверки API пройдены!")


if __name__ == "__main__":
    _check()

"""
Task API — Шаг 1: знакомство с FastAPI.

Запуск (из папки projects/task-api):
    uvicorn main:app --reload
Потом открой в браузере:  http://localhost:8000/docs  (интерактивная документация)
Остановить сервер:  Ctrl+C
"""

from fastapi import FastAPI, HTTPException

from models import Task, TaskCreate
from storage import (
    init_db,
    get_all_tasks,
    get_task,
    add_task,
    set_done,
    delete_task,
)

app = FastAPI(title="Task API")
init_db()   # создаём таблицу при старте


# health-check
@app.get("/")
async def root():
    return {"message": "Task API работает"}


# ОБРАЗЕЦ (готов) — список всех задач. Изучи и делай остальные по аналогии.
@app.get("/tasks", response_model=list[Task])
async def list_tasks():
    return get_all_tasks()


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(data: TaskCreate):
    task = add_task(data.title)
    return task
    

@app.get("/tasks/{task_id}")
async def show_task(task_id : int):
    task = get_task(task_id)
    if task is not None:
        return task
    else:
        raise HTTPException(status_code=404,detail="Задача не найдена")

@app.patch("/tasks/{task_id}/done")
async def task_done(task_id: int):
    ok = set_done(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    else:
        return get_task(task_id)


@app.delete("/tasks/{task_id}")
async def route_delete_task(task_id: int):
    ok = delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    else:
        return {"deleted": task_id}


# ЗАДАНИЕ 1: POST /tasks — создать задачу
#   - принимает тело запроса TaskCreate (JSON {"title": "..."})
#   - объяви параметр функции:  data: TaskCreate   (FastAPI возьмёт его из тела)
#   - создай через add_task(data.title), верни созданный Task
#   - выставь код 201:  @app.post("/tasks", response_model=Task, status_code=201)


# ЗАДАНИЕ 2: GET /tasks/{task_id} — одна задача (task_id: int)
#   - task = get_task(task_id);  если None -> raise HTTPException(status_code=404, detail="Задача не найдена")
#   - иначе верни task


# ЗАДАНИЕ 3: PATCH /tasks/{task_id}/done — отметить выполненной
#   - ok = set_done(task_id);  если не ok (False) -> 404
#   - иначе верни обновлённую задачу через get_task(task_id)


# ЗАДАНИЕ 4: DELETE /tasks/{task_id} — удалить задачу
#   - ok = delete_task(task_id);  если не ok -> 404
#   - иначе верни {"deleted": task_id}

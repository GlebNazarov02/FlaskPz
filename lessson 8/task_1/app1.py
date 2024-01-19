# Задание №1
# 📌 Создать API для управления списком задач. Приложение должно иметь
# возможность создавать, обновлять, удалять и получать список задач.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс Task с полями id, title, description и status.
# 📌 Создайте список tasks для хранения задач.
# 📌 Создайте маршрут для получения списка задач (метод GET).
# 📌 Создайте маршрут для создания новой задачи (метод POST).
# 📌 Создайте маршрут для обновления задачи (метод PUT).
# 📌 Создайте маршрут для удаления задачи (метод DELETE).
# 📌 Реализуйте валидацию данных запроса и ответа.


import logging
import uvicorn
from fastapi import FastAPI

from models import TaskBase, db1, Task, Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app1 = FastAPI()


@app1.get("/tasks")
async def read_root():
    res = []
    logger.info('Отработал GET запрос.')
    tasks = db1.query(TaskBase).all()
    for task in tasks:
        res.append(
            f"  task_id: {task.task_id}, title: {task.title}, description: "
            f"{task.description}, status: {task.status}  ")
    return res


@app1.get("/tasks/{task_id}")
async def read_root(task_id: int):
    logger.info('Отработал GET запрос.')
    task = db1.query(TaskBase).filter(TaskBase.task_id == task_id).first()
    return f"Task:  task_id: {task.task_id}, title: {task.title}, " \
        f"description: {task.description}, status: {task.status}"


@app1.post("/tasks/{task_id}")
async def create_item(task_id: int, task: Task):
    logger.info('Отработал POST запрос.')
    tasks = db1.query(TaskBase).filter(TaskBase.task_id == task_id).all()
    for task in tasks:
        if task.task_id == task_id:
            return f'Task already exist!'
    else:
        new_item = TaskBase(task_id=task.task_id, title=task.title,
                            description=task.description, status=task.status,
                            is_del=False)
        db1.add(new_item)
        db1.commit()
        return f'Task: {task}'


@app1.put("/tasks/{task_id}")
async def update_item(task_id: int, task_upd: Task):
    logger.info(f'Отработал PUT запрос для task id = {task_id}.')
    task = db1.query(TaskBase).filter(TaskBase.task_id == task_id).first()
    task.title = task_upd.title
    task.description = task_upd.description
    task.status = task_upd.status
    db1.commit()
    return {"task_id": task_id, "task": task_upd}


@app1.delete("/tasks/{task_id}")
async def delete_item(task_id: int):
    logger.info(f'Отработал DELETE запрос для task id = {task_id}.')
    tasks = db1.query(TaskBase).filter(TaskBase.task_id == task_id).all()
    for task in tasks:
        db1.delete(task)
        db1.commit()
    return {"task_id": task_id}

if __name__ == '__main__':
    uvicorn.run('app1:app', host='127.0.0.1', port=8000, reload=True)
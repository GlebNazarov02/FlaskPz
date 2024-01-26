from fastapi import FastAPI
from typing import List
from models import TaskBase, db5, Task, Base, engine
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

tasks = []

@app.get("/tasks/")
async def read_root():
    res = []
    logger.info('Отработал GET запрос.')
    tasks = db5.query(TaskBase).all()
    for task in tasks:
        res.append(
            f"  task_id: {task.task_id}, title: {task.title}, "
            f"description: {task.description}, status: {task.status}  ")
    return res


@app.get("/tasks/{task_id}")
async def read_root(task_id: int):
    logger.info('Отработал GET запрос.')
    task = db5.query(TaskBase).filter(TaskBase.task_id == task_id).first()
    return f"Task:  task_id: {task.task_id}, title: {task.title}," \
        f" description: {task.description}, status: {task.status}"


@app.post("/tasks/")
async def create_task(new_task: Task):
    task_id = 1
    logger.info('Отработал POST запрос.')
    tasks = db5.query(TaskBase).all()
    if db5.query(TaskBase.task_id).first():
        for task in tasks:
            if task_id == task.task_id:
                task_id += 1
            else:
                break
        new_item = TaskBase(task_id=task_id, title=new_task.title,
                            description=new_task.description,
                            status=new_task.status, is_del=False)
        db5.add(new_item)
        db5.commit()
        return f'Task: {new_item}'

    else:
        new_item = TaskBase(task_id=task_id, title=new_task.title,
                            description=new_task.description,
                            status=new_task.status, is_del=False)
        db5.add(new_item)
        db5.commit()
        return f'Task: {new_item}'


@app.post("/tasks/{task_id}")
async def create_item(task_id: int, task: Task):
    logger.info('Отработал POST запрос.')
    tasks = db5.query(TaskBase).filter(TaskBase.task_id == task_id).all()
    for task in tasks:
        if task.task_id == task_id:
            return f'Task already exist!'
    else:
        new_item = TaskBase(task_id=task.task_id, title=task.title,
                            description=task.description, status=task.status,
                            is_del=False)
        db5.add(new_item)
        db5.commit()
        return f'Task: {task}'


@app.put("/tasks/{task_id}")
async def update_item(task_id: int, task_upd: Task):
    logger.info(f'Отработал PUT запрос для task id = {task_id}.')
    task = db5.query(TaskBase).filter(TaskBase.task_id == task_id).first()
    task.title = task_upd.title
    task.description = task_upd.description
    task.status = task_upd.status
    db5.commit()
    return {"task_id": task_id, "task": task_upd}


@app.delete("/tasks/{task_id}")
async def delete_item(task_id: int):
    logger.info(f'Отработал DELETE запрос для task id = {task_id}.')
    tasks = db5.query(TaskBase).filter(TaskBase.task_id == task_id).all()
    for task in tasks:
        db5.delete(task)
        db5.commit()
    return {"task_id": task_id}

if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=8000, reload=True)
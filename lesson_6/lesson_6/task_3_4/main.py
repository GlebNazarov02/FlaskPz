# Задание 3 и 4
# Создать API для управления списком задач.
# Каждая задача должна содержать поля "название",
# "описание" и "статус" (выполнена/не выполнена).
# API должен позволять выполнять CRUD операции с
# задачами.
from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy import select, delete, insert, update

from database import startup, shutdown, db
from schemas import TodoSchema, TodoInSchema, Status
from models import TodoModel

app = FastAPI(title='Seminar_6, task 3 and 4')
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/tasks/", response_model=List[TodoSchema])
async def get_all_tasks() -> List[TodoSchema]:
    """Получение списка всех задач: GET /tasks/"""
    query = select(TodoModel)
    tasks = await db.fetch_all(query)
    return tasks


@app.get("/tasks/{task_id}", response_model=TodoInSchema)
async def get_single_task(task_id: int) -> TodoInSchema:
    """Получение информации о конкретном задаче: GET /tasks/{task_id}/"""
    query = select(TodoModel).where(TodoModel.id == task_id)
    task = await db.fetch_one(query)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.post("/tasks/", response_model=TodoSchema)
async def create_new_task(task: TodoInSchema) -> dict:
    """Создание новой задачи: POST /tasks/"""
    query = insert(TodoModel)
    new_task = {"title": task.title, "description": task.description, "status": task.status}
    new_task_id = await db.execute(query, new_task)
    return {**new_task, "id": new_task_id}


@app.put("/tasks/{task_id}", response_model=TodoSchema)
async def update_task(task_id: int, task: TodoInSchema) -> TodoSchema:
    """Обновление информации о задаче: PUT /tasks/{task_id}/"""
    query = select(TodoModel).where(TodoModel.id == task_id)
    task_ = await db.fetch_one(query)
    if task_:
        updated_user = task.dict(exclude_unset=True)
        query = update(TodoModel).where(TodoModel.id == task_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(TodoModel).where(TodoModel.id == task_id))
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}", response_model=str)
async def delete_task(task_id: int):
    query = select(TodoModel).where(TodoModel.id == task_id)
    task = await db.fetch_one(query)
    if task:
        query = delete(TodoModel).where(TodoModel.id == task_id)
        await db.execute(query)
        return f'Задача {task.title} удалена.'
    raise HTTPException(status_code=404, detail="Задача не найдена")


if __name__ == '__main__':
    import asyncio

    asyncio.run(startup())


    async def virgin_db():
        query = delete(TodoModel)
        await db.execute(query)
        query = insert(TodoModel)
        for i in range(10):
            if i % 2 == 0:
                status = Status.DONE
            else:
                status = Status.IN_PROGRESS
            new_task = {"title": f"task{i}", "description": f"description{i}", "status": status}
            await db.execute(query, new_task)


    asyncio.run(virgin_db())

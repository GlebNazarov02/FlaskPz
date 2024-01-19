from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool

tasks = [
    {"id": 1, "title": "first", "description": "noname3", "status": True},
    {"id": 2, "title": "sec", "description": "noname2", "status": True},
    {"id": 3, "title": "third", "description": "noname1", "status": True}
]

@app.get('/')
async def root():
    return {'message': 'DZ'}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"error": "task not found"}

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    tasks.append(task.dict())
    return {"message": "task created"}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for idx, current_task in enumerate(tasks):
        if current_task["id"] == task_id:
            tasks[idx] = task.dict()
            return {"message": "task updated"}
    return {"error": "task not found"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for idx, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[idx]
            return {"message": "task deleted"}
    return {"error": "task not found"}

if __name__ == '__main__':
    uvicorn.run('app1:app', host='127.0.0.1', port=8000, reload=True)